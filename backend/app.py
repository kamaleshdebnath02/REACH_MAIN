from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import spacy
from googletrans import Translator
import wikipediaapi
from chat_engine import fetch_response, read_text_file, read_pdf_file, fetch_web_data, read_health_info, read_pdf_health_info, user_memory, save_user_data
import os
import time
import subprocess
import tempfile

# Initialize Flask app and CORS
app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize translator
translator = Translator()

# Wikipedia API setup with a user agent
user_agent = "REACH AI Health Chatbot/1.0 (kamdn.69@gmail.com)"
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent=user_agent)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    user_id = data.get('user_id')  # Get the user ID from the request data

    if message:
        response = fetch_response(message, user_id)
    else:
        response = {"response": "Please provide a message for response.", "entities": []}
    return jsonify(response)

@app.route('/fetch-health-info', methods=['GET'])
def fetch_health_info():
    text_info = read_health_info("health_awareness.txt")
    return jsonify({"health_info": text_info})

@app.route('/fetch-health-pdf', methods=['GET'])
def fetch_health_pdf():
    pdf_info = read_pdf_health_info("health_awareness_book.pdf")
    return jsonify({"health_info": pdf_info})

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    lang = data.get('lang', 'en')  # Default to English
    retries = 3
    for i in range(retries):
        try:
            translation = translator.translate(text, dest=lang)
            return jsonify({'translated_text': translation.text})
        except Exception as e:
            print(f"Translation error: {e}")
            time.sleep(2)  # Wait for 2 seconds before retrying
    return jsonify({'translated_text': 'Error: Could not translate message.'}), 500

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('../frontend/public/images', filename)

@app.route('/save-user-data', methods=['POST'])
def save_user_data_route():
    """ Route to save user data to file """
    try:
        save_user_data()
        return jsonify({"message": "User data saved successfully"}), 200
    except Exception as e:
        print(f"Error saving user data: {e}")
        return jsonify({"message": "Error saving user data"}), 500





@app.route('/send-whatsapp', methods=['POST'])
def send_whatsapp():
    data = request.json
    phone = str(data.get('phone')).strip()
    message = str(data.get('message')).strip()

    # Ensure phone number starts with '+'
    if not phone.startswith("+"):
        return jsonify({"error": "Phone number must include country code with '+'"}), 400

    # Log the received data
    print(f"Received phone: {phone}")
    print(f"Received message: {message}")

    if not phone or not message:
        return jsonify({"error": "Phone number or message is missing"}), 400

    try:
        # Create a temporary file to hold the message content
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
            temp_file.write(message)
            temp_file_path = temp_file.name

        # Full path to the Python interpreter
        python_path = r'B:\\PROJECTS\Assam University\\REACH\AI chatbot\backend\\venv\Scripts\\python.exe'

        # Full path to the whatsapp_sender.py script
        script_path = r'B:\\PROJECTS\Assam University\\REACH\AI chatbot\backend\whatsapp_sender.py'

        # Use subprocess to call the whatsapp_sender.py script
        command = [python_path, script_path, phone, temp_file_path]
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Remove the temporary file after sending the message
        os.remove(temp_file_path)

        return jsonify({"message": f"Message sending initiated to {phone}"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to send message: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)

