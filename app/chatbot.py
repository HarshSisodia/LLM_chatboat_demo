"""
Core chatbot implementation for the LLM Chatbot project.
This module handles the interaction with the language model and manages conversation context.
"""

import os
import json
import datetime
from typing import List, Dict, Any, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from app.config import Config
from utils.text_processing import clean_text, format_response

class Chatbot:
    """
    A chatbot class that uses a pre-trained language model to generate responses.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the chatbot with the specified configuration.
        
        Args:
            config: Configuration object containing settings for the chatbot
        """
        self.config = config
        self.model_name = config.model_name
        self.max_length = config.max_response_length
        self.temperature = config.temperature
        self.conversation_history = []
        
        # Load model and tokenizer
        self._load_model()
        
        # Create conversation directory if it doesn't exist
        os.makedirs(config.conversation_dir, exist_ok=True)
    
    def _load_model(self):
        """Load the language model and tokenizer."""
        try:
            print(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Create text generation pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            
            print(f"Model loaded successfully: {self.model_name}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to smaller model: distilgpt2")
            self.model_name = "distilgpt2"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
    
    def generate_response(self, user_input: str) -> str:
        """
        Generate a response to the user input.
        
        Args:
            user_input: The user's input text
            
        Returns:
            The generated response
        """
        # Clean the input text
        cleaned_input = clean_text(user_input)
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": cleaned_input})
        
        # Prepare prompt with conversation history
        prompt = self._prepare_prompt()
        
        # Generate response
        response = self._generate_text(prompt)
        
        # Clean and format the response
        formatted_response = format_response(response)
        
        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": formatted_response})
        
        # Save conversation if configured
        if self.config.save_conversations:
            self._save_conversation()
        
        return formatted_response
    
    def _prepare_prompt(self) -> str:
        """
        Prepare the prompt for the language model using conversation history.
        
        Returns:
            The prepared prompt string
        """
        # Use only the last few exchanges to avoid context length issues
        recent_history = self.conversation_history[-self.config.max_history_length:]
        
        prompt = ""
        for message in recent_history:
            if message["role"] == "user":
                prompt += f"User: {message['content']}\n"
            else:
                prompt += f"Assistant: {message['content']}\n"
        
        # Add the final prompt for the assistant
        prompt += "Assistant:"
        
        return prompt
    
    def _generate_text(self, prompt: str) -> str:
        """
        Generate text using the language model.
        
        Args:
            prompt: The input prompt for the model
            
        Returns:
            The generated text
        """
        try:
            # Generate text
            outputs = self.generator(
                prompt,
                max_length=len(self.tokenizer.encode(prompt)) + self.max_length,
                temperature=self.temperature,
                top_p=0.92,
                top_k=50,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract the generated text
            generated_text = outputs[0]['generated_text']
            
            # Extract only the assistant's response
            response = generated_text.split("Assistant:")[-1].strip()
            
            # Remove any trailing user prompts
            if "User:" in response:
                response = response.split("User:")[0].strip()
            
            return response
        
        except Exception as e:
            if self.config.debug:
                print(f"Error generating response: {e}")
            return "I'm sorry, I encountered an error while generating a response."
    
    def _save_conversation(self):
        """Save the current conversation to a file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.config.conversation_dir, f"conversation_{timestamp}.json")
        
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        return "Conversation has been reset."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            The conversation history as a list of message dictionaries
        """
        return self.conversation_history
