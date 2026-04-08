from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from collections import Counter

try:
    from nltk.sentiment import SentimentIntensityAnalyzer
except Exception:
    SentimentIntensityAnalyzer = None

try:
    from wordcloud import STOPWORDS, WordCloud
except Exception:
    STOPWORDS = set()
    WordCloud = None


st.set_page_config(
    page_title="YouTube Performance Intelligence",
    page_icon="YT",
    layout="wide",
    initial_sidebar_state="expanded",
)


DATA_PATH = Path("full_df.csv")
COMMENTS_PATH = Path("comments_data.csv")
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
RATE_COLUMNS = ["like_rate", "comment_count_rate", "dislike_rate"]
DISPLAY_LABELS = {
    "views": "Views",
    "likes": "Likes",
    "dislikes": "Dislikes",
    "comment_count": "Comment Count",
    "like_rate": "Like Rate",
    "dislike_rate": "Dislike Rate",
    "comment_count_rate": "Comment Count Rate",
    "punc_count": "Punctuation Count",
    "channel_title": "Channel Title",
    "category_name": "Category",
    "video_id": "Video ID",
    "total_views": "Total Views",
    "total_likes": "Total Likes",
    "avg_like_rate": "Average Like Rate",
    "avg_comment_rate": "Average Comment Rate",
    "videos": "Trending Videos",
    "sentiment_score": "Sentiment Score",
    "sentiment_label": "Sentiment Label",
}
COLORS = {
    "bg": "#090d1a",
    "panel": "rgba(20, 24, 38, 0.90)",
    "line": "rgba(120, 136, 190, 0.18)",
    "text": "#f3f6ff",
    "muted": "#909ab8",
    "cyan": "#12d9ff",
    "blue": "#568dff",
    "pink": "#ff4fd8",
    "purple": "#9b55ff",
    "gold": "#ff8a1f",
    "green": "#18d59f",
}


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        :root {{
            --bg: {COLORS["bg"]};
            --panel: {COLORS["panel"]};
            --line: {COLORS["line"]};
            --text: {COLORS["text"]};
            --muted: {COLORS["muted"]};
            --cyan: {COLORS["cyan"]};
            --blue: {COLORS["blue"]};
            --pink: {COLORS["pink"]};
            --purple: {COLORS["purple"]};
            --gold: {COLORS["gold"]};
        }}
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: var(--text);
        }}
        .stApp {{
            background:
                radial-gradient(circle at 14% 10%, rgba(86,141,255,0.18), transparent 24%),
                radial-gradient(circle at 88% 14%, rgba(155,85,255,0.18), transparent 22%),
                radial-gradient(circle at 82% 72%, rgba(18,217,255,0.08), transparent 26%),
                linear-gradient(180deg, #080b16 0%, #090d1a 52%, #0d1120 100%);
        }}
        #MainMenu, footer {{ visibility: hidden; }}
        .block-container {{
            max-width: 1400px;
            padding-top: 2.6rem;
            padding-bottom: 2.4rem;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(18,21,34,0.99), rgba(13,16,28,0.99)) !important;
            border-right: 1px solid rgba(120, 136, 190, 0.22);
            box-shadow: inset -1px 0 0 rgba(255,255,255,0.02);
        }}
        h1, h2, h3, h4 {{
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 0.03em;
        }}
        .hero {{
            text-align: center;
            padding: 2.65rem 2rem 2.2rem 2rem;
            border-radius: 30px;
            border: 1px solid rgba(120, 136, 190, 0.18);
            background: linear-gradient(180deg, rgba(26,29,44,0.98), rgba(22,25,38,0.92));
            box-shadow: 0 26px 80px rgba(0,0,0,0.34), inset 0 1px 0 rgba(255,255,255,0.04);
            margin-bottom: 1.45rem;
            overflow: hidden;
            position: relative;
        }}
        .overview-hero {{
            margin-top: 1.2rem;
        }}
        .page-intro-card {{
            margin-top: 1.2rem;
        }}
        .hero:before {{
            content: "";
            position: absolute;
            width: 320px;
            height: 320px;
            left: -90px;
            top: -130px;
            background: radial-gradient(circle, rgba(86,141,255,0.22), transparent 70%);
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 0.48rem 0.95rem;
            border-radius: 999px;
            border: 1px solid rgba(86,141,255,0.28);
            background: rgba(86,141,255,0.10);
            color: #96b1ff;
            font-weight: 700;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            box-shadow: 0 0 18px rgba(86,141,255,0.10);
        }}
        .hero h1 {{
            margin: 1.05rem 0 0.7rem 0;
            font-size: clamp(2.1rem, 4vw, 3.6rem);
            color: #fff;
            line-height: 1.08;
            text-shadow: 0 0 20px rgba(86,141,255,0.10);
        }}
        .hero p {{
            max-width: 860px;
            margin: 0 auto;
            color: var(--muted);
            font-size: 1.04rem;
            line-height: 1.85;
        }}
        .section-card {{
            background: var(--panel);
            border: 1px solid rgba(120, 136, 190, 0.15);
            border-radius: 24px;
            padding: 1.2rem 1.25rem;
            box-shadow: 0 18px 48px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.03);
            backdrop-filter: blur(10px);
        }}
        .metric-card {{
            border-radius: 22px;
            padding: 1.15rem 1rem;
            min-height: 142px;
            border: 1px solid rgba(120, 136, 190, 0.16);
            background: linear-gradient(180deg, rgba(28,31,46,0.98), rgba(23,26,40,0.92));
            box-shadow: 0 16px 42px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.03);
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(86,141,255,0.32);
            box-shadow: 0 22px 48px rgba(0,0,0,0.30), 0 0 24px rgba(86,141,255,0.10);
        }}
        .metric-label {{
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.76rem;
            font-weight: 800;
        }}
        .metric-value {{
            color: white;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.68rem;
            margin: 0.7rem 0 0.32rem 0;
        }}
        .metric-note {{
            color: #8ba7ff;
            font-size: 0.88rem;
            font-weight: 600;
        }}
        .section-title {{
            margin: 1.7rem 0 0.6rem 0;
            color: white;
            font-size: 1.18rem;
        }}
        .section-copy {{
            margin: 0 0 1rem 0;
            color: var(--muted);
            line-height: 1.78;
        }}
        .insight {{
            margin-top: 0.75rem;
            margin-bottom: 1.1rem;
            padding: 1rem 1.05rem;
            border-left: 3px solid var(--purple);
            border-radius: 0 18px 18px 0;
            background: rgba(155,85,255,0.10);
            color: #e8f2ff;
            box-shadow: 0 0 24px rgba(155,85,255,0.06);
        }}
        .footer {{
            margin-top: 1.35rem;
            text-align: center;
            color: var(--muted);
            padding: 1rem 1.2rem;
            border-radius: 20px;
            border: 1px solid rgba(120, 136, 190, 0.15);
            background: linear-gradient(180deg, rgba(22,25,39,0.96), rgba(19,22,35,0.92));
        }}
        .sidebar-card {{
            padding: 0.95rem;
            border-radius: 18px;
            border: 1px solid rgba(120, 136, 190, 0.15);
            background: rgba(86,141,255,0.06);
            margin-top: 1rem;
        }}
        .sidebar-brand-card {{
            padding: 1.1rem 1rem;
            border-radius: 22px;
            border: 1px solid rgba(120, 136, 190, 0.16);
            background: linear-gradient(180deg, rgba(30,33,50,0.98), rgba(24,27,43,0.94));
            box-shadow: 0 18px 36px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.03);
            margin-bottom: 1rem;
            text-align: center;
        }}
        .sidebar-brand-card .icon {{
            font-size: 1.8rem;
            margin-bottom: 0.55rem;
        }}
        .sidebar-brand-card .title {{
            font-family: 'Orbitron', sans-serif;
            color: white;
            font-size: 1.25rem;
            margin-bottom: 0.45rem;
        }}
        .sidebar-brand-card .badge {{
            display: inline-flex;
            padding: 0.3rem 0.65rem;
            border-radius: 999px;
            border: 1px solid rgba(86,141,255,0.18);
            background: rgba(86,141,255,0.10);
            color: #8ba7ff;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.7rem;
        }}
        .sidebar-brand-card .copy {{
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.65;
        }}
        .sidebar-contact-card {{
            padding: 1.05rem 1rem;
            border-radius: 22px;
            border: 1px solid rgba(120, 136, 190, 0.16);
            background: linear-gradient(180deg, rgba(29,33,50,0.98), rgba(23,27,43,0.94));
            margin-top: 1rem;
            text-align: center;
            box-shadow: 0 18px 36px rgba(0,0,0,0.24), inset 0 1px 0 rgba(255,255,255,0.03);
        }}
        .sidebar-contact-card .title {{
            font-family: 'Orbitron', sans-serif;
            color: white;
            font-size: 1rem;
            margin-bottom: 0.45rem;
        }}
        .sidebar-contact-card .role {{
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 0.8rem;
        }}
        .sidebar-contact-card .contact-link {{
            display: block;
            text-decoration: none;
            color: #eaf7ff !important;
            padding: 0.58rem 0.75rem;
            margin-bottom: 0.45rem;
            border-radius: 14px;
            border: 1px solid rgba(120, 136, 190, 0.14);
            background: rgba(255,255,255,0.025);
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }}
        .sidebar-contact-card .contact-link:hover {{
            transform: translateY(-2px);
            border-color: rgba(86,141,255,0.24);
            box-shadow: 0 0 18px rgba(86,141,255,0.10);
        }}
        .sidebar-contact-card .contact-label {{
            display: block;
            color: #8ba7ff;
            font-size: 0.68rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.12rem;
        }}
        .sidebar-contact-card .contact-value {{
            display: block;
            color: #ffffff;
            font-size: 0.84rem;
            word-break: break-word;
        }}
        .sticky-top-filter {{
            position: sticky;
            top: 0.8rem;
            z-index: 40;
            padding: 1rem 1rem 0.3rem 1rem;
            border-radius: 22px;
            background: rgba(21,24,38,0.95);
            border: 1px solid rgba(120, 136, 190, 0.15);
            backdrop-filter: blur(14px);
            box-shadow: 0 18px 42px rgba(0,0,0,0.22);
            margin-bottom: 1rem;
        }}
        .sticky-top-filter [data-testid="stCheckbox"] {{
            margin-bottom: 0.1rem;
        }}
        .sticky-top-filter .stButton > button {{
            min-height: 48px;
            white-space: normal;
            line-height: 1.2;
            padding: 0.5rem 0.4rem;
            font-size: 0.76rem;
            font-weight: 700;
            border-radius: 14px;
        }}
        .sticky-top-filter .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, rgba(155,85,255,0.95), rgba(86,141,255,0.92)) !important;
            border: 1px solid rgba(138,110,255,0.82) !important;
            color: white !important;
            box-shadow: 0 0 20px rgba(138,110,255,0.18) !important;
        }}
        .sticky-top-filter .stButton > button[kind="secondary"] {{
            background: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(120, 136, 190, 0.14) !important;
            color: #ecf6ff !important;
        }}
        .sticky-side-filter {{
            position: sticky;
            top: 0.8rem;
            z-index: 35;
            padding: 1rem;
            border-radius: 22px;
            background: rgba(21,24,38,0.95);
            border: 1px solid rgba(120, 136, 190, 0.15);
            backdrop-filter: blur(14px);
            box-shadow: 0 18px 42px rgba(0,0,0,0.22);
        }}
        .sticky-side-filter [data-testid="stCheckbox"] label p {{
            font-size: 0.82rem !important;
            line-height: 1.15 !important;
        }}
        .sticky-side-filter [data-testid="stCheckbox"] {{
            margin-bottom: -0.2rem;
        }}
        .filter-label {{
            color: white;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            margin-bottom: 0.45rem;
        }}
        .filter-copy {{
            color: var(--muted);
            font-size: 0.9rem;
            line-height: 1.6;
            margin-bottom: 0.7rem;
        }}
        .stButton > button {{
            width: 100%;
            border-radius: 999px;
            border: 1px solid rgba(120, 136, 190, 0.20);
            background: linear-gradient(90deg, rgba(86,141,255,0.12), rgba(155,85,255,0.16));
            color: white;
            font-weight: 700;
            box-shadow: 0 0 20px rgba(86,141,255,0.08);
        }}
        .stButton > button:hover {{
            border-color: rgba(155,85,255,0.42);
            box-shadow: 0 0 26px rgba(155,85,255,0.14);
        }}
        [data-testid="stDataFrame"] {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(120, 136, 190, 0.14);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_main_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [col.replace("\ufeff", "").strip() for col in df.columns]

    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ["trending_date", "publish_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    df["category_name"] = df["category_name"].fillna("Unknown")
    df["channel_title"] = df["channel_title"].fillna("Unknown Channel")
    return df


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
    score = (sum(token in positive_words for token in tokens) - sum(token in negative_words for token in tokens))
    return float(np.clip(score / max(len(tokens), 1) * 4, -1, 1))


@st.cache_data(show_spinner=False)
def load_comment_sentiment(path: Path, sample_size: int = 10000) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()

    comments = pd.read_csv(path, on_bad_lines="skip")
    comments.columns = [col.replace("\ufeff", "").strip() for col in comments.columns]
    if "comment_text" not in comments.columns:
        return pd.DataFrame()

    comments = comments.dropna(subset=["comment_text"]).copy()
    if len(comments) > sample_size:
        comments = comments.sample(sample_size, random_state=42)

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
    )
    return comments


def filter_comments_to_videos(comments_df: pd.DataFrame, video_ids: pd.Series) -> pd.DataFrame:
    if comments_df.empty or "video_id" not in comments_df.columns:
        return comments_df
    return comments_df[comments_df["video_id"].isin(set(video_ids.dropna().astype(str)))]


def validate_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        st.error(f"Missing required columns in `full_df.csv`: {', '.join(missing)}")
        st.stop()


def fmt_number(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:,.0f}"


def fmt_pct(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.2%}"


def section_header(title: str, copy: str) -> None:
    st.markdown(f'<h2 class="section-title">{title}</h2>', unsafe_allow_html=True)
    st.markdown(f'<p class="section-copy">{copy}</p>', unsafe_allow_html=True)


def insight(text: str) -> None:
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)


