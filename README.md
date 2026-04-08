<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=300&section=header&text=YouTube%20Analytics%20Dashboard&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Transforming%20Raw%20Trending%20Data%20into%20Strategic%20Intelligence&descAlignY=58&descSize=18" width="100%"/>

</div>

<div align="center">
</p>
  <a href="https://www.linkedin.com/in/mir-shahadut-hossain/"><img src="https://img.shields.io/badge/LinkedIn-Mir%20Shahadut%20Hossain-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://github.com/doyancha"><img src="https://img.shields.io/badge/GitHub-doyancha-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="mailto:sujon6901@gmail.com"><img src="https://img.shields.io/badge/Email-sujon6901%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://youtube-data-analysis.streamlit.app/"><img src="https://img.shields.io/badge/Live%20App-Streamlit%20Deployment-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live App"></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-Data%20Analysis-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-Data%20Wrangling-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Plotly-Interactive%20Visuals-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Seaborn-Statistical%20Charts-4C72B0?style=flat-square" alt="Seaborn">
</p>


</div>

---

<div align="center">

<div align="center">

<h2 style="margin-bottom: 14px;">⚡ THE CORE QUESTION</h2>

<div style="display: inline-block; padding: 18px 24px; border-radius: 18px; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); border: 1px solid #334155; box-shadow: 0 10px 30px rgba(0,0,0,0.25);">
  <pre style="margin: 0; color: #e2e8f0; font-size: 15px; line-height: 1.5; font-family: Consolas, Monaco, monospace; text-align: left;">
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║        How does YouTube content convert VISIBILITY into ENGAGEMENT       ║
║                         and AUDIENCE RESPONSE?                           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
  </pre>
</div>

</div>


---

## Executive Summary

This project transforms large-scale YouTube trending and comment data into a polished Streamlit analytics experience focused on one core question:

> **How does YouTube content convert visibility into engagement and audience response?**

The app combines engagement metrics, creator/category comparisons, correlation analysis, sentiment evaluation, and word cloud exploration to provide both strategic and exploratory insight across the YouTube ecosystem.

---

## 📌 Table of Contents

