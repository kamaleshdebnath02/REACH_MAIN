import spacy
import json
import pdfplumber
import requests
from bs4 import BeautifulSoup
import random
import re
import wikipediaapi
import os
from intent import extract_main_topic 

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

# Load intents from JSON file
def load_intents():
    with open('intents.json', 'r') as file:
        return json.load(file)

intents = load_intents()

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='REACH AI Health Chatbot/1.0 (kamdn.69@gmail.com)')

# Global dictionary to store user information
user_memory = {}

# User data file path
USER_DATA_FILE = 'user_data.json'

def load_user_data():
    """ Load user data from file """
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_user_data():
    """ Save user data to file """
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(user_memory, file)

# Load user data at startup
user_memory.update(load_user_data())

def preprocess_text(text):
    """ Preprocess the text for better matching """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def find_intent_and_response(preprocessed_message, user_id):
    """ Find the best matching intent and response for the given message """
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            preprocessed_pattern = preprocess_text(pattern)
            if re.search(preprocessed_pattern, preprocessed_message):
                response = random.choice(intent['responses'])
                image_path = intent.get('image', None)
                
                # Insert user's name into response if available
                if user_id in user_memory and 'name' in user_memory[user_id]:
                    response = response.replace('{name}', user_memory[user_id]['name'])
                
                return response, image_path

    # No intent matched, return None to indicate default handling
    return None, None



def fetch_wikipedia_summary(query, user_id=None):
    """ Fetch a personalized, concise summary from Wikipedia based on the query """
    page = wiki_wiki.page(query)
    if page.exists():
        # Extract the first few sentences to keep the summary concise
        summary = page.summary.split('.')[:5]  # Get the first 5 sentences
        summary = '. '.join(summary) + '.'  # Reassemble the summary

        # Personalize the summary if the user's name is known
        if user_id in user_memory and 'name' in user_memory[user_id]:
            summary = f"{user_memory[user_id]['name']}, here's what I found about {query}: {summary}"
        else:
            summary = f"Here's what I found about {query}: {summary}"

        return summary
    else:
        return "I couldn't find any information on that topic."

def process_message(message, user_id):
    """ Process incoming messages using spaCy to extract intents based on entities recognized and matching patterns from intents. """
    preprocessed_message = preprocess_text(message)
    doc = nlp(preprocessed_message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Check for user's name and store it in memory
    name_recognized = False
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            user_memory[user_id] = {'name': ent.text}
            name_recognized = True

    # Prioritize the name recognition intent
    if name_recognized:
        response = f"Nice to meet you, {user_memory[user_id]['name']}!"
        save_user_data()
        return response, entities, None

    response, image_path = find_intent_and_response(preprocessed_message, user_id)
    if not response:
        # Extract main topic and fetch from Wikipedia if intent doesn't match
        main_topic = extract_main_topic(preprocessed_message)
        if main_topic:
            response = fetch_wikipedia_summary(main_topic, user_id)
        else:
            response = "I couldn't find any information on that topic."

    return response, entities, image_path

def fetch_response(message, user_id):
    """ Fetch a response based on the processed message. """
    try:
        response, entities, image_path = process_message(message, user_id)
        return {
            "response": response,
            "entities": entities,
            "image": image_path
        }
    except Exception as e:
        print(f"Error fetching response: {e}")
        return {
            "response": "I'm sorry, I encountered an error while processing your request.",
            "entities": [],
            "image": None
        }

def read_health_info(file_path):
    """ Read health awareness information from a text file. """
    try:
        with open(f'backend/data/{file_path}', 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading health info from text file: {e}")
        return "I couldn't retrieve the health information from the text file."

def read_pdf_health_info(file_path):
    """ Read health awareness information from a PDF file. """
    try:
        with pdfplumber.open(f'backend/data/{file_path}') as pdf:
            first_page = pdf.pages[0]
            return first_page.extract_text()
    except Exception as e:
        print(f"Error reading health info from PDF file: {e}")
        return "I couldn't retrieve the health information from the PDF file."

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading text file: {e}")
        return "I couldn't retrieve the information from the text file."

def read_pdf_file(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            first_page = pdf.pages[0]
            return first_page.extract_text()
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return "I couldn't retrieve the information from the PDF file."

def fetch_web_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except Exception as e:
        print(f"Error fetching web data: {e}")
        return "I couldn't retrieve the information from the web3."
