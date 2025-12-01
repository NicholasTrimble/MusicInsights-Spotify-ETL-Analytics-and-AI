import os
import pandas as pd

RAW_PATH = os.path.join("data", "raw", "spotify_tracks.csv")
PROCESSED_PATH = os.path.join("data", "processed", "spotify_clean.csv")


def extract(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "genre",
        "artist_name",
        "track_name",
        "track_id",
        "popularity",
        "duration_ms",
        "danceability",
        "energy",
        "acousticness",
        "speechiness",
        "liveness",
        "instrumentalness",
        "loudness",
        "valence",
        "tempo",
        "key",
        "mode",
        "time_signature"
    ]

    df = df[cols]

    df = df.drop_duplicates()
    df = df.dropna(subset=["popularity", "genre"])

    df["duration_min"] = df["duration_ms"] / 60000

    bins = [0, 25, 50, 75, 100]
    labels = ["low", "medium", "high", "very_high"]
    df["popularity_bucket"] = pd.cut(df["popularity"], bins=bins, labels=labels, include_lowest=True)

    return df


def load(df: pd.DataFrame, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)


def run_etl():
    print("Extracting the data")
    df_raw = extract(RAW_PATH)
    print("Transforming the data")
    df_clean = transform(df_raw)
    print("Loading the data")
    load(df_clean, PROCESSED_PATH)
    print("Done. Your all finished with the ETL process!")


if __name__ == "__main__":
    run_etl()
