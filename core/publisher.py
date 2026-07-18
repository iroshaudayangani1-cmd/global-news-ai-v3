import json
import os

from config.settings import REWRITTEN_JSON
from core.blogger import publish_post


def publish_articles():

    if not os.path.exists(REWRITTEN_JSON):
        raise FileNotFoundError(
            f"{REWRITTEN_JSON} not found."
        )

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("No rewritten articles found.")
        return

    article = articles[0]

    title = article["title"]
    content = f"""
<h2>{article['title']}</h2>

<p>{article['article']}</p>
"""

    print(f"Publishing: {title}")

    result = publish_post(title, content)

    print("=================================")
    print("Published Successfully")
    print(result["url"])
    print("=================================")
