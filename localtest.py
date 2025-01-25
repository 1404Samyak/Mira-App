from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Specify the video ID (from the YouTube URL)
url="https://youtu.be/nxowuOht6ec"
video_id = url.replace('https://youtu.be/',"")

# Fetch the transcript
plain_transcript=""
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine all the text into a single plain transcript
    plain_transcript = " ".join([entry['text'] for entry in transcript])
except Exception as e:
    print(f"An error occurred: {e}")

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("APP_KEY")

# Initialize the client
client = MiraClient(config={"API_KEY": api_key})

flow = Flow(source="flow.yaml")

input_dict = {"doubt":"What is generative AI","transcript":plain_transcript}

response = client.flow.test(flow, input_dict)
print(response)
# print(plain_transcript,len(plain_transcript),type(plain_transcript))