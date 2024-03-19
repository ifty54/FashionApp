from PIL import Image
import streamlit as st

# Add your HTML code for the logo and layout
header_html = """
<div style="display: flex; align-items: center; justify-content: space-between; padding: 2rem;">
    <div>
        <img src="https://scontent.fdac107-1.fna.fbcdn.net/v/t39.30808-6/351555268_3500384293553481_6829862043413033893_n.png?_nc_cat=102&ccb=1-7&_nc_sid=5f2048&_nc_eui2=AeEqDngsem-Wd5a1PnDBP8PY4Pg152UhAPzg-DXnZSEA_HqeFXx3DXqBQIk5TfTdA0vDYwQzefJHKwR6tJ6Y3off&_nc_ohc=TjAvaPNadfQAX8NSkLc&_nc_ht=scontent.fdac107-1.fna&oh=00_AfDB02dV7ud_3U68ZY9A0lmslanG__E-LouxEeX0JKVqoQ&oe=65EDBCB9" style="width: 500px;">
    </div>
    <div style="text-align: center;">
        <h1></h1>
    </div>
    <div></div>
</div>
"""

# Display the header HTML
st.markdown(header_html, unsafe_allow_html=True)

# Your existing code below...
st.header("Your Travel Guide by Project Six Four")

# Import statements
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Gemini Pro Vision API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to setup image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Input section
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Guide me!")

# Prompt text
input_prompt = """
You are an expert in travel where you need to see the image of the travel destinations that the user has uploaded. And, from the image,
kindly provide travel itineraries, destination guides, and recommendations for activities, accommodations, dining options, and budget to carry.
               ----
               ----
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_repsonse(input_text, image_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
