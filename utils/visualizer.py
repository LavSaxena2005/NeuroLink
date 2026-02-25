import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def plot_mood_trend(mood_data):
    # Convert date column to datetime if not already
    df = mood_data.copy()
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception:
            pass
    else:
        st.warning("No date column found for trend plotting.")
        return

    # Use score for numeric plot if available
    if 'score' in df.columns:
        df_sorted = df.sort_values('date')
        plt.figure(figsize=(8,3))
        plt.plot(df_sorted['date'], df_sorted['score'], marker='o')
        plt.title('Sentiment score over time')
        plt.xlabel('Date')
        plt.ylabel('Score (-1 to +1)')
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.info('No numeric score available to plot.')

def plot_mood_pie(mood_data):
    df = mood_data.copy()
    if 'mood' not in df.columns:
        st.warning('No mood column found for pie chart.')
        return
    counts = df['mood'].value_counts()
    plt.figure(figsize=(4,4))
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Mood distribution')
    st.pyplot(plt)

def weekly_summary_table(mood_data):
    df = mood_data.copy()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        last7 = df[df['date'] >= (pd.Timestamp.now() - pd.Timedelta(days=7))]
    else:
        last7 = df.copy()
    if last7.empty:
        return pd.DataFrame({'Message': ['No entries in the last 7 days.']})
    counts = last7['mood'].value_counts().rename_axis('mood').reset_index(name='count')
    return counts
