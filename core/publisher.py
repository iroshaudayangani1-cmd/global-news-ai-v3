import json
import os

from config.settings import REWRITTEN_JSON
from core.blogger import publisimport json
import os
from datetime import datetime

from config.settings import REWRITTEN_JSON
from core.blogger import publish_post


def publish_articles():

    if not os.path.exists(REWRITTEN_JSON):
        raise FileNotFoundError(REWRITTEN_JSON)

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("No rewritten articles.")
        return

    article = articles[0]

    title = article["title"]

    today = datetime.utcnow().strftime("%B %d, %Y")

    content = f"""
<div class="news-article">

<p><strong>Published:</strong> {today}</p>

<h2>{title}</h2>

<hr>

<p>{article["article"]}</p>

<hr>

<h3>Stay Updated</h3>

<p>
Global Viral Report brings you the latest breaking news,
technology, politics, business and world events every day.
</p>

<hr>

<p><strong>Source:</strong> AI rewritten from trusted public news sources.</p>

</div>
"""

    print("Publishing:", title)

    result = publish_post(title, content)

    print(result["url"])h_post


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
