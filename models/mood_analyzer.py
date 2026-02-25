import streamlit as st
from textblob import TextBlob
import google.generativeai as genai

# Get API key securely from Streamlit secrets
API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_mood_with_score(text):

    if not text or not text.strip():
        return "Neutral", 0.0

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    try:
        prompt = f"""
        Identify the primary emotional state of this text in ONE word only.

        Text: "{text}"

        Examples:
        Happy, Sad, Stressed, Calm, Anxious, Angry, Motivated, Neutral
        """

        response = model.generate_content(prompt)
        mood_label = response.text.strip().split()[0]

    except Exception:
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