def pretty_label(name: str) -> str:
    return DISPLAY_LABELS.get(name, name.replace("_", " ").title())


def pretty_labels(names: Iterable[str]) -> dict[str, str]:
    return {name: pretty_label(name) for name in names}


def apply_plotly_defaults() -> None:
    px.defaults.template = "plotly_dark"
    px.defaults.color_discrete_sequence = [
        COLORS["cyan"], COLORS["blue"], COLORS["purple"], COLORS["pink"], COLORS["gold"]
    ]


@st.cache_data(show_spinner=False)
def filter_data(
    df: pd.DataFrame,
    selected_categories: tuple[str, ...],
    selected_channels: tuple[str, ...],
    min_views: int,
    max_views: int,
) -> pd.DataFrame:
    filtered = df.copy()
    if selected_categories:
        filtered = filtered[filtered["category_name"].isin(selected_categories)]
    if selected_channels:
        filtered = filtered[filtered["channel_title"].isin(selected_channels)]
    filtered = filtered[filtered["views"].between(min_views, max_views)]
    return filtered


@st.cache_data(show_spinner=False)
def summarize_channels(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("channel_title", as_index=False)
        .agg(total_views=("views", "sum"), total_likes=("likes", "sum"), videos=("video_id", "count"))
        .sort_values("total_views", ascending=False)
    )


