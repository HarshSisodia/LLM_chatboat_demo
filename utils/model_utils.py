"""
Utility functions for model handling in the LLM Chatbot.
This module provides functions for working with language models.
"""

import os
import torch
from typing import Optional, Dict, Any
from transformers import AutoModelForCausalLM, AutoTokenizer

def check_model_availability(model_name: str) -> bool:
    """
    Check if a model is available locally or can be downloaded.
    
    Args:
        model_name: Name of the model to check
        
    Returns:
        True if the model is available, False otherwise
    """
    try:
        # Try to load the tokenizer as a quick check
        AutoTokenizer.from_pretrained(model_name)
        return True
    except Exception:
        return False

def get_model_info(model_name: str) -> Dict[str, Any]:
    """
    Get information about a model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary with model information
    """
    info = {
        "name": model_name,
        "available": check_model_availability(model_name),
        "is_local": os.path.exists(model_name),
        "requires_gpu": "large" in model_name.lower() or "medium" in model_name.lower(),
        "gpu_available": torch.cuda.is_available(),
        "recommended_for_chatbot": is_recommended_for_chatbot(model_name)
    }
    
    return info

def is_recommended_for_chatbot(model_name: str) -> bool:
    """
    Check if a model is recommended for chatbot use.
    
    Args:
        model_name: Name of the model
        
    Returns:
        True if recommended, False otherwise
    """
    # List of models known to work well for chatbots
    recommended_models = [
        "gpt2", "gpt2-medium", "distilgpt2", 
        "microsoft/DialoGPT-small", "microsoft/DialoGPT-medium",
        "facebook/blenderbot-400M-distill"
    ]
    
    return model_name in recommended_models

def get_recommended_models() -> Dict[str, Dict[str, Any]]:
    """
    Get a list of recommended models for chatbots.
    
    Returns:
        Dictionary of model names and their information
    """
    recommended_models = [
        "gpt2", "distilgpt2", "microsoft/DialoGPT-small"
    ]
    
    return {model: get_model_info(model) for model in recommended_models}

def estimate_memory_usage(model_name: str) -> Optional[float]:
    """
    Estimate the memory usage of a model in GB.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Estimated memory usage in GB, or None if unknown
    """
    # Rough estimates based on model size
    memory_estimates = {
        "gpt2": 0.5,
        "gpt2-medium": 1.5,
        "gpt2-large": 3.0,
        "gpt2-xl": 6.0,
        "distilgpt2": 0.3,
        "microsoft/DialoGPT-small": 0.5,
        "microsoft/DialoGPT-medium": 1.5,
        "facebook/blenderbot-400M-distill": 1.6
    }
    
    return memory_estimates.get(model_name)
