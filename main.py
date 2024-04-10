import streamlit as st
import base64
import openai
import requests

# Set up the Streamlit app
st.title("GPT Vision App")
st.header('Upload an Image below, and ask ChatGPT a question about it:', divider='rainbow')



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

        try:
            # Make the HTTP request to the OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            # Check the response status and display the output or an error message
            if response.status_code == 200:
                response_json = response.json()
                output = response_json["choices"][0]["message"]["content"]
                st.success(output)
            else:
                error_message = f"An error occurred while processing the request. Status code: {response.status_code}"
                error_details = response.text
                st.error(error_message)
                st.error(f"Error details: {error_details}")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while making the request: {str(e)}")
    else:
        st.warning("Please upload an image.")
