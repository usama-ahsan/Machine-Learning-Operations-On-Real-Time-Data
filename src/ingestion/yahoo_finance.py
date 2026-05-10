import os
import yfinance as yf
import pandas as pd

def collect_yahoo_finance_data(output_path="data/raw/market_data.csv"):
    print("[INFO] Fetching S&P 500 data...")
    try:
        ticker = yf.Ticker("^GSPC")
        df = ticker.history(period="2y", interval="1h").reset_index()
        
        if df.empty:
            return pd.DataFrame()
            
        df = df.rename(columns={
            "Datetime": "timestamp", "Date": "timestamp",
            "Open": "open", "High": "high", "Low": "low", 
            "Close": "close", "Volume": "volume"
        })
        
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["ticker"] = "^GSPC"
        
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S UTC")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if os.path.exists(output_path):
            existing_df = pd.read_csv(output_path)
            df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates(subset=["timestamp", "ticker"], keep="last")
            
        df.to_csv(output_path, index=False)
        print(f"[SAVED] Market data: {len(df)} rows")
        return df
    except Exception as e:
        print(f"[ERROR] Yahoo Finance: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    collect_yahoo_finance_data()
