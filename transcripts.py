from youtube_transcript_api import YouTubeTranscriptApi

# Specify the video ID (from the YouTube URL)
video_id = "xOS0BhhdUbo&t=517s"  # Replace with the actual video ID

# Fetch the transcript
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Combine all the text into a single plain transcript
    plain_transcript = " ".join([entry['text'] for entry in transcript])
    
    # Print the plain transcript
    print(plain_transcript)
except Exception as e:
    print(f"An error occurred: {e}")
