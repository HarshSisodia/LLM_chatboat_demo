"""
Utility functions for text processing in the LLM Chatbot.
This module provides functions for cleaning and formatting text.
"""

import re
import string
import html

def clean_text(text: str) -> str:
    """
    Clean and normalize input text.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
    """
    # Convert HTML entities
    text = html.unescape(text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove control characters
    text = ''.join(ch for ch in text if ch in string.printable)
    
    return text

def format_response(text: str) -> str:
    """
    Format the model's response for better readability.
    
    Args:
        text: Raw response from the model
        
    Returns:
        Formatted response
    """
    # Clean the text first
    text = clean_text(text)
    
    # Remove any trailing incomplete sentences
    if text and text[-1] not in '.!?':
        # Find the last sentence boundary
        last_boundary = max(text.rfind('.'), text.rfind('!'), text.rfind('?'))
        if last_boundary > 0:
            text = text[:last_boundary+1]
    
    # Ensure proper spacing after punctuation
    text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
    
    return text

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length while preserving complete sentences.
    
    Args:
        text: Text to truncate
        max_length: Maximum length in characters
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Find the last sentence boundary before max_length
    truncated = text[:max_length]
    last_boundary = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
    
    if last_boundary > 0:
        return text[:last_boundary+1]
    else:
        # If no sentence boundary found, just truncate at max_length
        return truncated + "..."

def extract_keywords(text: str, max_keywords: int = 5) -> list:
    """
    Extract key words or phrases from text.
    
    Args:
        text: Input text
        max_keywords: Maximum number of keywords to extract
        
    Returns:
        List of keywords
    """
    # This is a simple implementation that could be enhanced with NLP libraries
    # Remove punctuation and convert to lowercase
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove common stop words (a very basic list)
    stop_words = {'a', 'an', 'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'like', 'from'}
    
    words = text.split()
    keywords = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_counts = {}
    for word in keywords:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    
    # Sort by frequency and return top keywords
    sorted_keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_keywords[:max_keywords]]
