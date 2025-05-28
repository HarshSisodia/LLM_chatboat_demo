"""
Web interface for the LLM Chatbot.
This module provides a simple web interface using Flask.
"""

import os
from flask import Flask, render_template, request, jsonify
from app.chatbot import Chatbot

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Global chatbot instance
chatbot_instance = None

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Render the chat interface."""
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint for chat interactions."""
    if not request.json or 'message' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400
    
    user_message = request.json['message']
    response = chatbot_instance.generate_response(user_message)
    
    return jsonify({
        'response': response,
        'history': chatbot_instance.get_conversation_history()
    })

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """API endpoint to reset the conversation."""
    result = chatbot_instance.reset_conversation()
    return jsonify({'status': 'success', 'message': result})

def start_web_server(chatbot, host='0.0.0.0', port=8000, debug=False):
    """
    Start the web server.
    
    Args:
        chatbot: Chatbot instance
        host: Host to bind to
        port: Port to bind to
        debug: Whether to run in debug mode
    """
    global chatbot_instance
    chatbot_instance = chatbot
    
    print(f"Starting web server on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
