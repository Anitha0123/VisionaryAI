# VisionaryAI - An AI assistant for Visually Impaired Individuals 👁‍🗨

**VisionaryAI** is a powerful AI-powered assistant designed to help visually impaired individuals by providing scene descriptions, text extraction, object detection, and personalized task assistance through images. The assistant uses state-of-the-art technologies such as Langchain, Google Generative AI, Tesseract OCR, and Text-to-Speech (gTTS) to provide a comprehensive and user-friendly experience.

---

## Features

- **Scene Description**: Turn the uploaded image into a detailed, easy-to-understand description of the surroundings.
- **Text-to-Speech**: Extract text from the image and read it aloud to help users understand the content.
- **Object & Obstacle Detection**: Identify and describe objects and obstacles in the image to ensure safer navigation.
- **Personalized Task Assistance**: Recognize items and labels in the image, offering guidance on daily tasks.

---

## Prerequisites

Ensure that the following libraries and tools are installed before running the app:

- Python 3.7 or higher
- Streamlit
- Langchain
- Google Generative AI API
- Tesseract OCR
- gTTS (Google Text-to-Speech)

---

## 🖥️ Installation  

### 1️. Clone the Repository  
```bash  
git clone  https://github.com/Rohitjakkam/SightAssist.git
cd SightAssist
```
2️. Create a Virtual Environment
```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3️. Install Dependencies
```bash
pip install -r dependencies.txt  
```
4️. Set up Tesseract Path (if required)
Add the Tesseract OCR executable path in the script (example for Windows):
```bash
import pytesseract  
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

To run the Streamlit App
```bash
streamlit run Code_AIassistant.py
```

