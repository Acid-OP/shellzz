# gemini_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing. Ensure it's in .env and passed with --env-file")

# Configure Gemini
genai.configure(api_key=api_key)

def ask_gemini(prompt: str):
    try:
        # Use the GenerativeModel class
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"