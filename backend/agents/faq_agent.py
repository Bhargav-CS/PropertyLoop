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
def run_faq_agent(query: str, chat_history: list):
    """
    Handles FAQ queries with conversational context.

    Args:
        query (str): User's query.
        chat_history (list): List of previous exchanges in the conversation.

    Returns:
        str: The agent's response.
    """
    # Format chat history
    history = "\n".join([f"User: {q}\nAgent: {a}" for q, a in chat_history])

    prompt = f"""
You are a helpful assistant answering questions based on the following FAQ content.

[FAQ CONTENT]
{faq_data}

[Conversation History]
{history}

[User Question]
{query}

If the answer is not directly available in the FAQ,
try to answer with the best of you ability.
If you can’t find an exact answer, say "I’m not sure" or "I don’t know".
If the question is not related to the FAQ content, say "I can’t help with that. The issue is not listed in the FAQ".
handle the greetings and farewells politely.
"""
    response = llm.invoke(prompt)
    return response.content
