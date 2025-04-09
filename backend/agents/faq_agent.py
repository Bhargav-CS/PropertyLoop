# agents/faq_agent.py

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv  # Import load_dotenv

load_dotenv()  # Load environment variables from .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DOC_PATH = "faq_data/faq.txt"

# --- Load the FAQ content ---
def load_faq_content():
    try:
        with open(DOC_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "FAQ content is currently unavailable."

faq_data = load_faq_content()

# --- Gemini LLM setup ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

# --- Exposed function ---
def run_faq_agent(query: str):
    prompt = f"""
You are a helpful assistant answering questions based on the following FAQ content.

[FAQ CONTENT]
{faq_data}

[User Question]
{query}

If the answer is not directly available in the FAQ, say "Sorry, I couldn’t find an exact answer in the FAQ."
"""
    response = llm.invoke(prompt)
    return response.content
