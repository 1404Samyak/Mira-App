import streamlit as st
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("MIRA_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

flow = Flow(source="flow.yaml")
flow1=Flow(source="flow1.yaml")
# Apply custom CSS for styling
st.markdown("""
    <style>
        /* Center the app content */
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* Style the input fields */
        .stTextInput {
            width: 80%;
            margin: 10px auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 10px;
            font-size: 16px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }

        /* Style the button */
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            margin: 20px 0;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.2);
        }

        button:hover {
            background-color: #45a049;
        }

        /* Add subtle shadow to the app container */
        .block-container {
            box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 15px;
            background-color: #f8f9fa;
        }

        /* Style the header */
        h1 {
            color: #4CAF50;
            font-family: 'Arial', sans-serif;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        /* Style the subheader */
        h2 {
            color: #6c757d;
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Doubt Resolver App")

# Subheader
st.subheader("Resolve your doubts quickly by providing the video URL and your query below.")

# Input for video URL
video_url = st.text_input("Enter the Video URL:")
video_id = video_url.replace('https://youtu.be/',"")
# Input for the doubt
doubt = st.text_input("Enter Your Doubt:")

# Button to resolve the doubt
if st.button("Resolve Doubt"):
    st.success("Processing your request...")
    # Fetch the transcript
    plain_transcript=""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        plain_transcript = " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"An error occurred: {e}")
    input_dict = {"doubt":doubt,"transcript":plain_transcript}
    input_dict1={"transcript":plain_transcript}
    response1 = client.flow.test(flow, input_dict)
    response2=client.flow.test(flow1,input_dict1)
    
    st.subheader("Summary")
    st.write(response2['result'])
    
    # Display response 1
    st.subheader("Explanation of your doubt")
    st.write(response1['result'])
    
    st.info(f"Video URL: {video_url}\n Doubt: {doubt}")
