"""
Main application entry point for the LLM Chatbot.
This module initializes and runs the chatbot application.
"""

import os
import argparse
from app.chatbot import Chatbot
from app.config import Config

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='LLM Chatbot')
    parser.add_argument('--model', type=str, default='gpt2',
                        help='Model to use (default: gpt2)')
    parser.add_argument('--web', action='store_true',
                        help='Launch web interface')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port for web interface (default: 8000)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_arguments()
    
    # Load configuration
    config = Config()
    config.model_name = args.model
    config.debug = args.debug
    
    # Initialize chatbot
    chatbot = Chatbot(config)
    
    if args.web:
        # Start web interface
        from app.web_interface import start_web_server
        start_web_server(chatbot, port=args.port)
    else:
        # Start CLI interface
        print(f"LLM Chatbot initialized with model: {config.model_name}")
        print("Type 'exit' or 'quit' to end the conversation.")
        print("-" * 50)
        
        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            response = chatbot.generate_response(user_input)
            print(f"Bot: {response}")

if __name__ == "__main__":
    main()
