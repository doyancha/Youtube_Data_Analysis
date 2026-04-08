from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except Exception:
    SentimentIntensityAnalyzer = None


ROOT = Path(__file__).resolve().parent
FULL_DF_PATH = ROOT / "full_df.csv"
COMMENTS_PATH = ROOT / "comments_data.csv"
OUTPUT_DIR = ROOT / "data"
VIDEO_OUTPUT_PATH = OUTPUT_DIR / "youtube_videos.parquet"
COMMENTS_OUTPUT_PATH = OUTPUT_DIR / "comments_sentiment.parquet"

VIDEO_COLUMNS = [
    "video_id",
    "trending_date",
    "title",
    "channel_title",
    "category_name",
    "views",
    "likes",
    "dislikes",
    "comment_count",
    "like_rate",
    "dislike_rate",
    "comment_count_rate",
    "punc_count",
]
NUMERIC_COLUMNS = [
    "views",
    "likes",
    "dislikes",
    "comment_count",
    "like_rate",
    "dislike_rate",
    "comment_count_rate",
    "punc_count",
]
MAX_COMMENT_SAMPLE = 60000


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [col.replace("\ufeff", "").strip() for col in cleaned.columns]
    cleaned = cleaned.loc[:, ~cleaned.columns.duplicated()]
    return cleaned


def simple_sentiment_score(text: str) -> float:
    positive_words = {
        "good", "great", "love", "amazing", "best", "beautiful", "nice", "awesome",
        "cool", "favorite", "excellent", "fun", "perfect", "helpful",
    }
    negative_words = {
        "bad", "worst", "hate", "awful", "boring", "terrible", "poor", "annoying",
        "fake", "waste", "broken", "ugly", "problem", "trash",
    }
    tokens = [token.strip(".,!?;:()[]{}\"'").lower() for token in str(text).split()]
    if not tokens:
        return 0.0
    score = sum(token in positive_words for token in tokens) - sum(token in negative_words for token in tokens)
    return float(np.clip(score / max(len(tokens), 1) * 4, -1, 1))


def build_video_dataset() -> pd.DataFrame:
    if not FULL_DF_PATH.exists():
        raise FileNotFoundError(f"Missing source file: {FULL_DF_PATH}")

    df = pd.read_csv(FULL_DF_PATH, low_memory=False)
    df = clean_columns(df)

    missing = [col for col in VIDEO_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in full_df.csv: {missing}")

    video_df = df[VIDEO_COLUMNS].copy()
    for col in NUMERIC_COLUMNS:
        video_df[col] = pd.to_numeric(video_df[col], errors="coerce")

    video_df["trending_date"] = pd.to_datetime(video_df["trending_date"], errors="coerce", format="mixed")
    video_df["category_name"] = video_df["category_name"].fillna("Unknown")
    video_df["channel_title"] = video_df["channel_title"].fillna("Unknown Channel")
    video_df["title"] = video_df["title"].fillna("Untitled Video")
    video_df["video_id"] = video_df["video_id"].astype(str)
    return video_df


def build_comment_dataset() -> pd.DataFrame:
    if not COMMENTS_PATH.exists():
        return pd.DataFrame(columns=["video_id", "comment_text", "sentiment_score", "sentiment_label"])

    comments = pd.read_csv(COMMENTS_PATH, on_bad_lines="skip", low_memory=False)
    comments = clean_columns(comments)

    if "comment_text" not in comments.columns or "video_id" not in comments.columns:
        return pd.DataFrame(columns=["video_id", "comment_text", "sentiment_score", "sentiment_label"])

    comments = comments[["video_id", "comment_text"]].dropna(subset=["comment_text"]).copy()
    comments["video_id"] = comments["video_id"].astype(str)

    if len(comments) > MAX_COMMENT_SAMPLE:
        comments = comments.sample(MAX_COMMENT_SAMPLE, random_state=42)

    analyzer = None
    if SentimentIntensityAnalyzer is not None:
        try:
            analyzer = SentimentIntensityAnalyzer()
        except Exception:
            analyzer = None

    if analyzer is not None:
        comments["sentiment_score"] = comments["comment_text"].astype(str).apply(
            lambda text: analyzer.polarity_scores(text)["compound"]
        )
    else:
        comments["sentiment_score"] = comments["comment_text"].astype(str).apply(simple_sentiment_score)

    comments["sentiment_label"] = pd.cut(
        comments["sentiment_score"],
        bins=[-1.01, -0.15, 0.15, 1.01],
        labels=["Negative", "Neutral", "Positive"],
    ).astype(str)
    return comments


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    video_df = build_video_dataset()
    comments_df = build_comment_dataset()

    video_df.to_parquet(VIDEO_OUTPUT_PATH, index=False)
    comments_df.to_parquet(COMMENTS_OUTPUT_PATH, index=False)

    print(f"Saved {VIDEO_OUTPUT_PATH.name}: {len(video_df):,} rows")
    print(f"Saved {COMMENTS_OUTPUT_PATH.name}: {len(comments_df):,} rows")
    print(f"Video file size: {VIDEO_OUTPUT_PATH.stat().st_size / (1024 * 1024):.2f} MB")
    print(f"Comments file size: {COMMENTS_OUTPUT_PATH.stat().st_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    main()
