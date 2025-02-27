import streamlit as st
import os
os.system("pip install -U google-generativeai")
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()  # Load all environment variables
from PIL import Image

# Configure Gemini API with API key
genai.configure(api_key=os.environ['API_KEY'])

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use the new model
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Calories Advisor App")

st.header("Calories Advisor App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the Total Calories")

# Nutrition analysis prompt
input_prompt = """
You are a nutrition expert. Analyze the food items in the image and provide:
1. A list of food items with their calorie count.
2. Whether the food is healthy or not.
3. A breakdown of macronutrients (carbs, fats, proteins, fibers, sugar) in percentage.

Format:
1. Item 1 - X calories
2. Item 2 - Y calories
...
Health analysis: [Healthy/Unhealthy]
Macronutrient breakdown:
- Carbohydrates: X%
- Fats: Y%
- Proteins: Z%
- Fibers: A%
- Sugar: B%
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("Analysis Result")
    st.write(response)
