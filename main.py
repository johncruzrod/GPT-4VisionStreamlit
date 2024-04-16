import streamlit as st
import base64
import openai
import requests

st.set_page_config(layout="wide")

# Use Streamlit's secret management to safely store and access your API key
api_key = st.secrets["OPENAI_API_KEY"]

# Function to encode the image
def encode_image(uploaded_file):
   file_content = uploaded_file.read()
   base64_image = base64.b64encode(file_content).decode('utf-8')
   return base64_image

# Set up the columns
left_column, main_column, right_column = st.columns([1, 2, 1])

# Add content to the left column
with left_column:
   st.write("""
   <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
   <h2 style="color: #1a1a1a; font-size: 32px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">Unleash the Power of GPT Vision</h2>
   <p style="color: #4c4c4c; text-align: justify; font-size: 18px; line-height: 1.6; margin-bottom: 20px;">
   Unlock the secrets hidden within your images with <strong style="color: #007bff;">GPT Vision</strong>. This cutting-edge technology harnesses the power of OpenAI's language models to analyze and interpret visual data like never before.
   </p>
   <p style="color: #4c4c4c; text-align: justify; font-size: 18px; line-height: 1.6;">
   From extracting tabular data to identifying locations, GPT Vision is your gateway to a world of visual insights. Experience the future of image analysis today!
   </p>
   </div>
   """, unsafe_allow_html=True)

# Add your main component to the middle column
with main_column:
   st.header('Upload an Image below, and ask ChatGPT a question about it:')
   # File uploader
   uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "gif", "webp"])
   # Display the uploaded image centrally
   if uploaded_file is not None:
       st.image(uploaded_file, use_column_width=True)
   # Request input
   request = st.text_input("Type your question here:")
   # Submit button
   if st.button("Submit"):
       if uploaded_file is not None:
           # Encode the uploaded image
           base64_image = encode_image(uploaded_file)
           # Prepare the headers for the HTTP request to OpenAI API
           headers = {
               "Content-Type": "application/json",
               "Authorization": f"Bearer {api_key}"
           }
           # Prepare the payload with the encoded image and the user's request
           payload = {
               "model": "gpt-4-turbo",
               "messages": [
                   {
                       "role": "user",
                       "content": [
                           {
                               "type": "text",
                               "text": request
                           },
                           {
                               "type": "image_url",
                               "image_url": {
                                   "url": f"data:image/jpeg;base64,{base64_image}",
                                   "detail": "high"
                               }
                           }
                       ]
                   }
               ],
               "max_tokens": 4000
           }
           # Show the loading wheel
           with st.spinner("Processing your request..."):
               try:
                   # Make the HTTP request to the OpenAI API
                   response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                   # Check the response status and display the output or an error message
                   if response.status_code == 200:
                       response_json = response.json()
                       output = response_json["choices"][0]["message"]["content"]
                       st.markdown(output, unsafe_allow_html=True)
                   else:
                       error_message = f"An error occurred while processing the request. Status code: {response.status_code}"
                       error_details = response.text
                       st.error(error_message)
                       st.error(f"Error details: {error_details}")
               except requests.exceptions.RequestException as e:
                   st.error(f"An error occurred while making the request: {str(e)}")
       else:
           st.warning("Please upload an image.")

# Add content to the right column
with right_column:
  st.write("""
  <div style="background-color: #f8f9fa; padding: 20px; border-radius: 15px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
  <p style="color: #333333; font-family: 'Arial', serif; font-size: 16px; line-height: 1.5;"><strong>Extract the table from this image:</strong> Effortlessly extract tabular data from any image, making data analysis a breeze.</p>
  
  <p style="color: #333333; font-family: 'Arial', serif; font-size: 16px; line-height: 1.5;"><strong>Tell me where this photo was taken:</strong> Uncover the location depicted in your photos, unlocking a world of geographical context.</p>

  <p style="color: #333333; font-family: 'Arial', serif; font-size: 16px; line-height: 1.5;"><strong>Extract the writing from this whiteboard:</strong> Capture your notes and turn them into structured text.</p>
  
  <p style="color: #333333; font-family: 'Arial', serif; font-size: 16px; line-height: 1.5;"><strong>Describe the objects in this scene:</strong> Get detailed descriptions of the objects, people, and elements present in your images.</p>
  </div>
  """, unsafe_allow_html=True)
