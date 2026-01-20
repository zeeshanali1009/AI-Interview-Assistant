import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("🚨 GROQ_API_KEY not found in .env file!")

client = Groq(api_key=api_key)

def get_answer(question, context):
    prompt = f"""
    You are an expert AI career assistant.
    The user is preparing for an interview.

    Context:
    {context[:2000]}

    Question:
    {question}

    Provide a professional and concise sample answer.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert AI interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
