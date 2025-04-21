import os
import time
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})  # In production, restrict to specific origins

# Ensure the OpenAI API key is set
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY environment variable not set")

# Load assistant ID from file or use default
try:
    with open('assistant.json', 'r') as file:
        assistant_data = json.load(file)
        ASSISTANT_ID = assistant_data['assistant_id']
except (FileNotFoundError, json.JSONDecodeError, KeyError):
    # Default to the ID in the original code if file can't be read
    ASSISTANT_ID = 'asst_8VzDeD0GOmnLU2StbnWYFwyd'
    print(f"Using default Assistant ID: {ASSISTANT_ID}")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://api.openai.com/v1") 

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/quiz.html')
def serve_quiz():
    return send_from_directory(app.static_folder, 'quiz.html')

# Start the quiz
@app.route('/start', methods=['POST'])
def start_quiz():
    data = request.json
    test_name = data.get('test')
    
    if not test_name:
        return jsonify({"error": "Test name is required"}), 400
    
    initial_message = f"The user has selected the {test_name}. Please start the {test_name} and provide the first question with options."
    
    try:
        # Create a new thread
        thread = client.beta.threads.create()
        
        # Add the initial message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=initial_message
        )
        
        # Create a run to process the message
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )
        
        # Poll for run completion
        max_attempts = 30
        attempts = 0
        while attempts < max_attempts:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return jsonify({"error": f"Run {run_status.status}: {run_status.last_error}"}), 500
            
            attempts += 1
            time.sleep(1)
        
        if attempts >= max_attempts:
            return jsonify({"error": "Timeout waiting for assistant response"}), 504
        
        # Retrieve messages
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        
        # Get the assistant's response (the most recent message from the assistant)
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        if not assistant_messages:
            return jsonify({"error": "No response from assistant"}), 500
        
        # Get the content from the most recent assistant message
        latest_message = assistant_messages[0]
        content_parts = [part for part in latest_message.content if part.type == "text"]
        if not content_parts:
            return jsonify({"error": "No text content in assistant response"}), 500
        
        response_text = content_parts[0].text.value
        
        # Parse the response to extract question and options
        lines = response_text.strip().split('\n')
        question = lines[0] if lines else ""
        options = [line for line in lines[1:] if line.strip()]
        
        return jsonify({
            "thread_id": thread.id,
            "question": question,
            "options": options,
            "full_response": response_text  # Include full response for debugging
        })
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Process the quiz responses
@app.route('/quiz', methods=['POST'])
def process_quiz():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')
    
    if not thread_id:
        return jsonify({"error": "Thread ID is required"}), 400
    
    if not user_input:
        return jsonify({"error": "User message is required"}), 400
    
    try:
        # Add the user's message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )
        
        # Create a run to process the message
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID
        )
        
        # Poll for run completion
        max_attempts = 30
        attempts = 0
        while attempts < max_attempts:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                return jsonify({"error": f"Run {run_status.status}: {run_status.last_error}"}), 500
            
            attempts += 1
            time.sleep(1)
        
        if attempts >= max_attempts:
            return jsonify({"error": "Timeout waiting for assistant response"}), 504
        
        # Retrieve messages
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        
        # Get the assistant's response (the most recent message from the assistant)
        assistant_messages = [msg for msg in messages.data if msg.role == "assistant"]
        if not assistant_messages:
            return jsonify({"error": "No response from assistant"}), 500
        
        # Get the content from the most recent assistant message
        latest_message = assistant_messages[0]
        content_parts = [part for part in latest_message.content if part.type == "text"]
        if not content_parts:
            return jsonify({"error": "No text content in assistant response"}), 500
        
        response_text = content_parts[0].text.value
        
        # Parse the response to extract question and options
        lines = response_text.strip().split('\n')
        question = lines[0] if lines else ""
        options = [line for line in lines[1:] if line.strip()]
        
        # Check if this is a results message (no options)
        is_results = len(options) < 2
        
        return jsonify({
            "question": question,
            "options": options,
            "is_results": is_results,
            "full_response": response_text  # Include full response for debugging
        })
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "assistant_id": ASSISTANT_ID})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
