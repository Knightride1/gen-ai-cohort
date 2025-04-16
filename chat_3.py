import json
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta"
)
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
response = client.chat.completions.create(
    model="models/gemini-2.0-flash",
    response_format={"type":"json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is 3+4*5"},
        {"role": "assistant", "content": json.dumps({"step": "analyze", "content": "The user is asking to evaluate the expression '3+4*5'. This involves addition and multiplication. Need to consider operator precedence."})},
        {"role": "assistant", "content": json.dumps({"step": "think", "content": "According to the order of operations (PEMDAS/BODMAS), multiplication should be performed before addition. So, first calculate 4*5, and then add 3 to the result."})},
        {"role": "assistant", "content": json.dumps({
  "step": "output",
  "content": "23"
})},
{"role": "assistant", "content": json.dumps({
"step": "validate",
"content": "Let's verify the answer. 4 * 5 = 20, and 3 + 20 = 23.  The calculation seems correct."
})},
{"role": "assistant", "content": json.dumps({
"step": "result",
"content": "3 + 4 * 5 = 3 + (4 * 5) = 3 + 20 = 23. The result is 23 due to multiplication taking precedence over addition."
})}
    ]
)

print(response.choices[0].message.content)