# NeuroLink — Upgraded (Streamlit PoC)

This upgraded version adds the following features:
- Sentiment score (polarity) and % positivity
- Emoji feedback and richer mood labels (Very Positive, Positive, Neutral, Negative, Very Negative)
- Focus recommender and motivational chatbot responses
- Mood trend line chart and mood distribution pie chart
- Weekly summary table (last 7 days)
- Privacy mode (toggle in sidebar to avoid saving entries)

## Run instructions
1. Create a Python environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- Data is stored locally under `data/mood_data.csv` when 'Save my entries' is enabled in the sidebar.
- This is a PoC — for production you should add authentication and secure storage.
