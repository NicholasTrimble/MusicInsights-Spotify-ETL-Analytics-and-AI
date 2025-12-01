import sys
import os

# Make project root importable when running "streamlit run dashboard/app.py"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st
from dashboard.ai_helper import ask_ai_about_data

DATA_PATH = os.path.join("data", "processed", "spotify_clean.csv")


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def page_overview(df: pd.DataFrame):
    st.title("MusicInsights: Spotify ETL, Analytics, and AI")
    st.caption(
        "A small end-to-end project that cleans Spotify track data, explores it, "
        "and exposes simple analytics and an AI assistant on top."
    )

    st.subheader("Quick Snapshot")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tracks", f"{len(df):,}")
    with col2:
        st.metric("Unique Genres", df["genre"].nunique())
    with col3:
        st.metric("Average Popularity", f"{df['popularity'].mean():.1f}")

    st.subheader("Sample of the Dataset")
    st.dataframe(
        df[[
            "artist_name",
            "track_name",
            "genre",
            "popularity",
            "danceability",
            "energy"
        ]].head(20),
        use_container_width=True
    )


def page_genre_analysis(df: pd.DataFrame):
    st.title("Genre Analysis")

    st.write(
        "This view looks at the average popularity by genre. "
        "Use it to see which genres tend to perform better in this dataset."
    )

    top_n = st.slider("Number of Top Genres to View", 5, 30, 10)

    genre_pop = (
        df.groupby("genre")["popularity"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
    )

    st.bar_chart(genre_pop)

    with st.expander("Show underlying data"):
        st.dataframe(genre_pop.reset_index().rename(columns={"popularity": "avg_popularity"}))


def page_feature_distributions(df: pd.DataFrame):
    st.title("Audio Feature Distributions")

    st.write(
        "Pick an audio feature to see how it's distributed across all tracks."
    )

    feature = st.selectbox(
        "Choose a feature",
        ["danceability", "energy", "valence", "tempo", "loudness", "duration_min"],
    )

    bins = st.slider("Number of bins", 10, 80, 30)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df[feature], bins=bins)
    ax.set_title(f"Distribution of {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel("Count")

    st.pyplot(fig)


def page_song_explorer(df: pd.DataFrame):
    st.title("Song Explorer")

    st.write(
        "Filter by genre and optionally search by artist or track name "
        "to browse individual songs."
    )

    genre = st.selectbox(
        "Filter by genre", ["All"] + sorted(df["genre"].unique())
    )

    search_text = st.text_input("Search by artist or track name (optional):").strip()

    if genre == "All":
        filtered = df
    else:
        filtered = df[df["genre"] == genre]

    if search_text:
        mask = (
            filtered["artist_name"].str.contains(search_text, case=False, na=False)
            | filtered["track_name"].str.contains(search_text, case=False, na=False)
        )
        filtered = filtered[mask]

    st.write(
        filtered[
            ["artist_name", "track_name", "genre", "popularity", "danceability", "energy"]
        ].head(200)
    )


def page_ai_assistant(df: pd.DataFrame):
    st.title("AI Assistant")
    st.write(
        "Ask a question about the dataset, genres, or popularity trends. "
        "The assistant answers using a lightweight summary of the data."
    )

    question = st.text_input("Enter your question here:")

    if st.button("Ask AI"):
        with st.spinner("Thinking..."):
            response = ask_ai_about_data(question, df)

        st.markdown("**AI Response:**")
        st.write(response)


def main():
    df = load_data()

    st.sidebar.title("MusicInsights Navigation")
    st.sidebar.markdown("Use the options below to explore the project.")

    page = st.sidebar.radio(
        "Go to:",
        [
            "Overview",
            "Genre Analysis",
            "Feature Distributions",
            "Song Explorer",
            "AI Assistant",
        ],
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
