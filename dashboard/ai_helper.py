import os
import traceback
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

if API_KEY:
    client = OpenAI(api_key=API_KEY)
else:
    client = None


def build_summary(df: pd.DataFrame) -> str:
    """
    Build a compact summary of the dataset so we can keep requests lightweight.
    """
    top_genres = df["genre"].value_counts().head(5).to_dict()
    avg_popularity = df["popularity"].mean()

    summary = (
        f"Tracks: {len(df)}, "
        f"Genres: {df['genre'].nunique()}, "
        f"Top Genres: {top_genres}, "
        f"Average Popularity: {avg_popularity:.2f}"
    )
    return summary


def ask_ai_about_data(question: str, df: pd.DataFrame) -> str:
    """
    Ask the AI about the dataset using a lightweight summary.
    Returns a friendly, human-style answer, or a helpful error message.
    """

    if not client:
        return (
            "I couldn't find an OpenAI API key. "
            "Make sure you have a .env file with OPENAI_API_KEY set locally."
        )

    if not question or not question.strip():
        return "Please ask a question about the dataset, and I'll do my best to answer."

    summary = build_summary(df)

    prompt = (
        "You're helping someone explore a Spotify songs dataset. "
        "Keep your answers clear, friendly, and fairly short—like a helpful teammate.\n\n"
        f"Dataset summary: {summary}\n\n"
        f"User question: {question}\n\n"
        "Answer based only on the summary above. "
        "If something isn't clear from the data, say that honestly."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=220,
            temperature=0.3,
        )
        return response.choices[0].message.content

    except Exception as e:
        err_text = str(e)

        if "insufficient_quota" in err_text:
            return (
                "The AI service is reporting that the account is out of quota. "
                "If you want to keep using the assistant, you'll probably need to "
                "add billing or a different API key in your .env file."
            )

        if "rate" in err_text.lower():
            return (
                "The AI API is rate limiting requests right now. "
                "Give it a little time and try again."
            )

        # Fallback for anything unexpected
        return (
            "Something went wrong while talking to the AI service.\n\n"
            f"Error details (for debugging locally):\n{traceback.format_exc()}"
        )
