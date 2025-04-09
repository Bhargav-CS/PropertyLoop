from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from agents.faq_agent import run_faq_agent
from agents.vision_agent import run_vision_agent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class RouterAgent:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template(
            """You are a routing agent. Based on the query and conversation history, decide whether the query should be handled by the FAQ agent or the Vision agent.

[Conversation History]
{history}

[User Query]
{query}

if there are greetings route to 'faq' agent.
Respond with only one word: 'faq' or 'vision'. If the query is related to a previous image but no new image is provided, route to 'vision'.
If you are unsure about the routing decision, say 'unsure'.
"""
        )

    def route(self, query: str, image_base64: str, chat_history: list):
        # Format chat history
        history = "\n".join([f"User: {q}\nAgent: {a}" for q, a in chat_history])

        # Prepare routing decision
        decision_prompt = self.prompt.format(history=history, query=query)
        decision = llm.invoke(decision_prompt).content.strip().lower()

        # Route to the appropriate agent
        if decision == "faq":
            print(f"[ROUTING] FAQ agent selected for query: {query}")
            return run_faq_agent(query=query, chat_history=chat_history)
        elif decision == "vision":
            print(f"[ROUTING] Vision agent selected for query: {query}")
            return run_vision_agent(image_base64=image_base64, text=query, chat_history=chat_history)
        else:
            return f"Unable to route request. Got decision: {decision}"

routeragent = RouterAgent()
