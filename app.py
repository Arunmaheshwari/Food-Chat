import streamlit as st
from PIL import Image
import base64
import io
import os
from main import configure_genai, create_model, start_chat_session, analyze_photo


configure_genai()

# Initialize model and start chat session
model = create_model()
chat_session = start_chat_session(model)

# Streamlit UI
st.title("Food Detail Extractor using Gemini API")
st.write("Upload a food-related photo and get detailed analysis.")

# File uploader (allowing various formats)
uploaded_file = st.file_uploader("Upload a photo:", type=["jpg", "jpeg", "png", "jfif"])

if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)
    
    # Save the image as a temporary file to send it to the API
    temp_file_path = "temp_uploaded_image.jpg"
    image.save(temp_file_path)
    
    # Send the image file to the Gemini model for evaluation
    with st.spinner("Sending the photo to the Gemini API for analysis..."):
        response_text = analyze_photo(chat_session, temp_file_path)
    
    # Display the response
    st.success("Response Received!")
    st.write("**Extracted Details:**")
    st.text(response_text)
    
    # Optionally, show the image uploaded
    st.image(image, caption="Uploaded Image", use_column_width=True)
