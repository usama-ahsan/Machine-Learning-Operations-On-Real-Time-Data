import os
import pandas as pd
from textblob import TextBlob

def get_sentiment(text):
    if not text or not isinstance(text, str): return 0.0
    try: return round(TextBlob(text).sentiment.polarity, 4)
    except: return 0.0

def get_label(polarity):
    if polarity > 0.05: return "Positive"
    if polarity < -0.05: return "Negative"
    return "Neutral"

def label_sentiment(input_path="data/raw/news_data.csv", output_path="data/processed/news_sentiment.csv"):
    print("[INFO] Labeling sentiment...")
    if not os.path.exists(input_path): return None
    
    df = pd.read_csv(input_path)
    if df.empty: return None

    df["title_polarity"] = df["title"].apply(get_sentiment)
    df["summary_polarity"] = df["summary"].apply(get_sentiment)
    
    df["combined_polarity"] = (df["title_polarity"] * 0.6 + df["summary_polarity"] * 0.4).round(4)
    df["combined_sentiment"] = df["combined_polarity"].apply(get_label)
    df["sentiment_numeric"] = df["combined_sentiment"].map({"Positive": 1, "Neutral": 0, "Negative": -1})
    
    df["published_time"] = pd.to_datetime(df["published_time"], utc=True, errors="coerce")
    df = df.dropna(subset=["published_time"])
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SAVED] Sentiment data: {len(df)} rows")
    return df

if __name__ == "__main__":
    label_sentiment()
