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
                            "type": "image",
                            "image": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Debug: Print the status code and response content for troubleshooting
        print("Status Code:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            response_data = response.json()
            output = response_data['choices'][0]['message']['content']
            st.success(output)
        else:
            st.error("An error occurred while processing the request. Check logs for details.")
    else:
        st.warning("Please upload an image.")
