from google import genai
from dotenv import load_dotenv
import os
import base64
from PIL import Image
from io import BytesIO

load_dotenv()

def run_vision_agent(image_base64: str, text: str):
    """
    Processes the image using the Vision Agent with streaming response.

    Args:
        image_base64 (str): Base64-encoded image string.
        text (str): Additional text input.

    Returns:
        str: The streamed response from the Vision Agent.
    """
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=GOOGLE_API_KEY)

    # Decode the base64 image
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data))

    # Stream response from Gemini
    response_stream = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[text, image],
    )

    full_response = ""
    for chunk in response_stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)  # Optional: live print in terminal
            full_response += chunk.text

    return full_response
