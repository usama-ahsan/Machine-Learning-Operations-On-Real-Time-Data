import os
from src.ingestion.yahoo_finance import collect_yahoo_finance_data
from src.ingestion.reuters_rss import collect_reuters_rss_data
from src.sentiment.label_sentiment import label_sentiment
from src.preprocessing.build_timeseries import build_timeseries

def main():
    print("Starting pipeline...")
    
    data_dir = "data/raw"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    print("\nPhase 1: Ingestion")
    collect_yahoo_finance_data(f"{data_dir}/market_data.csv")
    collect_reuters_rss_data(f"{data_dir}/news_data.csv")
    
    print("\nPhase 2: Processing")
    label_sentiment(f"{data_dir}/news_data.csv", "data/processed/news_sentiment.csv")
    build_timeseries(f"{data_dir}/market_data.csv", "data/processed/news_sentiment.csv", "data/processed/timeseries_dataset.csv")
    
    print("\nPipeline complete.")

if __name__ == "__main__":
    main()
