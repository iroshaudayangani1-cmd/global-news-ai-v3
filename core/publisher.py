import json
import os

from config.settings import REWRITTEN_JSON
from core.blogger import (
    publish_post,
    get_recent_titles,
)

from datetime import datetime


def publish_articles():

    if not os.path.exists(REWRITTEN_JSON):
        raise FileNotFoundError(REWRITTEN_JSON)

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("No rewritten articles.")
        return

    existing_titles = get_recent_titles()

    for article in articles:

        title = article["title"]

        if title.lower() in existing_titles:
            print(f"Skipping duplicate: {title}")
            continue

        today = datetime.utcnow().strftime("%B %d, %Y")

        content = f"""
<div class="news-article">

<p><strong>Published:</strong> {today}</p>

<h2>{title}</h2>

<hr>

{article["article"]}

<hr>

<h3>Stay Updated</h3>

<p>
Global Viral Report brings you breaking news,
technology, business and world events every day.
</p>

<hr>

<p><strong>Source:</strong> AI rewritten from trusted public news sources.</p>

</div>
"""

        result = publish_post(title, content)

        print("=================================")
        print("Published Successfully")
        print(result["url"])
        print("=================================")

        return

    print("No new articles to publish today.")
