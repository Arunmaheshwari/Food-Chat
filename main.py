# main.py
import google.generativeai as genai
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Function to configure Gemini API with the API key directly
def configure_genai():
    # Get the API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key is None:
        raise ValueError("API key not found in .env file")
    
    genai.configure(api_key=api_key)

# Function to create model with generation config
def create_model():
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )
    return model

# Function to start chat session
def start_chat_session(model):
    chat_session = model.start_chat(
        history=[
          {
            "role": "user",
            "parts": [
                "gemini i will provide you image of food and your work is to find out what is the food and what is the features like color shape and others and give me all the information in precise manner",
            ],
          },
          {
            "role": "model",
            "parts": [
                "Okay, I understand! Please provide me with the image. I'm ready to analyze it and give you a concise description of the food, including its:\n\n*   **Name:** If I can identify it.\n*   **Color(s):** The dominant and notable colors.\n*   **Shape:** General form and any specific shapes within.\n*   **Other features:** Texture (if visible), garnishes, ingredients that can be discerned, and any other distinctive characteristics.\n\nI'll do my best to be accurate and precise with the information! Looking forward to seeing the image.\n",
                # "Okay, I understand! Please provide me with the image. I'm ready to analyze it and give you a concise description of the food, in json format",
            ],
          },
        ]
    )
    return chat_session

# Function to send image file and receive response from chat session
def analyze_photo(chat_session, image_path):
    # Read image file in binary format
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    # Convert image to base64
    image_base64 = base64.b64encode(image_data).decode("utf-8")

    # Send the image as a base64-encoded string to the model
    response = chat_session.send_message(image_base64)
    return response.text
