import openai
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv('secrets.env')
keys = os.getenv("API_KEY")

client = openai.OpenAI(api_key=keys)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a culinary master."},
    {"role": "user", "content": "Describe the difference between bok choy and chinese broccoli."}
  ]
)
print(completion.choices[0].message)