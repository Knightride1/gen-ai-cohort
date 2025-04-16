from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta"
)

response = client.chat.completions.create(
    model="models/gemini-2.0-flash",
    messages=[
        {"role": "user", "content": "What is 2 + 2 * 0"} # Zero Shot Prompting
    ]
)

print(response.choices[0].message.content)



# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI()

# result = client.chat.completions.create(
#     model="gpt-4",
#     messages=[
#         { "role": "user", "content": "What is greator? 9.8 or 9.11" } # Zero Shot Prompting
#     ]
# )

# print(result.choices[0].message.content)