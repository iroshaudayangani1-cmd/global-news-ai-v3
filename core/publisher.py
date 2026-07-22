import json
import os
from datetime import datetime

from config.settings import REWRITTEN_JSON
from core.blogger import (
    publish_post,
    get_recent_titles,
)


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

        tags = article.get("tags", [])

        today = datetime.utcnow().strftime("%B %d, %Y")

        image_html = ""

        # If image_downloader.py added an image_url,
        # insert it at the top of the article.
        if article.get("image_url"):
            image_html = f"""
<p style="text-align:center;">
<img src="{article['image_url']}"
     alt="{title}"
     style="max-width:100%;height:auto;border-radius:8px;">
</p>
"""

        content = f"""
<div class="news-article">

{image_html}

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

        print("Publishing:", title)

        result = publish_post(
            title=title,
            content=content,
            tags=tags,
        )

        print("=================================")
        print("Published Successfully")
        print(result["url"])
        print("=================================")

        return

    print("No new articles to publish today.")
