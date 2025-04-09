from google import genai
from dotenv import load_dotenv
import os
import base64
from PIL import Image
from io import BytesIO

load_dotenv()

def run_vision_agent(image_base64: str, text: str, chat_history: list):
    """
    Processes the image using the Vision Agent with conversational context.

    Args:
        image_base64 (str): Base64-encoded image string.
        text (str): Additional text input.
        chat_history (list): List of previous exchanges in the conversation.

    Returns:
        str: The response from the Vision Agent.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Decode the base64 image if provided
    image = None
    if image_base64:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))

    # Format chat history
    history = "\n".join([f"User: {q}\nAgent: {a}" for q, a in chat_history])

    # Stream response from Gemini
    prompt = f"""
You are a vision assistant specializing in property issue detection and troubleshooting.

[Conversation History]
{history}

[User Input]
Text: {text}
Image: {'[Image Provided]' if image else '[No Image Provided]'}

Responsibilities:
- Detect visible issues in the property (e.g., water damage, mold, cracks, poor lighting, broken fixtures).
- Provide troubleshooting suggestions, such as:
  - "You might need to contact a plumber."
  - "This looks like paint peeling due to moisture—consider using the anti-damp coating."
- Ask clarifying follow-up questions if the issue is unclear.

Respond based on the context of the conversation.
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, image] if image else [prompt],
    )

    return response.text.strip()
