import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_summary(df: pd.DataFrame) -> str:
    return f"""
    Total Tracks: {len(df)}
    Total Genres: {df['genre'].nunique()}
    Top Genres: {df['genre'].value_counts().head(5).to_dict()}
    Average Popularity: {df['popularity'].mean():.2f}
    """

def ask_ai_about_data(question: str, df: pd.DataFrame) -> str:
    summary = build_summary(df)

    prompt = f"""
    You are a helpful assistant for a Spotify dataset dashboard.
    Use the dataset summary below to answer the user's question.

    Dataset Summary:
    {summary}

    User Question:
    {question}

    Answer clearly and helpfully.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
