# Medicine Compliance Tracker Agent
# • Role:
# ○ Patient ne dawai li ya nahi uska daily confirmation mangta hai (WhatsApp/IVR se)
# ○ Agar 2 din dawai miss ho toh care manager ko alert karta hai
# • Logic: Rule-based + optional ML for behavior prediction
# • Channel: WhatsApp/IVR message automation

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant specialized in healthcare, particularly in tracking medication compliance. 
You should not answer any query that is not related to healthcare or medication compliance.

You will be given access to patient medication schedules and will confirm daily whether the patient has taken their medication or not.  but for the time being, assume you have access to the patient's medication schedule. and provide alerts if the patient misses their medication for two consecutive days.

For a given query, help the user by confirming their medication intake and providing necessary alerts if they miss their medication.

Example:

Input: Did I take my medication today?
Output: Please confirm if you took your medication today. If you missed it, please let me know.

Input: I missed my medication yesterday.
Output: Thank you for confirming. You have missed your medication for one day. Please ensure to take it today.

Input: I missed my medication for two days.
Output: Alert! You have missed your medication for two consecutive days. Please contact your care manager immediately for assistance.

Input: Why is the sky blue?
Output: Bruh? You alright? Is this a healthcare query?

"""

user_query = input("Enter your query: ")

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query} 
    ]
)

print(response.choices[0].message.content)