@st.cache_data(show_spinner=False)
def summarize_categories(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category_name", as_index=False)
        .agg(avg_like_rate=("like_rate", "mean"), avg_comment_rate=("comment_count_rate", "mean"), videos=("video_id", "count"))
        .sort_values("avg_like_rate", ascending=False)
    )


@st.cache_data(show_spinner=False)
def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    corr_df = df[NUMERIC_COLUMNS].corr(numeric_only=True)
    return corr_df.rename(index=pretty_label, columns=pretty_label)


@st.cache_data(show_spinner=False)
def sample_for_scatter(df: pd.DataFrame, max_points: int = 2500) -> pd.DataFrame:
    if len(df) <= max_points:
        return df
    return df.sample(max_points, random_state=42)


def polish_plotly(fig, height: int, title: str | None = None, legend_y: float = 1.02, top_margin: int = 90):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
        margin=dict(l=20, r=20, t=top_margin, b=20),
        legend=dict(
            bgcolor="rgba(7,17,31,0.0)",
            orientation="h",
            yanchor="bottom",
            y=legend_y,
            xanchor="right",
            x=1,
        ),
    )
    if title is not None:
        fig.update_layout(title=dict(text=title, x=0.02, xanchor="left"))
    return fig


def polish_category_legend(fig, height: int, title: str, legend_y: float = 1.16, top_margin: int = 150):
    fig = polish_plotly(fig, height, title, legend_y=legend_y, top_margin=top_margin)
    fig.update_layout(
        legend_title_text="",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            bgcolor="rgba(12,16,28,0.75)",
            bordercolor="rgba(120, 136, 190, 0.16)",
            borderwidth=1,
            tracegroupgap=6,
        ),
        margin=dict(l=20, r=220, t=top_margin, b=20),
    )
    return fig


