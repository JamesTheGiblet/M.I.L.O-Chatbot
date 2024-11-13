# chatbot_core.py

import json
import random
import nltk
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources (if not already downloaded)
nltk.download('punkt')


def process_input(user_comment):
    """Processes user input to identify potentially multiple keywords."""
    user_comment = user_comment.lower()
    intents = []

    if any(word in ['hi', 'hello', 'hey'] for word in user_comment.split()):
        intents.append("greeting")
    if 'how are you' in user_comment:
        intents.append("how_are_you")
    if any(word in ['bye', 'goodbye', 'see', 'ya', 'later'] for word in user_comment.split()):
        intents.append("goodbye")
    if any(word in ['thank', 'thanks', 'thx'] for word in user_comment.split()):
        intents.append("thanks")

    # More specific keywords for "about_me"
    if any(word in ['name', 'called', 'milo', 'stand', 'for', 'about'] for word in user_comment.split()):
        intents.append("about_me")

    if any(word in ['help', 'can', 'do', 'what'] for word in user_comment.split()):
        intents.append("help")
    if any(word in ['weather', 'like', 'outside'] for word in user_comment.split()):
        intents.append("weather")
    if any(word in ['time', 'now', 'oclock'] for word in user_comment.split()):
        intents.append("time")
    if any(word in ['cool', 'awesome', 'great', 'good', 'nice', 'fantastic'] for word in user_comment.split()):
        intents.append("compliment")
    if any(word in ['bad', 'terrible', 'stupid', 'dumb'] for word in user_comment.split()):
        intents.append("insult")
    # Add more intent keywords here...

    if not intents:
        intents.append("unknown")
    return intents


def load_responses(filename="reply.json"):
    """Loads reply from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_responses(reply, filename="reply.json"):
    """Saves reply to a JSON file."""
    with open(filename, "w") as f:
        json.dump(reply, f, indent=4)


def generate_response(user_comment, reply, context):
    """Generates responses based on identified intents and context."""
    if user_comment in reply:
        return random.choice(reply[user_comment])
    else:
        intents = process_input(user_comment)
        responses = []
        for intent in intents:
            if intent in reply:
                # Basic contextual response (example)
                if intent == "greeting" and "goodbye" in context[-2:]:  # If user said goodbye recently
                    responses.append("You said goodbye just now. Are you back already?")
                else:
                    responses.extend(reply[intent])
        if responses:
            return random.choice(responses)
        else:
            return None  # Return None to trigger learning


def learn_new_response(user_comment, reply):
    """Learns a new response for a given input,
       and optionally asks a question to learn more.
    """
    new_reply = input(f"I don't know how to respond to that. What should I say to '{user_comment}'? ")
    reply[user_comment] = [new_reply]

    # Ask a question based on the user's comment (example)
    if "like" in user_comment and "?" in user_comment:  # If the user asked a question with "like"
        question = f"What do you like about {user_comment.split('like')[-1].strip()}?"
        print("M.I.L.O:", question)
        answer = input("You: ")
        reply[question] = [answer]  # Store the user's answer

    return new_reply
