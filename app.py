from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import openai
import os

# Remove this line: from config import OPENAI_API_KEY

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Correctly retrieve the environment variable
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = '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'

# Set the API key for the 'openai' library
openai.api_key = OPENAI_API_KEY

# working API key check
if openai.api_key is None:
    raise ValueError("Missing OpenAI API key! Please set the OPENAI_API_KEY environment variable.")

# This list will hold the conversation.
# Note: In a production environment, you might want to replace this with a more robust solution for handling multiple users/sessions.
messages = [{"role": "system", "content": "You are a software developer recruting professional"}]

@app.route('/', methods=['GET'])
def home():
    # Render the HTML page. It will show the form.
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Get the user input from the POST request body
        # data = request.get_json()
        user_input = request.json['user_input']
        
        # Add the user's message to the conversation
        messages.append({"role": "user", "content": user_input})

        # This is the OpenAI GPT-3 engine deciding on its response.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        chatGPT_reply = response['choices'][0]['message']['content']
        
        # Add the assistant's reply to the conversation
        messages.append({"role": "assistant", "content": chatGPT_reply})
        
        # Send the reply as a JSON response
        return jsonify({'reply': chatGPT_reply})

    except Exception as e:
        # If an error occurs, print it to the console (you can also log it to a file)
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)

