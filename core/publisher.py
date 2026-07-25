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

        if article.get("image_url"):
            image_html = f"""
<div style="text-align:center;margin:25px 0;">
<img src="{article['image_url']}"
     alt="{title}"
     style="width:100%;max-width:900px;height:auto;border-radius:12px;">
</div>
"""

        labels = ""

        if tags:
            labels = f"""
<p style="color:#666;font-size:14px;">
<strong>Category:</strong> {" | ".join(tags)}
</p>
"""

        content = f"""
<div style="max-width:900px;margin:auto;font-family:Arial,sans-serif;font-size:18px;line-height:1.8;color:#222;">

<h1>{title}</h1>

<p style="color:#777;">
<strong>Published:</strong> {today}
</p>

{labels}

{image_html}

<hr>

{article["article"]}

<hr>

<h3>About Global Viral Report</h3>

<p>
Global Viral Report delivers trusted breaking news, world affairs,
technology, business, sports and science updates from reliable public
sources around the world.
</p>

<hr>

<p style="font-size:14px;color:#777;">
Source: AI rewritten from trusted public news sources.
</p>

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
