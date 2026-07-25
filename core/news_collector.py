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


def calculate_score(title, summary):

    text = f"{title} {summary}".lower()

    score = 0

    keywords = {
        "breaking": 25,
        "urgent": 20,
        "war": 20,
        "attack": 18,
        "explosion": 18,
        "earthquake": 25,
        "flood": 18,
        "wildfire": 18,
        "death": 18,
        "dies": 18,
        "president": 15,
        "trump": 20,
        "putin": 20,
        "xi": 20,
        "zelensky": 20,
        "israel": 18,
        "gaza": 18,
        "hamas": 18,
        "iran": 18,
        "china": 15,
        "usa": 15,
        "ukraine": 18,
        "elon": 20,
        "musk": 20,
        "tesla": 15,
        "apple": 15,
        "google": 15,
        "openai": 20,
        "ai": 15,
        "chatgpt": 20,
        "bitcoin": 18,
        "crypto": 18,
        "stock": 12,
        "market": 12,
        "football": 12,
        "fifa": 15,
        "world cup": 20,
        "klopp": 15,
    }

    for word, value in keywords.items():
        if word in text:
            score += value

    score += min(len(summary) // 20, 20)

    return score


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

                score = calculate_score(title, summary)

                news.append({
                    "id": len(news) + 1,
                    "score": score,
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
        key=lambda x: x["score"],
        reverse=True
    )

    for i, article in enumerate(news, start=1):
        article["id"] = i

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

    print("\nTop 5 Stories:")

    for article in news[:5]:
        print(f"[{article['score']}] {article['title']}")


if __name__ == "__main__":
    collect_news()
