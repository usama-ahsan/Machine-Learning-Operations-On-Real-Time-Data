# Real-Time Market Movement Prediction System

## ANN + MLOPS Semester Project (Group A)

A real-time financial market prediction system that scrapes live financial news and social media data, performs sentiment analysis, and uses sequential deep learning models (RNN, LSTM, GRU) to predict market direction, price movement trends, and volatility spikes.

---

## Project Structure

```
project1-market-prediction/
├── data/
│   ├── raw/                    # Raw collected data (CSV files)
│   └── processed/              # Cleaned & feature-engineered data
├── src/
│   ├── ingestion/              # Data collection scripts
│   │   ├── yahoo_finance.py    # Yahoo Finance OHLCV data
│   │   ├── reuters_rss.py      # Financial news RSS feeds
│   │   ├── reddit_scraper.py   # Reddit finance communities
│   │   └── twitter_scraper.py  # Twitter/X financial tweets
│   ├── sentiment/              # Sentiment analysis module
│   ├── models/                 # RNN, LSTM, GRU model training
│   └── api/                    # FastAPI REST API
├── dags/                       # Apache Airflow DAGs
├── notebooks/                  # Jupyter notebooks for EDA
├── frontend/                   # Simple web frontend
├── models/                     # Saved trained models
├── mlruns/                     # MLflow experiment tracking
├── .github/workflows/          # CI/CD pipeline (GitHub Actions)
├── main.py                     # Main data collection pipeline
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker containerization
├── .env.example                # API keys template
└── README.md                   # This file
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your credentials
# (See API Setup section below)
```

### 3. Run Data Collection
```bash
python main.py
```

---

## Data Sources

| Source | Library | API Key Required? | Data Type |
|--------|---------|-------------------|-----------|
| Yahoo Finance | yfinance | No | OHLCV market data |
| Reuters/News RSS | feedparser | No | News headlines & summaries |
| Reddit | PRAW | Yes (free) | Posts from finance subreddits |
| Twitter/X | Tweepy | Yes (restricted) | Financial tweets |

---

## API Key Setup

### Reddit API (Free)
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" → Select "script"
3. Set Redirect URI: `http://localhost:8080`
4. Copy `client_id` and `secret` to `.env`

### Twitter/X API (Optional - Restricted)
- Free tier is very limited since 2023
- Go to https://developer.twitter.com
- The project works fine with just Reddit + Reuters

---

## MLOps Pipeline (Group A)

| Tool | Purpose | Phase |
|------|---------|-------|
| DVC | Data version control | Phase 4 |
| MLflow | Experiment tracking | Phase 3 |
| Apache Airflow | Pipeline orchestration | Phase 4 |
| GitHub Actions | CI/CD pipeline | Phase 4 |
| Docker | Containerization | Phase 6 |
| AWS EC2 | Cloud deployment | Phase 6 |

---

## Models

- **RNN** (Recurrent Neural Network)
- **LSTM** (Long Short-Term Memory)
- **GRU** (Gated Recurrent Unit)

All models are trained on sentiment-enriched time-series data and compared using Accuracy, F1-score, and RMSE.

---

## Team

> Add your team members here

---

## License

This project is for academic purposes (ANN + MLOPS Semester Project).
