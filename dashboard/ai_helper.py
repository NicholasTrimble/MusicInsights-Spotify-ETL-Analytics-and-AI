import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import traceback

load_dotenv()

# Load API key safely
API_KEY = os.getenv("OPENAI_API_KEY")

# Graceful failure if key is missing
if not API_KEY:
    client = None
else:
    client = OpenAI(api_key=API_KEY)


def build_summary(df: pd.DataFrame) -> str:
    """Create a compact summary so the AI has context without wasting tokens."""
    return (
        f"Tracks: {len(df)}, "
        f"Genres: {df['genre'].nunique()}, "
        f"Top Genres: {df['genre'].value_counts().head(5).to_dict()}, "
        f"Avg Popularity: {df['popularity'].mean():.2f}"
    )


def ask_ai_about_data(question: str, df: pd.DataFrame) -> str:
    """Ask the AI about the dataset with strong error handling and a natural tone."""

    # If key is missing or client failed to load
    if client is None:
        return (
            "It looks like an OpenAI API key wasn’t detected. "
            "Please make sure your .env file contains OPENAI_API_KEY."
        )

    # Build context
    summary = build_summary(df)

    prompt = (
        "You're assisting a user exploring a Spotify dataset. "
        "Keep your answers friendly, concise, and easy to understand — "
        "as if you're a helpful teammate, not a robot.\n\n"
        f"Dataset Summary: {summary}\n\n"
        f"User Question: {question}\n\n"
        "Provide a clear and human explanation based on the data."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # lowest-cost model
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:
        err = str(e)

        # Specific quota error
        if "insufficient_quota" in err:
            return (
                "It looks like your OpenAI account has run out of free quota. "
                "If you want to keep using the AI Assistant, "
                "you may need to enable pay-as-you-go billing in your OpenAI settings."
            )

        # Rate limit
        if "rate" in err.lower():
            return (
                "You're hitting the rate limit for your API key. "
                "Give it a few seconds and try again."
            )

        # Generic fallback
        return (
            "Something went wrong while contacting the AI service.\n\n"
            f"Error details:\n{traceback.format_exc()}"
        )
