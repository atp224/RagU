from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from openai import OpenAI
import pandas as pd


file_path = 'menu.csv'
data = pd.read_csv(file_path)
csv_string = data.to_string()

client = openai.OpenAI(api_key="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")

app = Flask(__name__)
CORS(app)

@app.route('/save_prompt', methods=['POST'])
def save_prompt():
    data = request.json
    user_prompt = data['prompt']

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Roleplay as a helpful server at a restaurant and answer any questions about the menu provided below in CSV format: {csv_string}"},
                {"role": "user", "content": user_prompt}
            ]
        )
        gpt_response = response.choices[0].message.content
    except Exception as e:
        gpt_response = f"An error occurred: {e}"

    return jsonify({'prompt': user_prompt, 'gpt_response': gpt_response})


if __name__ == '__main__':
    app.run(debug=True)
