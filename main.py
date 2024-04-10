import streamlit as st
import base64
import requests

# Set up the Streamlit app
st.title("GPT Vision App")

# Use Streamlit's secret management to safely store and access your API key and the correct password
api_key = st.secrets["OPENAI_API_KEY"]

# Function to encode the image
def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

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

        # Send the request to the GPT Vision API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Display the output
        if response.status_code == 200:
            output = response.json()["choices"][0]["message"]["content"]
            st.success(output)
        else:
            st.error("An error occurred while processing the request.")
    else:
        st.warning("Please upload an image.")
