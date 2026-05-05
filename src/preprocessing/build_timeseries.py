import os
import pandas as pd

def build_timeseries(market_path="data/raw/market_data.csv", sentiment_path="data/processed/news_sentiment.csv", output_path="data/processed/timeseries_dataset.csv", window="15min"):
    print("[INFO] Building time-series dataset...")
    
    if not os.path.exists(market_path) or not os.path.exists(sentiment_path):
        return None
        
    market_df = pd.read_csv(market_path)
    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"].str.replace(" UTC", ""), utc=True, errors="coerce")
    market_df = market_df.dropna(subset=["timestamp"]).set_index("timestamp").sort_index()
    
    market_15min = market_df.resample(window).agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"
    }).dropna()

    sent_df = pd.read_csv(sentiment_path)
    sent_df["published_time"] = pd.to_datetime(sent_df["published_time"], utc=True, errors="coerce")
    sent_df = sent_df.dropna(subset=["published_time"]).set_index("published_time").sort_index()
    
    sent_15min = sent_df.resample(window).agg(
        mean_polarity=("combined_polarity", "mean"),
        article_count=("combined_polarity", "count"),
        sentiment_sum=("sentiment_numeric", "sum")
    )
    
    merged = market_15min.join(sent_15min, how="left").fillna(0)
    
    merged["price_return"] = merged["close"].pct_change().round(6)
    merged["next_close"] = merged["close"].shift(-1)
    merged["direction"] = (merged["next_close"] > merged["close"]).astype(int)
    
    merged = merged.dropna().reset_index().rename(columns={"timestamp": "datetime_utc"})
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"[SAVED] Time-series dataset: {len(merged)} rows")
    return merged

if __name__ == "__main__":
    build_timeseries()
