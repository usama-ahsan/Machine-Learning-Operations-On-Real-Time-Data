import os
import feedparser
import pandas as pd
from datetime import datetime, timezone
import re

def collect_reuters_rss_data(output_path="data/raw/news_data.csv"):
    print("[INFO] Fetching financial news RSS...")
    
    rss_feeds = {
        "Yahoo Finance S&P500": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^GSPC&region=US&lang=en-US",
        "CNBC Top News": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "MarketWatch Top": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "MarketWatch Markets": "https://feeds.marketwatch.com/marketwatch/markets/",
        "Investing.com News": "https://www.investing.com/rss/news.rss",
        "Google News Finance": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en",
    }
    
    all_articles = []
    for source_name, feed_url in rss_feeds.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                summary = re.sub(r"<[^>]+>", "", entry.get("summary", entry.get("description", ""))).strip()[:500]
                
                article = {
                    "title": entry.get("title", "").strip(),
                    "summary": summary,
                    "source": source_name,
                    "published_time": entry.get("published", entry.get("updated", entry.get("pubDate", ""))),
                }
                
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    from time import mktime
                    dt = datetime.fromtimestamp(mktime(entry.published_parsed), tz=timezone.utc)
                    article["published_time"] = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                    
                all_articles.append(article)
        except Exception as e:
            print(f"[ERROR] {source_name}: {e}")
            
    if all_articles:
        df = pd.DataFrame(all_articles)
        # Deduplicate current batch
        df = df.drop_duplicates(subset=["title"])
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if os.path.exists(output_path):
            existing_df = pd.read_csv(output_path)
            df = pd.concat([existing_df, df], ignore_index=True)
            # Deduplicate against history
            df = df.drop_duplicates(subset=["title"], keep="last")
            
        df.to_csv(output_path, index=False)
        print(f"[SAVED] News data: {len(df)} articles")
        return df
    return pd.DataFrame()

if __name__ == "__main__":
    collect_reuters_rss_data()