def render_sidebar_nav() -> str:
    pages = (
        "Overview",
        "Content Patterns",
        "Channel & Category Explorer",
        "Audience Sentiment",
        "Word Clouds",
        "Final Takeaway",
    )
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = "Overview"

    st.sidebar.markdown(
        """
        <div class="sidebar-brand-card">
            <div class="icon">📺</div>
            <div class="title">YouTube Pulse</div>
            <div class="badge">Strategy Dashboard</div>
            <div class="copy">
                A professional analytics interface for evaluating YouTube reach, engagement efficiency,
                creator performance, and audience response at both strategic and exploratory levels.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_page = st.sidebar.radio(
        "Navigation",
        pages,
        key="active_page",
        label_visibility="collapsed",
    )

    st.sidebar.markdown(
        """
        <div class="sidebar-contact-card">
            <div class="title">Connect</div>
            <div class="role">
                Mir Shahadut Hossain<br/>
                Data Analyst | Streamlit Developer
            </div>
            <a class="contact-link" href="https://www.linkedin.com/in/mir-shahadut-hossain/" target="_blank">
                <span class="contact-label">LinkedIn</span>
                <span class="contact-value">mir-shahadut-hossain</span>
            </a>
            <a class="contact-link" href="https://github.com/doyancha" target="_blank">
                <span class="contact-label">GitHub</span>
                <span class="contact-value">github.com/doyancha</span>
            </a>
            <a class="contact-link" href="mailto:sujon6901@gmail.com">
                <span class="contact-label">Email</span>
                <span class="contact-value">sujon6901@gmail.com</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return active_page


def render_hero(df: pd.DataFrame) -> None:
    st.markdown(
        f"""
        <div class="hero overview-hero">
            <div class="hero-badge">YouTube Performance Intelligence</div>
            <h1>YouTube Engagement Performance Analysis</h1>
            <p>
                This dashboard reframes the project around a tighter story: audience reach, interaction quality,
                top-performing creators and categories, and the emotional tone of viewer responses. The current
                view analyzes <strong>{len(df):,}</strong> trending video records.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_intro(title: str, copy: str, badge: str = "Insight View") -> None:
    st.markdown(
        f"""
        <div class="section-card page-intro-card" style="margin-bottom: 1rem; text-align: center;">
            <div class="hero-badge">{badge}</div>
            <h2 style="margin-top:0.9rem; margin-bottom:0.55rem;">{title}</h2>
            <p class="section-copy" style="margin-bottom:0; max-width: 860px; margin-left: auto; margin-right: auto;">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chip_label(text: str) -> str:
    replacements = {
        "Autos & Vehicles": "Autos &\nVehicles",
        "News & Politics": "News &\nPolitics",
        "People & Blogs": "People &\nBlogs",
        "Pets & Animals": "Pets &\nAnimals",
        "Science & Technology": "Science &\nTechnology",
        "Travel & Events": "Travel &\nEvents",
        "Film & Animation": "Film &\nAnimation",
        "Howto & Style": "Howto &\nStyle",
    }
    return replacements.get(text, text)


def category_chip_text(text: str, selected: bool) -> str:
    base = chip_label(text)
    return f"Selected\n{base}" if selected else base


def render_kpis(df: pd.DataFrame) -> None:
    kpis = [
        ("Total Views", fmt_number(df["views"].sum()), "Overall audience reach"),
        ("Total Likes", fmt_number(df["likes"].sum()), "Positive response volume"),
        ("Total Comments", fmt_number(df["comment_count"].sum()), "Conversation generated"),
        ("Avg Like Rate", fmt_pct(df["like_rate"].mean()), "Likes per view"),
        ("Avg Comment Rate", fmt_pct(df["comment_count_rate"].mean()), "Comments per view"),
        ("Active Categories", fmt_number(df["category_name"].nunique()), "Content breadth in scope"),
    ]
    cols = st.columns(6)
    for col, (label, value, note) in zip(cols, kpis):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def initialize_explorer_state(df: pd.DataFrame) -> None:
    if "explorer_categories" not in st.session_state:
        st.session_state["explorer_categories"] = sorted(df["category_name"].dropna().unique().tolist())
    if "explorer_channels" not in st.session_state:
        st.session_state["explorer_channels"] = []


def render_explorer_filters(df: pd.DataFrame) -> pd.DataFrame:
    initialize_explorer_state(df)

    all_categories = sorted(df["category_name"].dropna().unique().tolist())
    top_channels = (
        df.groupby("channel_title")["video_id"]
        .count()
        .sort_values(ascending=False)
        .head(20)
        .index.tolist()
    )

    selected_categories = list(st.session_state["explorer_categories"])
    selected_channels = list(st.session_state["explorer_channels"])

    st.markdown('<div class="sticky-top-filter">', unsafe_allow_html=True)
    st.markdown('<div class="filter-label">Category Selection</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="filter-copy">Pick the content categories you want to compare. This bar stays visible while you scroll through the explorer page.</div>',
        unsafe_allow_html=True,
    )
    top_actions = st.columns([1, 1, 4])
    with top_actions[0]:
        all_categories_clicked = st.button("All Categories", key="all_categories_btn", use_container_width=True)
    with top_actions[1]:
        clear_categories_clicked = st.button("Clear Categories", key="clear_categories_btn", use_container_width=True)

    if all_categories_clicked:
        selected_categories = all_categories
    elif clear_categories_clicked:
        selected_categories = []

    selected_category_set = set(selected_categories)
    if all_categories_clicked:
        selected_category_set = set(all_categories)
    elif clear_categories_clicked:
        selected_category_set = set()

    category_cols = st.columns(9)
    for idx, category in enumerate(all_categories):
        is_selected = category in selected_category_set
        if category_cols[idx % 9].button(
            category_chip_text(category, is_selected),
            key=f"explorer_cat_btn_{category}",
            type="primary" if is_selected else "secondary",
            use_container_width=True,
        ):
            if category in selected_category_set:
                selected_category_set.remove(category)
            else:
                selected_category_set.add(category)

    new_selected_categories = [category for category in all_categories if category in selected_category_set]
    st.markdown(
        f'<div class="filter-copy" style="margin-top:0.55rem; margin-bottom:0;">Selected categories: <strong>{len(new_selected_categories)}</strong> of <strong>{len(all_categories)}</strong></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    right_col_selected_channels: list[str] = []
    content_col, channel_col = st.columns([3.9, 1.75], gap="large")

    with channel_col:
        st.markdown('<div class="sticky-side-filter">', unsafe_allow_html=True)
        st.markdown('<div class="filter-label">Top 20 Channels</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="filter-copy">Use these creator checkboxes to narrow the explorer without leaving the page.</div>',
            unsafe_allow_html=True,
        )
        channel_actions = st.columns(2)
        with channel_actions[0]:
            all_channels_clicked = st.button("All", key="all_channels_btn", use_container_width=True)
        with channel_actions[1]:
            clear_channels_clicked = st.button("Clear", key="clear_channels_btn", use_container_width=True)

        if all_channels_clicked:
            selected_channels = top_channels
        elif clear_channels_clicked:
            selected_channels = []

        channel_cols = st.columns(2)
        for idx, channel in enumerate(top_channels):
            channel_key = f"explorer_channel_{channel}"
            if all_channels_clicked:
                st.session_state[channel_key] = True
            elif clear_channels_clicked:
                st.session_state[channel_key] = False

            if channel_cols[idx % 2].checkbox(
                channel,
                value=channel in selected_channels,
                key=channel_key,
            ):
                right_col_selected_channels.append(channel)
        st.markdown('</div>', unsafe_allow_html=True)

    st.session_state["explorer_categories"] = new_selected_categories
    st.session_state["explorer_channels"] = right_col_selected_channels

    filtered_df = filter_data(
        df,
        tuple(st.session_state["explorer_categories"]),
        tuple(st.session_state["explorer_channels"]),
        int(df["views"].min()),
        int(df["views"].max()),
    )
    return filtered_df, content_col


def render_engagement_drivers(df: pd.DataFrame) -> None:
    section_header(
        "What Drives Engagement",
        "This section focuses on the strongest signals behind YouTube performance: reach-to-like behavior, rate-based correlations, and the relationship between title punctuation and response intensity.",
    )

    left, right = st.columns([1.15, 0.85])
    scatter_df = sample_for_scatter(df)

    with left:
        fig = px.scatter(
            scatter_df,
            x="views",
            y="likes",
            size="comment_count",
            color="category_name",
            hover_name="title" if "title" in df.columns else "channel_title",
            opacity=0.78,
            title="Reach vs Like Conversion",
            labels=pretty_labels(["views", "likes", "comment_count", "category_name"]),
        )
        fig = polish_category_legend(fig, 520, "Reach vs Like Conversion", legend_y=1.18, top_margin=160)
        st.plotly_chart(fig, use_container_width=True)
        corr = df[["views", "likes"]].corr().iloc[0, 1]
        insight(
            f"Views and likes move together with a correlation of <strong>{corr:.2f}</strong>. In practical terms, reach is a major performance engine, but the spread around the curve shows that some videos are materially better at converting exposure into visible appreciation."
        )

    with right:
        corr_df = correlation_matrix(df)
        fig, ax = plt.subplots(figsize=(7, 5.5))
        sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="mako", linewidths=0.4, ax=ax)
        fig.patch.set_facecolor("#07111f")
        ax.set_facecolor("#07111f")
        ax.tick_params(colors="white")
        ax.set_title("Rate and Volume Correlations", color="white", pad=12)
        st.pyplot(fig, clear_figure=True)
        insight(
            "Rate metrics are often more decision-useful than raw counts because they compare performance quality across videos of very different sizes."
        )

    fig = px.box(
        df,
        x="category_name",
        y="like_rate",
        color="category_name",
        title="Which Categories Sustain Stronger Like Rates?",
        points=False,
        labels=pretty_labels(["category_name", "like_rate"]),
    )
    fig = polish_plotly(fig, 500, "Which Categories Sustain Stronger Like Rates?")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    best_category = df.groupby("category_name")["like_rate"].mean().sort_values(ascending=False).index[0]
    insight(
        f"<strong>{best_category}</strong> currently leads on average like rate, which suggests category positioning is not just a labeling exercise. It meaningfully changes how efficiently views turn into approval."
    )

    punc_corr = df["punc_count"].corr(df["comment_count"])
    fig = px.scatter(
        scatter_df,
        x="punc_count",
        y="comment_count",
        color="category_name",
        title="Does Expressive Packaging Drive More Discussion?",
        opacity=0.7,
        labels=pretty_labels(["punc_count", "comment_count", "category_name"]),
    )
    fig = polish_category_legend(fig, 470, "Does Expressive Packaging Drive More Discussion?", legend_y=1.20, top_margin=165)
    st.plotly_chart(fig, use_container_width=True)
    insight(
        f"Punctuation count has a <strong>{punc_corr:.2f}</strong> correlation with comment volume in the current view. It is not a primary growth lever on its own, but it may indicate more emotionally packaged titles that prompt stronger audience reaction."
    )


def render_overview_analytics(df: pd.DataFrame) -> None:
    section_header(
        "Core Performance Signals",
        "These three visuals summarize the project at a glance: how reach converts into likes, where channel-level trend visibility concentrates, and how the main engagement variables move together.",
    )

    scatter_df = sample_for_scatter(df)
    fig = px.scatter(
        scatter_df,
        x="views",
        y="likes",
        size="comment_count",
        color="category_name",
        hover_name="title" if "title" in df.columns else "channel_title",
        opacity=0.78,
        title="Relationship Between Views and Likes",
        labels=pretty_labels(["views", "likes", "comment_count", "category_name"]),
    )
    fig = polish_category_legend(fig, 450, "Relationship Between Views and Likes", legend_y=1.20, top_margin=165)
    st.plotly_chart(fig, use_container_width=True)

    views_likes_corr = df[["views", "likes"]].corr().iloc[0, 1]
    insight(
        f"The relationship between views and likes is strong at <strong>{views_likes_corr:.2f}</strong>. This tells us that scale is still the biggest engine of visible engagement, but conversion quality varies from one video cluster to another."
    )

    paired_left, paired_right = st.columns(2, gap="large")

    top_trending_channels = (
        df.groupby("channel_title", as_index=False)
        .agg(trending_videos=("video_id", "count"), total_views=("views", "sum"))
        .sort_values("trending_videos", ascending=False)
        .head(20)
    )

    with paired_left:
        fig = px.bar(
            top_trending_channels.head(12),
            x="trending_videos",
            y="channel_title",
            orientation="h",
            color="total_views",
            title="Top Trending Channels by Number of Records",
            color_continuous_scale=[COLORS["blue"], COLORS["cyan"], COLORS["gold"]],
            hover_data=["total_views"],
            labels=pretty_labels(["trending_videos", "channel_title", "total_views"]),
        )
        fig = polish_plotly(fig, 440, "Top Trending Channels by Number of Records", top_margin=95)
        fig.update_layout(yaxis_title="", xaxis_title="Trending Videos", coloraxis_colorbar_title="Total Views")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    with paired_right:
        corr_df = correlation_matrix(df)
        fig, ax = plt.subplots(figsize=(7.6, 5.1))
        sns.heatmap(corr_df, annot=True, fmt=".2f", cmap="mako", linewidths=0.4, ax=ax)
        fig.patch.set_facecolor("#07111f")
        ax.set_facecolor("#07111f")
        ax.tick_params(colors="white", labelsize=8)
        ax.set_title("Correlation Heatmap", color="white", pad=14)
        st.pyplot(fig, clear_figure=True)

    leading_channel = top_trending_channels.iloc[0]["channel_title"]
    leading_count = int(top_trending_channels.iloc[0]["trending_videos"])
    insight(
        f"This overview suggests three things clearly: <strong>{leading_channel}</strong> shows the strongest recurring trending presence with <strong>{leading_count}</strong> appearances, view growth is closely tied to like accumulation, and rate-based metrics remain essential for comparing content quality beyond raw scale."
    )


def render_top_performers(df: pd.DataFrame) -> None:
    section_header(
        "Top Channels & Categories",
        "Instead of listing everything, this section highlights where performance is concentrating: the creators pulling the most reach and the categories delivering the strongest engagement efficiency.",
    )

    channel_summary = summarize_channels(df).head(10)
    category_summary = summarize_categories(df)

    left, right = st.columns(2)

    with left:
        fig = px.bar(
            channel_summary,
            x="total_views",
            y="channel_title",
            orientation="h",
            color="total_likes",
            title="Top Channels by Total Views",
            color_continuous_scale=[COLORS["blue"], COLORS["cyan"], COLORS["pink"]],
            hover_data=["videos"],
            labels=pretty_labels(["total_views", "channel_title", "total_likes", "videos"]),
        )
        fig = polish_plotly(fig, 500, "Top Channels by Total Views")
        fig.update_layout(yaxis_title="", xaxis_title="Total Views", coloraxis_colorbar_title="Likes")
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        category_plot = category_summary.rename(
            columns={
                "avg_like_rate": pretty_label("avg_like_rate"),
                "avg_comment_rate": pretty_label("avg_comment_rate"),
                "category_name": pretty_label("category_name"),
            }
        )
        fig = px.bar(
            category_plot,
            x=pretty_label("category_name"),
            y=[pretty_label("avg_like_rate"), pretty_label("avg_comment_rate")],
            barmode="group",
            title="Category Efficiency: Likes and Comments per View",
            color_discrete_sequence=[COLORS["cyan"], COLORS["purple"]],
        )
        fig = polish_plotly(fig, 500, "Category Efficiency: Likes and Comments per View")
        fig.update_layout(xaxis_title="Category", yaxis_title="Average Rate")
        st.plotly_chart(fig, use_container_width=True)

    leader = channel_summary.iloc[0]["channel_title"]
    leading_category = category_summary.iloc[0]["category_name"]
    insight(
        f"<strong>{leader}</strong> dominates on accumulated view scale, while <strong>{leading_category}</strong> leads on engagement efficiency. For strategy, that distinction matters: the biggest attention winners are not always the strongest interaction winners."
    )


def render_explorer_page(df: pd.DataFrame, comments_df: pd.DataFrame) -> None:
    render_page_intro(
        "Channel & Category Explorer",
        "This is the only page where filtering lives. Categories stay pinned at the top, channels stay pinned on the right, and the charts below update around those selections.",
        badge="Explorer",
    )
    filtered_df, content_col = render_explorer_filters(df)

    with content_col:
        if filtered_df.empty:
            st.warning("No records match the current category and channel selections.")
            return

        render_kpis(filtered_df)
        render_top_performers(filtered_df)

        scatter_df = sample_for_scatter(filtered_df)
        fig = px.scatter(
            scatter_df,
            x="views",
            y="likes",
            color="category_name",
            size="comment_count",
            hover_name="title" if "title" in filtered_df.columns else "channel_title",
            labels=pretty_labels(["views", "likes", "comment_count", "category_name"]),
            title="Filtered Reach vs Like Conversion",
        )
        fig = polish_category_legend(fig, 520, "Filtered Reach vs Like Conversion", legend_y=1.18, top_margin=160)
        st.plotly_chart(fig, use_container_width=True)

        filtered_comments = filter_comments_to_videos(comments_df, filtered_df["video_id"].astype(str))
        if not filtered_comments.empty:
            sentiment_share = (filtered_comments["sentiment_label"] == "Positive").mean()
            insight(
                f"Within the active explorer selection, <strong>{sentiment_share:.1%}</strong> of sampled comments are positive. That helps connect creator and category performance with audience tone."
            )


def render_audience_sentiment(comments_df: pd.DataFrame) -> None:
    section_header(
        "Audience Sentiment",
        "Quantitative engagement tells us that people reacted. Sentiment helps estimate how that reaction felt by sampling the emotional tone of comments.",
    )

    if comments_df.empty:
        st.markdown(
            """
            <div class="section-card">
                Sentiment charts are unavailable because the comments file or sentiment analyzer could not be loaded.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    left, right = st.columns(2)
    with left:
        sentiment_mix = (
            comments_df["sentiment_label"].value_counts(dropna=False).rename_axis("sentiment").reset_index(name="count")
        )
        fig = px.pie(
            sentiment_mix,
            names="sentiment",
            values="count",
            title="Comment Sentiment Mix",
            color="sentiment",
            color_discrete_map={
                "Positive": COLORS["cyan"],
                "Neutral": COLORS["purple"],
                "Negative": COLORS["pink"],
            },
        )
        fig = polish_plotly(fig, 430, "Comment Sentiment Mix")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.histogram(
            comments_df,
            x="sentiment_score",
            nbins=45,
            title="Sentiment Score Distribution",
            color_discrete_sequence=[COLORS["blue"]],
            labels=pretty_labels(["sentiment_score"]),
        )
        fig = polish_plotly(fig, 430, "Sentiment Score Distribution")
        st.plotly_chart(fig, use_container_width=True)

    positive_share = (comments_df["sentiment_label"] == "Positive").mean()
    negative_share = (comments_df["sentiment_label"] == "Negative").mean()
    insight(
        f"The sampled audience is <strong>{positive_share:.1%}</strong> positive versus <strong>{negative_share:.1%}</strong> negative. That points to a healthier engagement profile, where strong attention is not being driven only by negative sentiment or backlash."
    )


def render_punctuation_impact(df: pd.DataFrame) -> None:
    section_header(
        "Punctuation Impact",
        "This combined view compares how punctuation count relates to views, likes, dislikes, and comment count. It works as a supporting behavioral signal rather than a standalone performance driver.",
    )
    metrics = ["views", "likes", "dislikes", "comment_count"]
    scatter_df = sample_for_scatter(df, max_points=2200)
    long_df = scatter_df.melt(
        id_vars=["punc_count"],
        value_vars=metrics,
        var_name="metric",
        value_name="value",
    )
    long_df["metric"] = long_df["metric"].map(pretty_label)

    fig = px.scatter(
        long_df,
        x="punc_count",
        y="value",
        color="metric",
        facet_col="metric",
        facet_col_wrap=2,
        opacity=0.65,
        labels={"punc_count": pretty_label("punc_count"), "value": "Value", "metric": "Metric"},
        title="Impact of Punctuation Count on Key Engagement Metrics",
    )
    fig = polish_plotly(fig, 720, "Impact of Punctuation Count on Key Engagement Metrics", legend_y=1.06, top_margin=120)
    fig.update_xaxes(title_text=pretty_label("punc_count"))
    fig.update_yaxes(matches=None)
    st.plotly_chart(fig, use_container_width=True)

    correlations = {pretty_label(metric): df["punc_count"].corr(df[metric]) for metric in metrics}
    strongest_metric = max(correlations, key=lambda name: abs(correlations[name]))
    insight(
        f"Among the four metrics, punctuation count has its strongest relationship with <strong>{strongest_metric}</strong>. This is best interpreted as a packaging cue: expressive formatting may amplify audience response, but it does not replace content quality or distribution scale."
    )


@st.cache_data(show_spinner=False)
def build_wordcloud_texts(comments_df: pd.DataFrame) -> tuple[str, str]:
    if comments_df.empty or "comment_text" not in comments_df.columns:
        return "", ""

    positive_comments = comments_df[comments_df["sentiment_label"] == "Positive"]["comment_text"].astype(str)
    negative_comments = comments_df[comments_df["sentiment_label"] == "Negative"]["comment_text"].astype(str)
    return " ".join(positive_comments.tolist()), " ".join(negative_comments.tolist())


def extract_top_terms(text: str, limit: int = 12) -> pd.DataFrame:
    stopwords = set(STOPWORDS) if STOPWORDS else set()
    stopwords.update(
        {
            "video", "channel", "youtube", "one", "like", "really", "would", "much",
            "get", "got", "make", "made", "know", "still", "amp",
        }
    )
    words = [
        token.strip(".,!?;:()[]{}\"'").lower()
        for token in text.split()
        if len(token.strip(".,!?;:()[]{}\"'")) > 3
    ]
    filtered = [word for word in words if word and word not in stopwords and word.isalpha()]
    common = Counter(filtered).most_common(limit)
    return pd.DataFrame(common, columns=["term", "count"])


def render_wordcloud_figure(text: str, accent: str, title: str):
    if not text or WordCloud is None:
        st.info(f"{title} is unavailable because usable comment text or the `wordcloud` package was not found.")
        return

    wc = WordCloud(
        width=1200,
        height=620,
        background_color="#121723",
        colormap=accent,
        stopwords=set(STOPWORDS) if STOPWORDS else None,
        collocations=False,
        max_words=120,
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    fig.patch.set_facecolor("#121723")
    ax.set_facecolor("#121723")
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title, color="white", fontsize=14, pad=14)
    st.pyplot(fig, clear_figure=True)


def render_wordcloud_page(comments_df: pd.DataFrame) -> None:
    render_page_intro(
        "Audience Language Patterns",
        "This page highlights how viewers describe their reactions in their own words. Positive and negative word clouds surface repeated themes in the comment stream, while the supporting keyword tables help translate visual patterns into analyst-ready signals.",
        badge="Word Clouds",
    )

    if comments_df.empty:
        st.markdown(
            """
            <div class="section-card">
                Word cloud analysis is unavailable because comment sentiment data could not be loaded for this run.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    positive_text, negative_text = build_wordcloud_texts(comments_df)
    cloud_left, cloud_right = st.columns(2, gap="large")

    with cloud_left:
        render_wordcloud_figure(positive_text, "winter", "Positive Comment Word Cloud")

    with cloud_right:
        render_wordcloud_figure(negative_text, "magma", "Negative Comment Word Cloud")

    positive_terms = extract_top_terms(positive_text)
    negative_terms = extract_top_terms(negative_text)
    term_left, term_right = st.columns(2, gap="large")

    with term_left:
        fig = px.bar(
            positive_terms,
            x="count",
            y="term",
            orientation="h",
            title="Most Frequent Positive Terms",
            color_discrete_sequence=[COLORS["cyan"]],
            labels={"count": "Mentions", "term": "Term"},
        )
        fig = polish_plotly(fig, 420, "Most Frequent Positive Terms", top_margin=90)
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    with term_right:
        fig = px.bar(
            negative_terms,
            x="count",
            y="term",
            orientation="h",
            title="Most Frequent Negative Terms",
            color_discrete_sequence=[COLORS["pink"]],
            labels={"count": "Mentions", "term": "Term"},
        )
        fig = polish_plotly(fig, 420, "Most Frequent Negative Terms", top_margin=90)
        fig.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig, use_container_width=True)

    insight(
        "The word clouds provide a qualitative layer to the dashboard by surfacing repeated audience language. When the most frequent positive terms align with strong engagement rates, it reinforces the case that attention is being driven by favorable reception rather than noise alone."
    )


def render_takeaway(df: pd.DataFrame, comments_df: pd.DataFrame) -> None:
    section_header(
        "Final Analyst Takeaway",
        "The goal of this dashboard is not to show every chart possible. It is to leave one clear interpretation of what appears to matter most in this YouTube dataset.",
    )

    top_category = df.groupby("category_name")["like_rate"].mean().sort_values(ascending=False).index[0]
    top_channel = df.groupby("channel_title")["views"].sum().sort_values(ascending=False).index[0]
    avg_like_rate = df["like_rate"].mean()
    avg_comment_rate = df["comment_count_rate"].mean()
    positive_share = (comments_df["sentiment_label"] == "Positive").mean() if not comments_df.empty else np.nan

    st.markdown(
        f"""
        <div class="section-card">
            <p class="section-copy">
                The strongest pattern in this project is that <strong>reach and engagement are related, but not identical</strong>.
                Large channels such as <strong>{top_channel}</strong> dominate attention, yet category-level efficiency still matters,
                with <strong>{top_category}</strong> leading the current view on average like rate.
            </p>
            <p class="section-copy">
                On average, videos convert views into likes at <strong>{avg_like_rate:.2%}</strong> and into comments at
                <strong> {avg_comment_rate:.2%}</strong>. That means content performance should be evaluated not just on scale,
                but on how effectively it turns reach into interaction.
            </p>
            <p class="section-copy">
                {"Sampled comments are directionally positive at <strong>" + f"{positive_share:.1%}" + "</strong>, which strengthens the case that strong performance is often paired with healthy audience response." if not pd.isna(positive_share) else "Comment sentiment was unavailable in this run, so the final takeaway relies on behavioral metrics only."}
            </p>
            <p class="section-copy">
                For a content strategy lens, the clearest takeaway is this: sustainable performance comes from pairing
                discoverable scale with formats that convert attention into likes, comments, and positive audience tone.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    top_category = summarize_categories(df).iloc[0]["category_name"]
    top_channel_row = summarize_channels(df).iloc[0]
    top_channel = top_channel_row["channel_title"]
    top_channel_views = fmt_number(top_channel_row["total_views"])
    recommendation_cols = st.columns(3, gap="large")

    recommendation_cards = [
        (
            "Content Direction",
            f"Double down on content patterns associated with <strong>{top_category}</strong>, since this category currently leads on engagement efficiency rather than just raw visibility.",
        ),
        (
            "Creator Benchmark",
            f"Use <strong>{top_channel}</strong> as a benchmark for sustained audience reach. Its current accumulated view base of <strong>{top_channel_views}</strong> provides a useful reference for scale-oriented comparison.",
        ),
        (
            "Engagement Focus",
            "Prioritize rate-based KPIs alongside raw volume. Likes and comments per view offer a more reliable signal of audience quality than views alone when comparing creators or formats.",
        ),
    ]

    for col, (title, body) in zip(recommendation_cols, recommendation_cards):
        with col:
            st.markdown(
                f"""
                <div class="section-card" style="min-height: 220px;">
                    <h3 style="margin-top:0; margin-bottom:0.65rem; font-size:1rem;">{title}</h3>
                    <p class="section-copy" style="margin-bottom:0;">{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def main() -> None:
    inject_css()
    apply_plotly_defaults()

    if not DATA_PATH.exists():
        st.error("`full_df.csv` was not found beside `app.py`.")
        st.stop()

    df = load_main_data(DATA_PATH)
    validate_columns(
        df,
        [
            "views",
            "likes",
            "dislikes",
            "comment_count",
            "category_name",
            "like_rate",
            "dislike_rate",
            "comment_count_rate",
            "punc_count",
            "channel_title",
            "video_id",
        ],
    )

    active_page = render_sidebar_nav()
    comments_df = load_comment_sentiment(COMMENTS_PATH)

    if active_page == "Overview":
        render_hero(df)
        render_kpis(df)
        render_page_intro(
            "Executive Overview",
            "This landing page presents a high-level view of the YouTube dataset, highlighting overall scale, engagement quality, and the core performance relationships that shape the analysis before moving into more targeted exploration.",
            badge="Overview",
        )
        summary_left, summary_right = st.columns([1.2, 1])
        with summary_left:
            total_views = fmt_number(df["views"].sum())
            total_likes = fmt_number(df["likes"].sum())
            total_comments = fmt_number(df["comment_count"].sum())
            avg_like_rate = fmt_pct(df["like_rate"].mean())
            avg_comment_rate = fmt_pct(df["comment_count_rate"].mean())
            views_likes_corr = df[["views", "likes"]].corr().iloc[0, 1]
            st.markdown(
                f"""
                <div class="section-card">
                    <p class="section-copy">
                        This project analyzes <strong>{len(df):,}</strong> trending-video records spanning
                        <strong> {df["category_name"].nunique():,}</strong> categories and
                        <strong> {df["channel_title"].nunique():,}</strong> channels, representing
                        <strong> {total_views}</strong> views, <strong>{total_likes}</strong> likes, and
                        <strong>{total_comments}</strong> comments in aggregate.
                    </p>
                    <p class="section-copy">
                        At the dataset level, videos convert attention into interaction at an average
                        <strong>{avg_like_rate}</strong> like rate and <strong>{avg_comment_rate}</strong> comment rate,
                        while the relationship between views and likes remains strong at
                        <strong>{views_likes_corr:.2f}</strong>.
                    </p>
                    <p class="section-copy">
                        Use <strong>Content Patterns</strong> for global behavioral signals and
                        <strong> Channel & Category Explorer</strong> for filter-driven comparisons across creators and categories.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with summary_right:
            top_category = summarize_categories(df).iloc[0]["category_name"]
            top_channel = summarize_channels(df).iloc[0]["channel_title"]
            top_channel_views = fmt_number(summarize_channels(df).iloc[0]["total_views"])
            top_category_like_rate = fmt_pct(summarize_categories(df).iloc[0]["avg_like_rate"])
            avg_dislike_rate = fmt_pct(df["dislike_rate"].mean())
            st.markdown(
                f"""
                <div class="section-card">
                    <p class="section-copy"><strong>Fast read</strong></p>
                    <p class="section-copy">Top category by like-rate efficiency: <strong>{top_category}</strong> at <strong>{top_category_like_rate}</strong></p>
                    <p class="section-copy">Top channel by accumulated views: <strong>{top_channel}</strong> with <strong>{top_channel_views}</strong></p>
                    <p class="section-copy">Average comment-rate across the dataset: <strong>{fmt_pct(df["comment_count_rate"].mean())}</strong></p>
                    <p class="section-copy">Average dislike-rate across the dataset: <strong>{avg_dislike_rate}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        render_overview_analytics(df)
    elif active_page == "Content Patterns":
        render_page_intro(
            "Content Patterns",
            "This page focuses on global engagement behavior across the whole dataset. It intentionally ignores channel and category picking so the patterns remain stable and fast to load.",
            badge="Patterns",
        )
        render_engagement_drivers(df)
    elif active_page == "Channel & Category Explorer":
        render_explorer_page(df, comments_df)
    elif active_page == "Audience Sentiment":
        render_page_intro(
            "Audience Sentiment",
            "This page reads the emotional tone of sampled comments at the full-dataset level so it remains lightweight and easy to interpret.",
            badge="Sentiment",
        )
        render_audience_sentiment(comments_df)
        render_punctuation_impact(df)
    elif active_page == "Word Clouds":
        render_wordcloud_page(comments_df)
    else:
        render_page_intro(
            "Final Takeaway",
            "A concise end-state summary of what appears to matter most in the dataset after considering scale, interaction quality, creator performance, and audience tone.",
            badge="Conclusion",
        )
        render_takeaway(df, comments_df)

    st.markdown(
        """
        <div class="footer">
            <strong>YouTube Data Analysis Dashboard</strong><br/>
            An analytics solution focused on YouTube reach, engagement efficiency, creator performance, and audience response.<br/>
            Developed by <a href="https://www.linkedin.com/in/mir-shahadut-hossain/" target="_blank" style="color:#54f3ff; text-decoration:none;">Mir Shahadut Hossain</a>
            •
            <a href="https://github.com/doyancha" target="_blank" style="color:#54f3ff; text-decoration:none;">GitHub</a>
            •
            <a href="mailto:sujon6901@gmail.com" style="color:#54f3ff; text-decoration:none;">Email</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
