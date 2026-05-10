import os
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, SMAIndicator, EMAIndicator
from ta.volatility import AverageTrueRange

def build_timeseries(market_path="data/raw/market_data.csv", sentiment_path="data/processed/news_sentiment.csv", output_path="data/processed/timeseries_dataset.csv", window="1h"):
    print("[INFO] Building enhanced time-series dataset with technical indicators...")
    
    if not os.path.exists(market_path) or not os.path.exists(sentiment_path):
        print(f"[ERROR] Required files not found: {market_path} or {sentiment_path}")
        return None
        
    market_df = pd.read_csv(market_path)
    market_df["timestamp"] = pd.to_datetime(market_df["timestamp"].str.replace(" UTC", ""), utc=True, errors="coerce")
    market_df = market_df.dropna(subset=["timestamp"]).set_index("timestamp").sort_index()
    
    # Resample to 15min intervals
    market_15min = market_df.resample(window).agg({
        "open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"
    }).dropna()

    # --- Add Technical Indicators BEFORE merging with sentiment ---
    print("[INFO] Adding Technical Indicators (RSI, MACD, SMA, EMA, ATR)...")
    
    # RSI (14)
    market_15min['rsi'] = RSIIndicator(close=market_15min['close'], window=14).rsi()
    
    # MACD
    macd = MACD(close=market_15min['close'])
    market_15min['macd'] = macd.macd()
    market_15min['macd_signal'] = macd.macd_signal()
    market_15min['macd_diff'] = macd.macd_diff()
    
    # SMA 20 and EMA 12
    market_15min['sma_20'] = SMAIndicator(close=market_15min['close'], window=20).sma_indicator()
    market_15min['ema_12'] = EMAIndicator(close=market_15min['close'], window=12).ema_indicator()
    
    # ATR (14)
    market_15min['atr'] = AverageTrueRange(high=market_15min['high'], low=market_15min['low'], close=market_15min['close'], window=14).average_true_range()
    
    # Volume Change %
    market_15min['vol_change_pct'] = market_15min['volume'].pct_change()
    
    # Price Change %
    market_15min['price_change_pct'] = market_15min['close'].pct_change()

    # --- Sentiment Analysis ---
    sent_df = pd.read_csv(sentiment_path)
    sent_df["published_time"] = pd.to_datetime(sent_df["published_time"], utc=True, errors="coerce")
    sent_df = sent_df.dropna(subset=["published_time"]).set_index("published_time").sort_index()
    
    sent_15min = sent_df.resample(window).agg(
        mean_polarity=("combined_polarity", "mean"),
        article_count=("combined_polarity", "count"),
        sentiment_sum=("sentiment_numeric", "sum")
    )
    
    # Merge datasets
    merged = market_15min.join(sent_15min, how="left").fillna(0)
    
    # Target labeling
    merged["next_close"] = merged["close"].shift(-1)
    merged["direction"] = (merged["next_close"] > merged["close"]).astype(int)
    
    # Drop rows with NaN from indicator calculations (first few rows)
    # and the last row (shift(-1) target is NaN)
    merged = merged.dropna().reset_index().rename(columns={"timestamp": "datetime_utc"})
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"[SAVED] Enhanced dataset: {len(merged)} rows")
    return merged

if __name__ == "__main__":
    build_timeseries()
