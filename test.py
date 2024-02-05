import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

def load_environment_variables():
    load_dotenv()  # Load all the environment variables
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except IndexError as e:
        st.error("Invalid YouTube video link format.")
    except YouTubeTranscriptApi.TranscriptNotFoundException as e:
        st.error("Transcript not found for the given YouTube video.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def show_video_thumbnail(youtube_link):
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

def get_detailed_notes_button():
    if st.button("Get Detailed Notes", key='detailed_notes_btn', help="Click to generate detailed notes"):
        transcript_text = extract_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)
        else:
            st.warning("Transcript is empty.")

load_environment_variables()

prompt = f"""
You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:
"""

st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

# Dark and White mode toggle button in the sidebar
dark_mode = st.sidebar.checkbox("Dark Mode", help="Toggle Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
        body {
            color: white;
            background-color: #2e4057;
        }
        .stTextInput, .stNumberInput, .stSelectbox, .stTextArea, .stCheckbox, .stRadio {
            color: white;
            background-color: #3b5268;
        }
        .stButton>button {
            color: white !important;
            background-color: #007bff !important;
        }
        .stMarkdown {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

if youtube_link:
    show_video_thumbnail(youtube_link)

# Centered "Get Detailed Notes" button with blue color
st.markdown("""
<style>
    .get-detailed-notes-btn {
        display: flex;
        justify-content: center;
    }
    .get-detailed-notes-btn button {
        background-color: #007bff;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

get_detailed_notes_button()
