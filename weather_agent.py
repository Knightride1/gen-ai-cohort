from urllib import response
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def get_weather(city:str):
    # TODO and actual api call
    return "31 degrees celsius"

system_prompt = """
You are an helpful ai assistant who is speacialized in resolving user query.
You work on start, plan, action, observe mode.

For the given user query and available tools, plan the step by step execution.
Based on the planning, select the relevant tool from the available tools.
And based on the tool selection you perform an action to call the tool.
Wait for the observation and based on the observation from the tool call, resolve the user query.

Rules:
1. Follow the strict json output as per output schema 
2. Always perform one step at a time and wait for next input
3. Carefully analyze the user query.

Output JSON format: 
{{
    "step":"string",
    "content": "string",
    "function": "the name of the function if the step is the action",
    "input": "The input parameter for the function"
}}

Available Tools:




Example:
User Query: What is the weather of New york?
Output: {{"step": "plan", "content": "The user is interested in the weather data of New York."}}
Output: {{"step": "plan", "content": "From the available tools I should call get_weather"}}
Output: {{"step": "action", "function": "get_weather","input": "New York"}}
Output: {{"step": "observe", "output": "12 degrees celsius"}}
Output: {{"step": "output", "content": "The weather for new york seems to be 12 degrees celsius"}}





"""



response=client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format={"type":"json_object"},
    messages=[
        {"role": "system", "content": system_prompt},
        {"role":"user","content": "what is the current weather of patiala?"},
        # start filling ai response data from here in the format of 
        # {"role": "assistant", "content": json.dumps( and the response here)}
        
    ]
)

print(response.choices[0].message.content)