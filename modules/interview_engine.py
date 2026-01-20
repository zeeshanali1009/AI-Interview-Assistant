import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load from .env file
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("🚨 GROQ_API_KEY not found in .env file!")

client = Groq(api_key=api_key)

def generate_interview_questions(resume_text, jd_text):
    prompt = f"""
    You are an expert interviewer. Based on the following resume and job description,
    generate 5 personalized technical and behavioral interview questions.

    Resume:
    {resume_text[:2000]}

    Job Description:
    {jd_text[:2000]}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a professional technical interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.split("\n")
