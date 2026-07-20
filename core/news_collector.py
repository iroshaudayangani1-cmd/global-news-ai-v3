import feedparser
import json
import os
from datetime import datetime

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.cnn.com/rss/edition.rss",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://feeds.skynews.com/feeds/rss/world.xml",
]


def collect_news():
    news = []
    seen = set()

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(
                url,
                request_headers={
                    "User-Agent": "GlobalViralReportBot/1.0"
                }
            )

            for entry in feed.entries[:10]:

                link = entry.get("link", "")

                if link in seen:
                    continue

                seen.add(link)

                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()

                if not title or not summary:
                    continue

                news.append({
                    "id": len(news) + 1,
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published": entry.get("published", ""),
                    "source": feed.feed.get("title", "")
                })

        except Exception as e:
            print(f"❌ Failed: {url}")
            print(e)

    news.sort(
        key=lambda x: x.get("published", ""),
        reverse=True
    )

    os.makedirs("output/news", exist_ok=True)

    with open("output/news/news.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "generated": datetime.utcnow().isoformat(),
                "count": len(news),
                "articles": news,
            },
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(f"Collected {len(news)} articles.")


if __name__ == "__main__":
    collect_news()
