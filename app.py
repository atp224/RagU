from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import pandas as pd

import sqlite3
import json

from dotenv import load_dotenv
import os

load_dotenv('secrets.env')
keys = os.getenv("API_KEY")

client = openai.OpenAI(api_key=keys)

file_path = 'menu.csv'
data = pd.read_csv(file_path)
csv_string = data.to_string()

client = openai.OpenAI(api_key=keys)

app = Flask(__name__)
CORS(app)

messages = []

@app.route('/save_prompt', methods=['POST'])
def save_prompt():
    global messages
    data = request.json
    user_prompt = data['prompt']

    messages.append({"role": "user", "content": user_prompt})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages + [
                {"role": "system", "content": f"Roleplay as a helpful server at a restaurant and answer any questions about the menu provided below in CSV format: {csv_string} and also knowledgable about the previous conversation history in {messages} but only answer the most recent question that is at the end of the list"},
                {"role": "user", "content": user_prompt}
            ]
        )
        gpt_response = response.choices[0].message.content
        messages.append({"role": "system", "content": gpt_response})
    except Exception as e:
        gpt_response = f"An error occurred: {e}"

    return jsonify({'prompt': user_prompt, 'gpt_response': gpt_response})


if __name__ == '__main__':
    app.run(debug=True)
