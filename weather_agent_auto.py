from urllib import response
from dotenv import load_dotenv
import requests
from openai import OpenAI
import os
import json

import requests

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# these are the actual tools that the ai can use to do things


def get_weather(city:str):
    # TODO and actual api call
    print("🛠️:  Tool called: get_weather:", city)
    url=f"https://wttr.in/{city}?format=%C+%t"
    response=requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

def run_command(command):
    result = os.system(command=command)
    return result



available_tools = {
    "get_weather": {
        "fn":get_weather,
        "description": "Takes a city name as an input and return the current weather for the city"
    },
    "run_command": {
        "fn":run_command,
        "description": "Takes a command as input to execute on system and returns the output"
    }
}
# this thing above is like a list of functions that can be called by the ai 
# or lets say that its the tool set that we are providing it in a bag 
# saying here's your tool bag now go and do work with it.


system_prompt = f"""
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
- get_weather: Takes a city name as an input and return the current weather for the city
- run_command: Takes a command as input to execute on system and returns the output.


Example:
User Query: What is the weather of New york?
Output: {{"step": "plan", "content": "The user is interested in the weather data of New York."}}
Output: {{"step": "plan", "content": "From the available tools I should call get_weather"}}
Output: {{"step": "action", "function": "get_weather","input": "New York"}}
Output: {{"step": "observe", "output": "12 degrees celsius"}}
Output: {{"step": "output", "content": "The weather for new york seems to be 12 degrees celsius"}}





"""
messages = [
    {"role": "system", "content": system_prompt}
]

while True: 
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type":"json_object"},
            messages=messages
        )
        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue
        if parsed_response.get("step") == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            if tool_name in available_tools:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role":"assistant","content": json.dumps({"step": "observe", "output": output})})
                continue
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break
