import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
from dashboard.ai_helper import ask_ai_about_data
DATA_PATH = os.path.join("data", "processed", "spotify_clean.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def page_overview(df):
    st.title("MusicInsights: Spotify ETL, Analytics, and AI")
    st.subheader("Dataset Overview")

    st.write(df.head())
    st.metric("Total Tracks", len(df))
    st.metric("Total Genres", df["genre"].nunique())


def page_genre_analysis(df):
    st.title("Genre Analysis")

    top_n = st.slider("Number of Top Genres to View", 5, 30, 10)
    genre_pop = (
        df.groupby("genre")["popularity"].mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.bar_chart(genre_pop)


def page_feature_distributions(df):
    st.title("Audio Feature Distributions")

    feature = st.selectbox(
        "Choose a feature",
        ["danceability", "energy", "valence", "tempo", "loudness", "duration_min"]
    )

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[feature], bins=30)
    ax.set_title(f"Distribution of {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")

    st.pyplot(fig)


def page_song_explorer(df):
    st.title("Song Explorer")

    genre = st.selectbox(
        "Filter by genre", ["All"] + sorted(df["genre"].unique())
    )

    if genre == "All":
        filtered = df
    else:
        filtered = df[df["genre"] == genre]

    st.write(
        filtered[
            ["artist_name", "track_name", "genre", "popularity", "danceability", "energy"]
        ].head(200)
    )


def page_ai_assistant(df):
    st.title("AI Assistant")
    st.write("Ask questions about the dataset!")

    question = st.text_input("Enter your question here:")

    if st.button("Ask AI"):
        if question:
            
            response = ask_ai_about_data(question, df)
            st.write("**AI Response:**")
            st.write(response)
        else:
            st.write("Please enter a question.")


def main():
    df = load_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Overview", "Genre Analysis", "Feature Distributions", "Song Explorer", "AI Assistant"],
    )

    if page == "Overview":
        page_overview(df)
    elif page == "Genre Analysis":
        page_genre_analysis(df)
    elif page == "Feature Distributions":
        page_feature_distributions(df)
    elif page == "Song Explorer":
        page_song_explorer(df)
    elif page == "AI Assistant":
        page_ai_assistant(df)


if __name__ == "__main__":
    main()
