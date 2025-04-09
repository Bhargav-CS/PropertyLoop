from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from agents.faq_agent import run_faq_agent
from agents.vision_agent import run_vision_agent
from dotenv import load_dotenv  # Import load_dotenv
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
            """You are a routing agent. Decide whether the user input should be handled by the FAQ agent or the Vision agent.
Input Text: {text}
Image Uploaded: {has_image}

Respond with only one word: 'faq' or 'image'."""
        )


    def _auto_route(self, text: str, image_base64: str):
        has_image = "yes" if image_base64 else "no"

        chain = self.prompt | llm
        decision = chain.invoke({"text": text or "None", "has_image": has_image})
        decision = decision.content.strip().lower()

        if decision == "faq":
            print(f"[ROUTING] FAQ agent selected for text: {text}")
            return run_faq_agent(text)
            # return "Routing to FAQ agent."
        elif decision == "image":
            print(f"[ROUTING] Vision agent selected for image.")
            return run_vision_agent(image_base64, text)
            # return "Routing to Vision agent."
        else:
            return f"Unable to route request. Got decision: {decision}"

routeragent = RouterAgent()
