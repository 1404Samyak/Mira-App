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
flow1 = Flow(source="flow1.yaml")

# Apply custom CSS for styling
st.markdown("""
    <style>
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .block-container {
            box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.1);
            padding: 20px;
            border-radius: 15px;
            background-color: #f8f9fa;
        }
        h1 {
            color: #4CAF50;
            font-family: 'Arial', sans-serif;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("Doubt Resolver App")

# Subheader
st.subheader("Resolve your doubts quickly by providing the required input below.")

# Dropdown for input type
input_type = st.selectbox("Select Input Type:", ["Video URL", "PDF File"])

# Input logic
if input_type == "Video URL":
    video_url = st.text_input("Enter the Video URL:")
    video_id = video_url.replace('https://youtu.be/', "")
    doubt = st.text_input("Enter Your Doubt:")
    
    # Button to resolve the doubt
    if st.button("Resolve Doubt"):
        st.success("Processing your request...")
        plain_transcript = ""
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            plain_transcript = " ".join([entry['text'] for entry in transcript])
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input_dict = {"doubt": doubt, "transcript": plain_transcript}
        input_dict1 = {"transcript": plain_transcript}
        
        response1 = client.flow.test(flow, input_dict)
        response2 = client.flow.test(flow1, input_dict1)
        
        st.subheader("Summary")
        st.write(response2['result'])
        
        st.subheader("Explanation of your doubt")
        st.write(response1['result'])
        
        st.info(f"Video URL: {video_url}\nDoubt: {doubt}")

# elif input_type == "PDF File":
#     pdf_file = st.file_uploader("Upload a PDF File:", type=["pdf"])
#     if pdf_file:
#         # Display file name
#         st.write(f"Uploaded file: {pdf_file.name}")
#         # Extract text from PDF
#         try:
#             import PyPDF2
#             pdf_reader = PyPDF2.PdfReader(pdf_file)
#             pdf_text = ""
#             for page in pdf_reader.pages:
#                 pdf_text += page.extract_text()
            
#             st.text_area("Extracted Text from PDF:", pdf_text, height=300)
            
#             doubt = st.text_input("Enter Your Doubt:")
#             if st.button("Resolve Doubt"):
#                 input_dict = {"doubt": doubt, "document_text": pdf_text}
#                 response = client.flow.test(flow, input_dict)
                
#                 st.subheader("Explanation of your doubt")
#                 st.write(response['result'])
        
#         except Exception as e:
#             st.error(f"An error occurred while processing the PDF: {e}")
