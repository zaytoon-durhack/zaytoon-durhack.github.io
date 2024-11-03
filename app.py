import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('energy_data.csv')

# Function to get response based on user input
def get_response(user_input):
    user_input = user_input.lower()

    # Simple keyword matching to find relevant data
    if "temperature" in user_input:
        location = extract_location(user_input)
        year = extract_year(user_input)
        month = extract_month(user_input)

        response = data[(data['Location'].str.lower() == location) & 
                        (data['Year'] == year) & 
                        (data['Month'] == month)]

        if not response.empty:
            temp = response['Temperature'].values[0]
            return f"The temperature in {location.title()} in {month} {year} was {temp}°F."
        else:
            return "Sorry, I couldn't find temperature data for that location."

    elif "humidity" in user_input:
        location = extract_location(user_input)
        year = extract_year(user_input)
        month = extract_month(user_input)

        response = data[(data['Location'].str.lower() == location) & 
                        (data['Year'] == year) & 
                        (data['Month'] == month)]

        if not response.empty:
            humidity = response['Humidity'].values[0]
            return f"The humidity in {location.title()} in {month} {year} was {humidity}%. "
        else:
            return "Sorry, I couldn't find humidity data for that location."

    elif "energy consumption" in user_input:
        location = extract_location(user_input)
        year = extract_year(user_input)

        response = data[(data['Location'].str.lower() == location) & 
                        (data['Year'] == year)]

        if not response.empty:
            consumption = response['Energy Consumption'].values[0]
            return f"The energy consumption in {location.title()} in {year} was {consumption} units."
        else:
            return "Sorry, I couldn't find energy consumption data for that location."

    return "I'm sorry, I don't understand your request."

# Helper functions to extract location, year, and month from the user input
def extract_location(user_input):
    # This is a simple keyword matching; this can be improved for better NLP
    locations = data['Location'].str.lower().unique()
    for loc in locations:
        if loc in user_input:
            return loc
    return ""

def extract_year(user_input):
    for word in user_input.split():
        if word.isdigit() and 2000 <= int(word) <= 2100:
            return int(word)
    return 2020  # Default year if no year is found

def extract_month(user_input):
    months = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }
    for month in months:
        if month in user_input:
            return months[month]
    return 1  # Default month if no month is found

@app.route('/')
def home():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat_api():
    user_input = request.json.get('message')
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
