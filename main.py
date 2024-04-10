import streamlit as st
import base64
import requests
import openai

# Set up the Streamlit app
st.title("GPT Vision App")

# Use Streamlit's secret management to safely store and access your API key
api_key = st.secrets["OPENAI_API_KEY"]

# Function to encode the image
def encode_image(uploaded_file):
    file_content = uploaded_file.read()
    base64_image = base64.b64encode(file_content).decode('utf-8')
    return base64_image

# File uploader
uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "gif", "webp"])

# Request input
request = st.text_input("Enter your request")

# Debugging function to log messages to the Streamlit UI
def log_to_app(message, message_type="info"):
    if message_type == "info":
        st.info(message)
    elif message_type == "success":
        st.success(message)
    elif message_type == "error":
        st.error(message)
    elif message_type == "warning":
        st.warning(message)
    else:
        st.text(message)

# Submit button
if st.button("Submit"):
    if uploaded_file is not None:
        # Encode the uploaded image
        base64_image = encode_image(uploaded_file)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "text-davinci-003",  # Be sure to use the appropriate model name here
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request
                        },
                        {
                            "type": "image",
                            "image": {
                                # Ensure you are using the data property, not url, for base64 images
                                "data": base64_image,
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Instead of using print, use our logging function to display in the app
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        except Exception as e:
            log_to_app(f"An exception occurred: {str(e)}", "error")
            return

        if response.status_code == 200:
            response_data = response.json()
            output = response_data['choices'][0]['message']['content']
            log_to_app(output, "success")
        else:
            log_to_app("An error occurred while processing the request.", "error")
            log_to_app(f"Status Code: {response.status_code}\nResponse Content: {response.text}", "warning")
    else:
        log_to_app("Please upload an image.", "warning")
