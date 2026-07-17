import feedparser
import json
import os
from datetime import datetime

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.skynews.com/feeds/rss/world.xml"
]


def collect_news():
    news = []
    seen = set()

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                link = entry.get("link", "")

                if link in seen:
                    continue

                seen.add(link)

                news.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": link,
                    "published": entry.get("published", ""),
                    "source": feed.feed.get("title", "")
                })

        except Exception as e:
            print(f"Error reading {url}: {e}")

    os.makedirs("output/news", exist_ok=True)

    with open("output/news/news.json", "w", encoding="utf-8") as f:
        json.dump({
            "generated": datetime.utcnow().isoformat(),
            "count": len(news),
            "articles": news
        }, f, indent=4, ensure_ascii=False)

    print(f"Collected {len(news)} articles.")


if __name__ == "__main__":
    collect_news()
