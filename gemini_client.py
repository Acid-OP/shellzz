# gemini_client.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from llm_file_generator import file_generator

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing. Ensure it's in .env and passed with --env-file")

genai.configure(api_key=api_key)

SYSTEM_INSTRUCTION = f"""You are AcidopShell AI Assistant - a helpful coding assistant integrated into a custom shell.
You can answer questions, explain concepts, and generate code files.

{file_generator.get_enhanced_prompt()}

Be concise but helpful. When generating files, always provide complete, working code.
You can provide explanations before or after the XML tags."""

model_with_files = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    system_instruction=SYSTEM_INSTRUCTION
)

model_regular = genai.GenerativeModel("gemini-2.0-flash-exp")


def ask_gemini(prompt: str):
    """
    Basic Gemini query - just returns the response text.
    Use this for simple Q&A without file generation.
    """
    try:
        response = model_regular.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {e}"


def ask_gemini_with_file_generation(query: str, project_dir: str = "."):
    """
    Enhanced Gemini query with automatic file generation.
    
    Args:
        query: The user's prompt
        project_dir: Directory where files should be created (default: current dir)
    
    Returns:
        tuple: (response_text, files_were_generated)
            - response_text: The full response from Gemini
            - files_were_generated: True if files were created, False otherwise
    """
    try:
        response = model_with_files.generate_content(query)
        response_text = response.text
        
        files_generated = file_generator.process_response(response_text, project_dir)
        
        return response_text, files_generated
        
    except Exception as e:
        return f"⚠️ Error: {e}", False