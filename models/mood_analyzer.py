import os
from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please check your .env file.")

genai.configure(api_key=API_KEY)

# Use lightweight model (saves quota)
model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_mood_with_score(text):
    """
    Analyze mood using:
    - Gemini (for intelligent mood label)
    - TextBlob (for polarity score)

    Returns:
        (mood_label, polarity_score)
    """

    if not text or not text.strip():
        return "Neutral", 0.0

    # --- Step 1: Get polarity score using TextBlob ---
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to +1

    # --- Step 2: Use Gemini to detect emotional label ---
    try:
        prompt = f"""
        Identify the primary emotional state of this text in ONE word only.

        Text: "{text}"

        Possible examples:
        Happy, Sad, Stressed, Calm, Anxious, Angry, Motivated, Neutral
        """

        response = model.generate_content(prompt)

        mood_label = response.text.strip().split()[0]

    except Exception as e:
        # If Gemini fails, fallback to polarity-based label
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