import openai
from openai import OpenAI
client = openai.OpenAI(api_key="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")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a culinary master."},
    {"role": "user", "content": "Describe the difference between bok choy and chinese broccoli."}
  ]
)
print(completion.choices[0].message)