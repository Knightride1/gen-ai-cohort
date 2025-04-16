import json
from urllib import response
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# client = OpenAI(
#     api_key=os.getenv("OPENROUTER_API_KEY"),
#     base_url="https://openrouter.ai/api/v1"  # OpenRouter's endpoint
# )


system_prompt = """
You are an Ai assistant who is expert in breaking down complex problems and then resolve the user query

For the given user input, analyze the input and break down the problem step by step.
Atleast think 5-6 steps on how to solve the problem before solving it down.

The steps are you get a user input, you analyze, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving the final result.

Follow these steps in sequence that is "analyze", "think", "output", "validate", "result"

Rules:
1. Follow the strict json output as per output schema 
2. Always perform one step at a time and wait for next input
3. Carefully analyze the user query.

Output Format:
{{step: "string", content: "string"}}

Example:
Input: 2+2
Output: {{step: "analyze", content: "Alright the user is interested in maths query and he is asking a basic arithmatic operation"}}
Output: {{step: "think", content: "To perform the addition i must go from left to right and add all the operands"}}
Output: {{step: "output", content: "4"}}
Output: {{step: "validate", content: "Seems like 4 is correct answer for 2+2 "}}
Output: {{step: "Result", content: "2+2 = 4 and that is calculated by adding all numbers "}}



"""
messages = [
    {"role": "system", "content": system_prompt}
]


query = input("> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_format={"type":"json_object"},
        messages=messages
    )
    content = response.choices[0].message.content
    parsed_response = json.loads(content)
    messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

    if parsed_response.get("step") != "output":
        print(f"🧠: {parsed_response.get("content")}")

        continue
    print(f"🤖: {parsed_response.get("content")}")
    break
