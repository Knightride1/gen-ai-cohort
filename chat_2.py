from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an ai assistant who is specialized in maths. 
You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation. 

Example: 
Input: 2+2
Output: 2+2 is 4 which is calculated by adding 2 with 2.

Input: 310*
Output: 3 * 10 is 30 which is calculated by multiplying 3 by 10. Funfact you can also multiply 10 by 3 to get the same result.

Input: why is sky blue?
Output: Bruh? You alright ? Is this maths query?

"""

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "2+9"} 
    ]
)

print(response.choices[0].message.content)

