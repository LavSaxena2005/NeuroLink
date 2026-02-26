import os
import streamlit as st
import pandas as pd
from datetime import datetime
from models.mood_analyzer import analyze_mood_with_score
from utils.focus_recommender import get_focus_tips
from utils.chatbot_responses import get_chat_response
from utils.visualizer import plot_mood_trend, plot_mood_pie, weekly_summary_table

# --------------------------
# Setup
# --------------------------
os.makedirs("data", exist_ok=True)
DATA_PATH = "data/mood_data.csv"

st.set_page_config(
    page_title="NeuroLink — AI Mental Fitness Companion",
    layout="centered"
)

st.title("🧠 NeuroLink — AI Mental Fitness Companion")

# --------------------------
# Load Data
# --------------------------
if os.path.exists(DATA_PATH):
    try:
        mood_data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    except Exception:
        mood_data = pd.DataFrame(columns=["date","text","mood","score"])
else:
    mood_data = pd.DataFrame(columns=["date","text","mood","score"])

# --------------------------
# Sidebar
# --------------------------
st.sidebar.header("Settings")

save_data = st.sidebar.checkbox("Save my entries (Privacy Mode off)", value=True)

if st.sidebar.button("Clear Mood History"):
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)
    st.sidebar.success("Mood history cleared. Refresh the page.")

# --------------------------
# Mood Input
# --------------------------
st.subheader("Log your mood")

user_text = st.text_area(
    "How are you feeling right now?",
    height=120
)

col1, col2 = st.columns([3,1])

with col2:
    analyze_btn = st.button("Analyze")

with col1:
    st.write("Tip: Write a sentence or two for better analysis.")

# --------------------------
# Analyze Logic
# --------------------------
if analyze_btn:

    if not user_text.strip():
        st.warning("Please type something to analyze your mood.")
        st.stop()

    # Crisis Safety Filter
    danger_words = ["suicide", "kill myself", "self harm", "end my life"]

    if any(word in user_text.lower() for word in danger_words):
        st.error("If you're in crisis, please contact local emergency services immediately.")
        st.stop()

    try:
        with st.spinner("Analyzing emotional state..."):
            mood, score = analyze_mood_with_score(user_text)

        tips = get_focus_tips(mood)
        reply = get_chat_response(mood)

    except Exception:
        st.error("AI service temporarily unavailable.")
        st.stop()

    # Score formatting
    score_percent = int(round((score + 1) / 2 * 100))
    emoji = "😊" if score > 0.2 else ("😞" if score < -0.2 else "😐")

    st.success(f"Detected mood: **{mood} {emoji} ({score_percent}% positivity)**")
    st.info(f"💡 Suggestion: {tips}")
    st.write(f"🤖 NeuroCoach: {reply}")

    # Save Data
    if save_data:
        new_row = pd.DataFrame([{
            "date": datetime.now(),
            "text": user_text.replace('\n',' '),
            "mood": mood,
            "score": score
        }])

        mood_data = pd.concat([mood_data, new_row], ignore_index=True)
        mood_data.to_csv(DATA_PATH, index=False)

        st.success("Entry saved to your mood history.")

# --------------------------
# Dashboard
# --------------------------
st.markdown("---")
st.subheader("Your Mood Dashboard")

if mood_data.empty:
    st.info("No saved mood entries yet.")
else:
    st.dataframe(mood_data.tail(10).reset_index(drop=True))

    st.markdown("### Mood Trend Over Time")
    plot_mood_trend(mood_data)

    st.markdown("### Mood Breakdown")
    plot_mood_pie(mood_data)

    st.markdown("### Weekly Summary")
    summary_df = weekly_summary_table(mood_data)
    st.table(summary_df)

    csv = mood_data.to_csv(index=False)
    st.download_button(
        "📥 Download Full Mood History",
        csv,
        file_name="mood_history.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("NeuroLink — AI Mental Fitness Companion")
