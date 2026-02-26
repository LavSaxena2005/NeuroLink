import os
from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

genai.configure(api_key=API_KEY)

# Use lightweight model (quota-friendly)
model = genai.GenerativeModel("gemini-1.5-flash")


@st.cache_data(show_spinner=False)
def analyze_mood_with_score(text):
    """
    Analyze mood using:
    - Gemini (emotion label)
    - TextBlob (polarity score)

    Returns:
        (mood_label, polarity_score)
    """

    if not text or not text.strip():
        return "Neutral", 0.0

    # -------- Step 1: TextBlob polarity --------
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to +1

    # -------- Step 2: Gemini Emotion Detection --------
    try:
        prompt = f"""
        Identify the primary emotional state of this text in ONE single word only.
        No punctuation. No explanation.

        Text: "{text}"

        Possible labels:
        Happy, Sad, Stressed, Calm, Anxious, Angry, Motivated, Neutral
        """

        response = model.generate_content(prompt)

        if response and response.text:
            mood_label = response.text.strip().split()[0]
            mood_label = mood_label.capitalize()
        else:
            mood_label = "Neutral"

    except Exception:
        # -------- Fallback to polarity-based label --------
        if polarity > 0.4:
            mood_label = "Very Positive"
        elif polarity > 0.1:
            mood_label = "Positive"
        elif polarity < -0.4:
            mood_label = "Very Negative"
        elif polarity < -0.1:
            mood_label = "Negative"
        else:
            mood_label = "Neutral"

    return mood_label, polarity
