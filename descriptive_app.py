# Importing necessary classes and functions from the flask package.
from flask import Flask, request, render_template, jsonify

# Importing the CORS module to handle Cross-Origin Resource Sharing, allowing the client to interact with the server from a different domain.
from flask_cors import CORS

# Importing the openai library, which provides the Python client for the OpenAI API.
import openai

# Importing os for operating system related functionalities, particularly for reading environment variables.
import os

# Initializes a Flask object, "__name__" is a predefined setup, which provides the name of the script as the starting point for Flask.
app = Flask(__name__)

# Setting up Cross-Origin Resource Sharing (CORS) for the Flask app. This allows the server to accept requests from different domains, specifically from "http://localhost:3000" here.
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Retrieving the OpenAI API key from the system's environment variable. It's a secure way to use sensitive information without hardcoding it into the script.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Assigning the retrieved API key to the openai library configuration; this is necessary for making authenticated requests to the OpenAI API.
# api_key is an attribute of openai
openai.api_key = OPENAI_API_KEY

# An immediate check to see if the API key is not set (None). If it's missing, the script raises a ValueError to alert the user to set the API key, halting the server's execution.
if openai.api_key is None:
    raise ValueError("Missing OpenAI API key! Please set the OPENAI_API_KEY environment variable.")

# Initializing a list that will store the conversation messages. In a real-world scenario, consider using more complex data handling (like a database) to support multiple users or persist conversations.
messages = [{"role": "system", "content": "You are a software developer"}]

# A route for the root of the app, responding to GET requests. When users access the root URL, they receive the rendered 'index.html' page.
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# A route handling POST requests sent to '/get_response'. This endpoint is where the user input is sent, and from where the script responds after processing the conversation with GPT-3.
@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Extracting 'user_input' from the JSON body of the POST request. This is what the user types into the chat on the client side.
        user_input = request.json['user_input']
        
        # Appending the user's message to the 'messages' list. It keeps the conversation flow that will be sent to GPT-3 for context.
        messages.append({"role": "user", "content": user_input})

        # Making a request to the OpenAI API. The 'ChatCompletion.create' function sends the conversation history to the GPT-3 model, prompting it to generate a response based on the provided context.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # specifying which GPT-3 model to use
            messages=messages       # the conversation context
        )

        # Extracting GPT-3's response text from the API's reply. This text will be the model's continuation of the conversation, based on the input and context provided.
        chatGPT_reply = response['choices'][0]['message']['content']
        
        # Appending GPT-3's response to the 'messages' list to continue building the conversation history.
        messages.append({"role": "assistant", "content": chatGPT_reply})
        
        # Sending back GPT-3's response in JSON format. This is the response that the server sends back to the client's POST request.
        return jsonify({'reply': chatGPT_reply})

    except Exception as e:
        # Basic error handling: if any step within the try block fails, this script prints the error message, and the server responds with a JSON object indicating an internal server error (HTTP 500).
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500

# A conditional check for whether this script is the main program being executed. If it is, Flask's development server starts, listening on port 3000, with debug mode enabled.
if __name__ == '__main__':
    app.run(port=3000, debug=True)