| # | Section |
|---|---------|
| 01 | [🎯 Project Intention & Goals](#-project-intention--goals) |
| 02 | [📊 Dataset at a Glance](#-dataset-at-a-glance) |
| 03 | [🔬 Analysis Modules](#-analysis-modules) |
| 04 | [💡 Key Findings](#-key-findings) |
| 05 | [🧠 Technical Pipeline](#-technical-pipeline) |
| 06 | [📁 Repository Structure](#-repository-structure) |
| 07 | [🚀 Run Locally](#-run-locally) |
| 08 | [📸 Dashboard Preview](#-dashboard-preview) |
| 09 | [👤 About the Author](#-about-the-author) |
| 10 | [📚 Suggested Resources](#-suggested-resources) |

---

  
## 🎯 Project Intention & Goals

> This project was built to go **beyond surface-level metrics** — treating YouTube's trending data not as a curiosity, but as a mirror into how digital content earns and sustains public attention.

### 🔭 What This Project Sets Out To Do

<div align="left">
  
- 📌 **Decode engagement dynamics** also understand whether a video truly *earns* its views or just stumbles into them
- 📌 **Profile creator momentum** and identify channels that trend repeatedly versus those with one-off spikes
- 📌 **Measure category efficiency** as well as determine which content categories convert visibility into actual engagement most effectively
- 📌 **Analyze audience sentiment** and go beyond likes/dislikes to understand the *emotional tone* of comment sections at scale
- 📌 **Explore language signals** also investigate whether structural cues in video titles (like punctuation) correlate with stronger audience reactions
- 📌 **Build a production-grade dashboard** not just a notebook, but a fully deployed, stakeholder-ready analytics application
- 📌 **Demonstrate end-to-end data storytelling** from raw CSV ingestion to interactive visual narrative
</div>

### 🧩 Business Questions Addressed
<div align="left">

- Which content categories drive the strongest **like rates**?
- Which creators sustain **repeated trending** presence over time?
- How strongly are **reach and approval** correlated and where do they diverge?
- What does **comment sentiment** reveal about audience reception beyond raw counts?
- Do **title punctuation patterns** influence engagement metrics?
</div>
---

## 📊 Dataset at a Glance

<div align="center">

| 📹 Metric | 📈 Value |
|-----------|----------|
| **Trending Video Records** | 679,050 |
| **Unique Channels** | 48,183 |
| **Comment Records** | 691,400 |
| **Content Categories** | 17 |
| **Total Views** | 833.11 Billion |
| **Total Likes** | 23.46 Billion |
| **Total Comments** | 2.63 Billion |
| **Views ↔ Likes Correlation** | **0.78** |
| **Countries Covered** | Multiple (US, UK, CA, RU & more) |

</div>

### 🗂️ Data Sources Used

| File | Purpose |
|------|---------|
| `full_df.csv` | Primary enriched video dataset (views, likes, dislikes, rates, punc_count) |
| `comments_data.csv` | Comment-level text for sentiment & word cloud analysis |
| `*_category_id.json` | Maps numeric category IDs to human-readable names |
| `data/youtube_videos.parquet` | Deployment-optimized video data (compressed) |
| `data/comments_sentiment.parquet` | Pre-scored comments for fast cloud loading |

---

## 🔬 Analysis Modules

The notebook is organized into **11 distinct analytical sections**, each building on the previous:

---

### 🧹 Module 1 — Data Ingestion & Cleaning
> *Foundation before insight.*

<div align="left">
  
- Multi-country CSV loading with encoding handling (`utf-8`, `latin-1`, `ISO-8859-1`)
- Null detection and removal via `dropna()`
- Deduplication across merged country datasets
- Export pipeline: `.csv` → `.json` → MySQL DB via SQLAlchemy
</div>
---

### 💬 Module 2 — Sentiment Analysis
> *What does the audience actually feel?*

<div align="left">

- NLTK **VADER** (Valence Aware Dictionary and sEntiment Reasoner) for comment scoring
- Compound score range: `−1.0` (most negative) → `+1.0` (most positive)
- Classification thresholds:
  - **Positive:** `score ≥ 0.5`
  - **Negative:** `score ≤ −0.5`
- Applied to 691,400+ comment records
</div>

<div align="left">
  <pre style="display: inline-block; text-align: left; background: #0f172a; color: #e2e8f0; padding: 16px 20px; border-radius: 14px; border: 1px solid #334155; box-shadow: 0 8px 24px rgba(0,0,0,0.18); font-family: Consolas, monospace; font-size: 14px;">
def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))
    return score['compound']

df['sentiment_score'] = df['comment_text'].apply(get_sentiment)
  </pre>
</div>


---

### ☁️ Module 3 — Word Cloud Generation
> *What language defines positive vs. negative engagement?*

<div align="left">


- Separated corpora: positive comments vs. negative comments
- Stop-word filtering using `wordcloud.STOPWORDS`
- Side-by-side 18×7 matplotlib visualization
- Reveals dominant vocabulary patterns in audience reactions
</div>
---

### 😄 Module 4 — Emoji Frequency Analysis
> *The unspoken language of YouTube comments.*

<div align="left">

- Emoji extraction using the `emoji` library's `emoji_list()` function
- Top-10 most-used emojis ranked by frequency
- Interactive Plotly bar chart for visual exploration
- Provides cultural and emotional context beyond text
</div>
---

### 🗺️ Module 5 — Multi-Country Data Merge
> *Scale before depth.*

<div align="left">

- Iterates all `*videos.csv` files from multiple country datasets
- Unified `full_df` DataFrame with consistent schema
- Shape validation post-merge
</div>
---

### 🏷️ Module 6 — Category Enrichment
> *Numbers mean nothing without context.*

<div align="left">

- Parsed `_category_id.json` to build `cat_dict = {id: name}`
- Mapped numeric IDs to readable labels (e.g., `10` → `"Music"`)
- Seaborn strip plot of `likes` distribution per category
</div>
---

### 📐 Module 7 — Engagement Rate Engineering
> *Raw counts lie. Rates tell the truth.*

<div align="left">
  
Three derived metrics computed as a percentage of views:
</div>
<div align="center">

<h3 style="margin-bottom: 12px; color: #0f172a;">Metric Formulas</h3>

<div style="display: inline-block; padding: 18px 24px; border-radius: 18px; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); border: 1px solid #334155; box-shadow: 0 10px 28px rgba(0,0,0,0.22);">
  <pre style="margin: 0; color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.75; text-align: left;">
like_rate          = (likes / views) × 100
dislike_rate       = (dislikes / views) × 100
comment_count_rate = (comment_count / views) × 100
  </pre>
</div>

</div>
<br>
<div align="left">

- 1×3 subplot grid showing rate distributions per category
- Reveals hidden performers vs. inflated-view content
</div>
---

### 🔗 Module 8 — Correlation Analysis
> *How tightly do these signals move together?*

<div align="left">

Pearson correlation matrix: `views`, `likes`, `dislikes`
Seaborn `regplot` for `views` vs `likes` with regression line
Annotated heatmap for full numeric intuition
</div>
---

### 📺 Module 9 — Channel Trending Analysis
> *Who dominates the trending tab — and how often?*

<div align="left">

`value_counts()` on `channel_title` across all records
Top 20 most-trending channels ranked
Interactive Plotly bar chart with color gradient by count
</div>
---

### ✏️ Module 10 — Punctuation Analysis
> *Does expressive formatting drive stronger reactions?*

<div align="left">

<div style="display: inline-block; padding: 18px 24px; border-radius: 18px; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); border: 1px solid #334155; box-shadow: 0 10px 28px rgba(0,0,0,0.22);">
  <pre style="margin: 0; color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.75; text-align: left;">
def punctuation_count(text):
    return len([char for char in text if char in string.punctuation])

full_df['punc_count'] = full_df['title'].apply(punctuation_count)
  </pre>
</div>

</div>
<br>

<div align="left">

- 2×2 subplot grid: `punc_count` vs `views`, `likes`, `dislikes`, `comment_count`
- Treated as a behavioral signal, not a primary driver

</div>
---

### 💾 Module 11 — Export & Deployment Packaging
> *From notebook to production.*

<div align="left">

- `build_deployment_data.py` script packages raw data into compressed Parquet files
- Eliminates need to upload 600MB+ CSV to cloud
- Streamlit app detects `data/*.parquet` and loads from there automatically
</div>
---

## 💡 Key Findings

> Here's what the data actually says — straight from the analysis.

<div align="left">

### 🔑 Finding 1 — Views & Likes Move Together, But Not Perfectly
The correlation between views and likes is **0.78** which is strong, but not deterministic. Some videos accumulate massive view counts without proportional likes, suggesting passive viewership. The best-performing content earns *active* approval, not just passive impressions.

### 🔑 Finding 2 — Category Efficiency Matters More Than Scale
**Howto & Style** leads all categories in average Like Rate. This means content that *teaches* tends to generate more deliberate, appreciative engagement even when raw view counts are modest compared to Entertainment or Music.

### 🔑 Finding 3 — Trending Success Is Not Random
The channel with the highest recurring trending count was **The Late Show with Stephen Colbert** appearing **710 times** in the dataset. This points to durable creator-level momentum, not viral luck. Consistent content cadence compounds into algorithmic staying power.

### 🔑 Finding 4 — Creator Brand Drives Raw Reach
**NickyJamTV** led in total accumulated views. At the top of the distribution, raw reach is overwhelmingly driven by creator brand strength rather than category or title optimization.

### 🔑 Finding 5 — Sentiment Adds a Layer Beyond Raw Metrics
Positive comments are dominated by words of admiration and entertainment. Negative comments cluster around criticism and controversy. High like counts alone can mask a divided comment section sentiment analysis is the corrective lens.

### 🔑 Finding 6 — Title Punctuation as a Behavioral Signal
Videos with moderate punctuation in titles show marginally higher engagement across all metrics. However, this is a *supporting signal* expressive formatting may correlate with a certain content personality type rather than directly causing engagement.
</div>
---

## 🧠 Technical Pipeline




<div align="center">


<div style="display: inline-block; padding: 20px 24px; border-radius: 18px; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); border: 1px solid #334155; box-shadow: 0 10px 28px rgba(0,0,0,0.22);">
  <pre style="margin: 0; color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.65; text-align: left;">
Raw CSVs (Multi-Country)
        │
        ▼
   Data Cleaning ──────────────────────────────────────────────┐
   (null removal, dedup, encoding handling)                    │
        │                                                      │
        ▼                                                      ▼
Feature Engineering                                    Comment Processing
(like_rate, dislike_rate,                           (VADER sentiment scoring,
 comment_count_rate, punc_count,                     word cloud generation,
 category_name mapping)                              emoji frequency analysis)
        │                                                      │
        └───────────────────┬──────────────────────────────────┘
                            │
                            ▼
                   Analysis & Visualization
              (Seaborn, Matplotlib, Plotly)
                            │
                            ▼
                  Export & Packaging
             (CSV, JSON, MySQL, Parquet)
                            │
                            ▼
               Streamlit Dashboard (6 Pages)
              youtube-data-analysis.streamlit.app
  </pre>
</div>

</div>



### 🛠️ Tech Stack


<table align="center" style="border-collapse: collapse; width: 90%; max-width: 900px; overflow: hidden; border-radius: 14px;">
  <thead>
    <tr>
      <th style="background: #0f172a; color: #ffffff; padding: 14px; border: 1px solid #334155;">Layer</th>
      <th style="background: #0f172a; color: #ffffff; padding: 14px; border: 1px solid #334155;">Tools</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Data Wrangling</strong></td>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>pandas</code>, <code>numpy</code></td>
    </tr>
    <tr>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>NLP / Sentiment</strong></td>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>nltk</code> (VADER), <code>wordcloud</code></td>
    </tr>
    <tr>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Emoji Analysis</strong></td>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>emoji</code>, <code>collections.Counter</code></td>
    </tr>
    <tr>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Visualization</strong></td>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>matplotlib</code>, <code>seaborn</code>, <code>plotly.express</code></td>
    </tr>
    <tr>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Dashboard</strong></td>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>streamlit</code></td>
    </tr>
    <tr>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Database</strong></td>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>sqlalchemy</code>, <code>pymysql</code> (MySQL)</td>
    </tr>
    <tr>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>Deployment Data</strong></td>
      <td style="background: #f8fafc; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>pyarrow</code> (Parquet)</td>
    </tr>
    <tr>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><strong>String Processing</strong></td>
      <td style="background: #eef2ff; padding: 12px 14px; border: 1px solid #cbd5e1;"><code>string</code>, <code>os</code></td>
    </tr>
  </tbody>
</table>




---

## 📁 Repository Structure

<div align="left">

```
Youtube_Data_Analysis/
│
├── 📓 youtube_data_analysis.ipynb   ← Main analysis notebook (225 cells)
├── 🖥️ app.py                        ← Streamlit dashboard (6 pages)
├── ⚙️ build_deployment_data.py      ← Parquet packaging script
├── 📄 comments_data.csv             ← Comment records (691K rows)
├── 📄 full_df.csv                   ← Full cleaned and enriched dataset
├── 📄 requirements.txt              ← Python dependencies
│
├── 📂 data/
│   ├── youtube_videos.parquet       ← Compressed video dataset
│   └── comments_sentiment.parquet   ← Pre-scored comment dataset
│
├── 📂 assets/
│   ├── img-1.png  → img-6.png       ← Dashboard screenshots
│
└── 🔗 Resources Link               ← Additional Databases, full_df.csv (google drive link)



```
</div>


> ⚠️ **Note:** `full_df.csv` is **not committed** to this repo (too large for GitHub). Generate it by running the notebook, or build from the packaged Parquet files.

---

## 🚀 Run Locally

### Step 1 — Clone the Repository

<div align="left">
  
```bash
git clone https://github.com/doyancha/Youtube_Data_Analysis.git
cd Youtube_Data_Analysis
```
</div>

### Step 2 — Install Dependencies

<div align="left">

```bash
pip install -r requirements.txt
```
</div>

### Step 3 — Prepare the Data

<div align="left">

**Option A:** You already have `full_df.csv` also place it in the project root.

**Option B:** Regenerate from the notebook and run all cells in `youtube_data_analysis.ipynb`, then export:

```python
full_df.to_csv("full_df.csv", index=False)
```


**Option C:** Build compressed Parquet files for cloud deployment:

```bash
python build_deployment_data.py
```
</div>

### Step 4 — Launch the Dashboard

<div align="left">

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉
</div>

### ⚡ Requirements

<div align="left">

```txt
streamlit==1.53.1
pandas==2.3.3
numpy==2.4.1
matplotlib==3.10.8
seaborn==0.13.2
plotly==6.5.2
nltk==3.9.2
wordcloud==1.9.6
pyarrow==23.0.0
```
</div>
---

## Dashboard Preview

<div align="left">

The repository includes exported dashboard screenshots in the [`assets`](./assets) folder so visitors can preview the interface before running the app locally.
</div>

<table>
  <tr>
    <td><img src="./assets/img-1.png" alt="Dashboard Preview 1" width="100%"></td>
    <td><img src="./assets/img-2.png" alt="Dashboard Preview 2" width="100%"></td>
    <td><img src="./assets/img-3.png" alt="Dashboard Preview 3" width="100%"></td>
  </tr>
  <tr>
    <td><img src="./assets/img-4.png" alt="Dashboard Preview 4" width="100%"></td>
    <td><img src="./assets/img-5.png" alt="Dashboard Preview 5" width="100%"></td>
    <td><img src="./assets/img-6.png" alt="Dashboard Preview 6" width="100%"></td>
  </tr>
</table>

<div align="center">

> The dashboard uses a **dark neon-glassmorphism** design language built to feel like a modern BI product, not a notebook export.

| Page | Description |
|------|-------------|
| 🏠 **Overview** | Executive KPIs, views/likes scatter, trending channel bar chart, correlation heatmap |
| 📈 **Content Patterns** | Category like rates, reach-to-engagement behavior, punctuation impact |
| 🔍 **Channel & Category Explorer** | Filterable KPI strip, creator comparisons, filtered scatter |
| 💬 **Audience Sentiment** | Sentiment mix donut, score distribution, punctuation vs. reaction |
| ☁️ **Word Clouds** | Positive/negative word clouds, most frequent terms |
| 🏁 **Final Takeaway** | Strategic recommendation cards for creators and analysts |

</div>

---

## 👤 About the Author

<div align="center">

<div align="center">

<div style="display: inline-block; padding: 20px 24px; border-radius: 18px; background: linear-gradient(135deg, #0f172a 0%, #111827 100%); border: 1px solid #334155; box-shadow: 0 10px 28px rgba(0,0,0,0.22);">
  <pre style="margin: 0; color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.65; text-align: left;">
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                 MIR SHAHADUT HOSSAIN                      ║
║            Data Analyst | Streamlit Developer             ║
║                                                           ║
║      Turning raw data into decisions, one dashboard       ║
║                       at a time.                          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  </pre>
</div>

</div>

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mir%20Shahadut%20Hossain-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mir-shahadut-hossain/)
[![GitHub](https://img.shields.io/badge/GitHub-doyancha-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/doyancha)
[![Email](https://img.shields.io/badge/Email-sujon6901%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:sujon6901@gmail.com)
[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://youtube-data-analysis.streamlit.app/)

</div>

---

## 📚 Suggested Resources

### 📖 Documentation & Libraries Used

| Resource | Link |
|----------|------|
| **Streamlit Docs** | [docs.streamlit.io](https://docs.streamlit.io) |
| **Pandas Documentation** | [pandas.pydata.org/docs](https://pandas.pydata.org/docs) |
| **Plotly Express** | [plotly.com/python/plotly-express](https://plotly.com/python/plotly-express) |
| **NLTK VADER Sentiment** | [nltk.org/api/nltk.sentiment.vader](https://www.nltk.org/api/nltk.sentiment.vader.html) |
| **WordCloud Library** | [amueller.github.io/word_cloud](https://amueller.github.io/word_cloud/) |
| **Seaborn Gallery** | [seaborn.pydata.org/examples](https://seaborn.pydata.org/examples/index.html) |
| **emoji (PyPI)** | [pypi.org/project/emoji](https://pypi.org/project/emoji/) |
| **SQLAlchemy** | [docs.sqlalchemy.org](https://docs.sqlalchemy.org/) |

### 📂 Datasets

| Resource | Link |
|----------|------|
| **Kaggle: YouTube Trending Videos** | [kaggle.com/datasets/datasnaek/youtube-new](https://www.kaggle.com/datasets/datasnaek/youtube-new) |
| **Kaggle: YouTube Comments** | [kaggle.com/datasets/datasnaek/youtube](https://www.kaggle.com/datasets/datasnaek/youtube) |

### 🎓 Learning References

| Topic | Link |
|-------|------|
| **Sentiment Analysis with VADER** | [medium.com — VADER guide](https://medium.com/analytics-vidhya/simplifying-social-media-sentiment-analysis-using-vader-in-python-f9e6ec6fc52f) |
| **Python Encoding Guide** | [docs.python.org/encoding](https://docs.python.org/3/library/codecs.html#standard-encodings) |
| **Streamlit App Deployment** | [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud/get-started) |
| **Parquet with Pandas** | [pandas.pydata.org/parquet](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_parquet.html) |
| **Plotly for Dashboards** | [plotly.com/python/getting-started](https://plotly.com/python/getting-started/) |
| **Data Storytelling Principles** | [storytellingwithdata.com](https://www.storytellingwithdata.com/) |

---

<div align="center">

<div align="center">

<div style="display: inline-block; padding: 16px 22px; border-radius: 16px; background: linear-gradient(135deg, #111827 0%, #0f172a 100%); border: 1px solid #334155; box-shadow: 0 8px 24px rgba(0,0,0,0.18);">
  <pre style="margin: 0; color: #e2e8f0; font-family: Consolas, Monaco, monospace; font-size: 14px; line-height: 1.7; text-align: center;">
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Built with ❤️ by Mir Shahadut Hossain | 2025-2026
  Data Analyst · Python Developer · Streamlit Builder
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  </pre>
</div>

</div>
<br>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=120&section=footer" width="100%"/>

</div>
