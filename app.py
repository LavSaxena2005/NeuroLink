import os
import streamlit as st
import pandas as pd
from datetime import datetime
from models.mood_analyzer import analyze_mood_with_score
from utils.focus_recommender import get_focus_tips
from utils.chatbot_responses import get_chat_response
from utils.visualizer import plot_mood_trend, plot_mood_pie, weekly_summary_table

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
DATA_PATH = "data/mood_data.csv"

st.set_page_config(page_title="NeuroLink — AI Mental Fitness Companion", layout="centered")
st.title("🧠 NeuroLink — AI Mental Fitness Companion")

# Load existing data
if os.path.exists(DATA_PATH):
    try:
        mood_data = pd.read_csv(DATA_PATH, parse_dates=["date"])
    except Exception:
        mood_data = pd.DataFrame(columns=["date","text","mood","score"])
else:
    mood_data = pd.DataFrame(columns=["date","text","mood","score"])

# Sidebar settings
st.sidebar.header("Settings")
save_data = st.sidebar.checkbox("Save my entries (Privacy Mode off)", value=True)
show_examples = st.sidebar.checkbox("Show example inputs", value=False)

if show_examples:
    st.sidebar.markdown("- I'm feeling great today!")
    st.sidebar.markdown("- I am stressed about exams.")
    st.sidebar.markdown("- I feel calm after meditation.")

# Input section
st.subheader("Log your mood")
user_text = st.text_area("How are you feeling right now?", height=120)

col1, col2 = st.columns([3,1])

with col2:
    analyze_btn = st.button("Analyze")

with col1:
    st.write("Tip: write a sentence or two — the analyzer works better with context.")

# Analyze button logic
if analyze_btn:

    if not user_text.strip():
        st.warning("Please type something to analyze your mood.")

    else:
        with st.spinner("Analyzing your mood..."):
            mood, score = analyze_mood_with_score(user_text)
            tips = get_focus_tips(mood)
            reply = get_chat_response(mood)

        score_percent = int(round((score + 1) / 2 * 100))
        emoji = "😊" if score > 0.2 else ("😞" if score < -0.2 else "😐")

        st.success(f"Detected mood: **{mood} {emoji} ({score_percent}% positivity)**")
        st.info(f"💡 Suggestion: {tips}")
        st.write(f"🤖 NeuroCoach: {reply}")

        # Save entry
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
        else:
            st.info("Privacy mode ON — this entry was not saved.")

# Dashboard Section
st.markdown('---')
st.subheader("Your Mood Dashboard")

if mood_data.empty:
    st.info("No saved mood entries yet.")
else:
    st.write("Recent entries:")
    st.dataframe(mood_data.tail(10).reset_index(drop=True))

    st.markdown("### Mood trend over time")
    plot_mood_trend(mood_data)

    st.markdown("### Mood breakdown")
    plot_mood_pie(mood_data)

    st.markdown("### Weekly summary (last 7 days)")
    summary_df = weekly_summary_table(mood_data)
    st.table(summary_df)

    csv = mood_data.to_csv(index=False)
    st.download_button(
        "📥 Download full mood history",
        csv,
        file_name="mood_history.csv",
        mime="text/csv"
    )

st.markdown('---')
st.caption("NeuroLink — AI Mental Fitness Companion | Built with Streamlit")