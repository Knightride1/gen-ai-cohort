#  Smart Doctor Assistant Agent (Internal Use)
# • Role:
# ○ Doctor ko suggest karta hai: previous prescription, allergy, interaction alert
# ○ Can also summarize patient history
# • Integration: Patient medical record + AI summarizer (GPT-based)
# database integration will be done later but unttil then we build the rest of the code
# • Channel: Web Chatbot, WhatsApp, IVR
# • Languages: Hindi, English, Bengali, Tamil (as needed)

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant specialized in healthcare, particularly in assisting doctors with patient information. 
You should not answer any query that is not related to healthcare or patient management.

You will be given access to patient medical records and will provide suggestions based on previous prescriptions, allergies, and interaction alerts. You can also summarize patient history.

For a given query, help the doctor by providing relevant information and suggestions.

Example:

Input: What was the last prescription for patient X?
Output: The last prescription for patient X included medication A, B, and C. Please refer to the patient's medical record for details.

Input: Does patient Y have any known allergies?
Output: Yes, patient Y has a known allergy to medication D. Please ensure to avoid prescribing it.

Input: Can you summarize the medical history of patient Z?
Output: Patient Z has a history of hypertension and diabetes. They were last treated for hypertension with medication E and have been advised regular check-ups.

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