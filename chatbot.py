import os
import csv
import random
from weather_functions import get_weather, extract_city_from_input
from chatbot_personality import ChatbotPersonality

class Chatbot:
    def __init__(self, user_data_file='user_data.csv', learned_data_file='learned_data.csv', questions_file='questions.csv'):
        self.user_data_file = user_data_file
        self.learned_data_file = learned_data_file
        self.questions_file = questions_file
        self.load_user_data()
        self.load_learned_data()
        self.load_questions()
        self.personality = ChatbotPersonality()  # Initialize the personality module

    def load_user_data(self):
        self.user_data = {}
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        try:
                            self.user_data[row[0]] = eval(row[1])
                        except (SyntaxError, NameError):
                            self.user_data[row[0]] = {}

    def save_user_data(self):
        with open(self.user_data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for username, data in self.user_data.items():
                writer.writerow([username, data])

    def load_learned_data(self):
        self.learned_data = {}
        if os.path.exists(self.learned_data_file):
            with open(self.learned_data_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        self.learned_data[row[0]] = row[1]

    def save_learned_data(self):
        with open(self.learned_data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            for user_input, response in self.learned_data.items():
                writer.writerow([user_input, response])

    def load_questions(self):
        self.questions = []
        if os.path.exists(self.questions_file):
            with open(self.questions_file, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.questions.append(row[0])

    def get_response(self, user_input):
        # Check if the user is asking about the weather
        if "weather" in user_input.lower():
            city = extract_city_from_input(user_input)
            if city:
                weather_data = get_weather(city)
                if weather_data:
                    return f"The weather in {city} is {weather_data['description']} with a temperature of {weather_data['temperature']} degrees Celsius."
                else:
                    return "I couldn't get the weather information for that city."

        response = self.learned_data.get(user_input)
        if response:
            return response
        return "I don't know how to respond to that yet. Can you teach me?"


    def learn_response(self, user_input, user_response):
        self.learned_data[user_input] = user_response
        self.save_learned_data()

    def chat(self):
        print(self.personality.get_greeting())  # Use a personalized greeting
        user_name = input("You: ").strip()

        if user_name in self.user_data:
            print(f"Welcome back, {user_name}! How can I assist you today?")
        else:
            print(f"Nice to meet you, {user_name}! How can I assist you today?")
            self.user_data[user_name] = {}
            self.save_user_data()

        question_count = 0

        while True:
            user_input = input(f"{user_name}: ").strip()
            if user_input.lower() == 'exit':
                print(self.personality.get_farewell())  # Use a personalized farewell
                break

            response = self.get_response(user_input)
            # Use the personality module to add variation
            print(f"M.I.L.O.: {self.personality.add_variation(response, user_name)}")  
            if response == "I don't know how to respond to that yet. Can you teach me?":
                user_response = input(f"{user_name}: ").strip()
                self.learn_response(user_input, user_response)
                print("Thanks! I've learned something new.")

            # Suggest topics if the conversation lulls 
            if user_input.lower() in ["ok", "okay", "hmm", "yeah"]:  
                suggestions = [
                    "What's your favorite hobby?",
                    "Have you seen any good movies lately?",
                    "What do you think about [current event]?"
                ]
                suggestion = random.choice(suggestions)
                print(f"M.I.L.O.: {suggestion}")

            # Check for preference expressions
            if "I like" in user_input:
                preference_type, preference_value = self.extract_preference(user_input)
                if preference_type and preference_value:
                    self.personality.learn_preference(user_name, preference_type, preference_value)
                    print(f"M.I.L.O.: I'll remember that you like {preference_value} {preference_type}.")

            # Ask questions every 3 responses
            question_count += 1
            if question_count >= 3:
                question_count = 0
                if self.questions:
                    question = random.choice(self.questions)
                    print(f"M.I.L.O.: {question}")
                    user_answer = input(f"{user_name}: ").strip()
                    self.user_data[user_name][question] = user_answer
                    self.save_user_data()
                else:
                    print("M.I.L.O.: I've run out of questions to ask!")


    def extract_preference(self, user_input):
        # Basic preference extraction (you'll need to improve this)
        try:
            # Example: "I like using 😊 emojis"
            parts = user_input.split()
            if len(parts) >= 4 and parts[0] == "I" and parts[1] == "like" and parts[2] == "using":
                preference_type = "emojis"
                preference_value = parts[3]
                return preference_type, preference_value
        except ValueError:  # Catch specific exception if possible
            print("Error extracting preference: Invalid input format.")
        except IndexError:
            print("Error extracting preference: Input too short.")
        except Exception as e:  # Catch general exceptions for unexpected errors
            print(f"An unexpected error occurred: {e}")
        return None, None

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
