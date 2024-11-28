import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pytesseract  
from PIL import Image 
import base64
from gtts import gTTS
from io import BytesIO  


# Set the path for Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set the API key for Google Generative AI
api_key = "AIzaSyByskqL-TltPyk0RAQ3j04sIJiAecmlBo8"
model_name = "gemini-1.5-flash"

# Function to convert an image file to Base64 encoding
def convert_image_to_base64(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# Function to encode image (added missing function)
def encode_image(image_file):
    buffered = BytesIO()
    image = Image.open(image_file)
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Function to set up the LangChain model with custom prompts
def setup_langchain_model(system_prompt, user_prompt):
    chat_prompt = ChatPromptTemplate.from_messages([system_prompt, user_prompt])
    output_parser = StrOutputParser()
    chat_model = ChatGoogleGenerativeAI(
        google_api_key=api_key, model=model_name
    )
    return chat_prompt | chat_model | output_parser

# Function to extract text from an image using OCR
def extract_text_from_image(image_path):
    try:
        # Open the image file
        image = Image.open(image_path)
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        return text
    except Exception as error:
        print(f"An error occurred during text extraction: {error}")
        return ""

# Function to convert text to speech and save as an audio file
def text_to_speech(text, filename="output_audio.wav"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Set up the page configuration
st.set_page_config(page_title="Visionary AI", layout="wide")

# Display the application title
st.title("VisionaryAI: An AI assistant for Visually Impaired Individuals 👁‍🗨")

st.sidebar.title("📝 About")
st.sidebar.write("VisionaryAI is an AI Assistant that helps visually impaired users by providing scene descriptions, text extraction, and speech.")
st.sidebar.markdown(
    """
    📌 **Features**
   - **Scene Description**: Turn the image into a clear description, helping users understand what’s around them.
   - **Text-to-Speech**: Read out loud any text found in the image for easy listening.
   - **Object & Obstacle Detection**: Identify objects or obstacles in the image, ensuring safer navigation.
   - **Personalised Task Assistance**: Assist with daily tasks by recognizing items, reading labels, and giving useful information.
    """
)

# Image Upload Feature
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

# Functionality Selection Dropdown
select_functionality = st.selectbox(
    "Choose a functionality:",
    ["Scene Description", "Text-to-Speech", "Object & Obstacle Detection", "Personalised Task Assistance"],
    index=None, placeholder="Select a feature...",
)

# Analysis Start Button
button = st.button("Generate")

# Processing Uploaded Image on Button Click
if uploaded_file and button:
    # Convert image to Base64 format
    image_data = encode_image(uploaded_file)

    # Perform selected functionality
    with st.spinner("👨‍🦯‍➡️ Analyzing the image... Please wait."):
        # Handling Image Description Request
        if select_functionality == "Scene Description":
            system_prompt = (
                "system",
                """You are an AI assistant helping visually impaired individuals.
                These individuals often face difficulties in understanding their surroundings and performing tasks that require sight.
                They will upload an image and ask for assistance in understanding the scene, reading text, detecting obstacles, or assisting with daily tasks.
                Your task is to respond in an easy-to-understand way with comprehensive explanations."""
            )
            input_prompt = "Give a detailed description of the uploaded image."

            user_prompt = (
                "human",
                [
                    {"type": "text", "text": "{input}"},
                    {"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data}"},
                ],
            )

            chain = setup_langchain_model(system_prompt, user_prompt)

            user_input = {
                "input": input_prompt,
                "image_data": image_data,
            }

            description = chain.invoke(user_input)
            st.image(uploaded_file, caption="Uploaded Image", width=200)
            st.markdown("### 📝 Generated Analysis")
            st.success(description)

        # Handling Text-to-Speech Conversion
        elif select_functionality == "Text-to-Speech":
            extracted_text = extract_text_from_image(uploaded_file)
            st.image(uploaded_file, caption="Uploaded Image", width=200)
            st.markdown("### 📝 Generated Analysis")
            st.success(extracted_text)

            # Generate and display the audio file
            audio_file = text_to_speech(extracted_text)
            st.markdown("### 🎙️ Generated Audio")
            st.audio(audio_file, format="audio/mp3")

        # Handling Object Detection
        elif select_functionality == "Object & Obstacle Detection":
            system_prompt = (
                "system",
                """You are an AI assistant for visually impaired individuals, helping them identify objects and obstacles for safer movement.
                The user will upload an image and ask for object detection assistance, where you will provide details of identified objects or obstacles along with their relevance to the scene."""
            )
            input_prompt = """Examine the image for objects or obstacles. 
            Identify and describe them in detail, including their positions and significance to user safety."""
            user_prompt = (
                "human",
                [
                    {"type": "text", "text": "{input}"},
                    {"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data}"},
                ],
            )

            chain = setup_langchain_model(system_prompt, user_prompt)

            user_input = {
                "input": input_prompt,
                "image_data": image_data,
            }

            description = chain.invoke(user_input)
            st.image(uploaded_file, caption="Uploaded Image", width=200)
            st.markdown("### 📝 Generated Analysis")
            st.success(description)

        # Handling Task Assistance
        elif select_functionality == "Personalised Task Assistance":
            system_prompt = (
                "system",
                """You are a helpful AI assistant for visually impaired individuals, aiding them with tasks that require sight. 
                Upon uploading an image, you will offer assistance with tasks such as recognizing items, reading labels, and providing helpful context."""
            )
            input_prompt = """Analyze the image to recognize items, interpret labels, and offer guidance on completing daily tasks."""
            user_prompt = (
                "human",
                [
                    {"type": "text", "text": "{input}"},
                    {"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data}"},
                ],
            )

            chain = setup_langchain_model(system_prompt, user_prompt)

            user_input = {
                "input": input_prompt,
                "image_data": image_data,
            }

            description = chain.invoke(user_input)
            st.image(uploaded_file, caption="Uploaded Image", width=200)
            st.markdown("### 📝 Generated Analysis")
            st.success(description)
