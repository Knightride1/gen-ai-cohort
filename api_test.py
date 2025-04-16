# from json import load
# import dotenv
# from together import Together
from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

response = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct",
    messages=[{"role": "user", "content": "What are some fun things to do in New York?"}]
)
print(response.choices[0].message.content)