import json
import os
from datetime import datetime

from config.settings import REWRITTEN_JSON
from core.blogger import (
    publish_post,
    get_recent_titles,
)
from core.facebook import publish_to_facebook


def publish_articles():

    if not os.path.exists(REWRITTEN_JSON):
        raise FileNotFoundError(REWRITTEN_JSON)

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    if not articles:
        print("No rewritten articles.")
        return

    existing_titles = get_recent_titles()

    posts_published = 0
    MAX_POSTS_PER_RUN = 2

    for article in articles:

        if posts_published >= MAX_POSTS_PER_RUN:
            break

        title = article["title"]

        if title.lower() in existing_titles:
            print(f"Skipping duplicate: {title}")
            continue

        tags = [article.get("category", "World")]

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

        content = f"""
<div style="max-width:900px;margin:auto;font-family:Arial,sans-serif;font-size:18px;line-height:1.8;">

<h1>{title}</h1>

<p><strong>Published:</strong> {today}</p>

<hr>

{image_html}

{article["article"]}

<hr>

<h3>About Global Viral Report</h3>

<p>
Global Viral Report delivers trusted breaking news,
technology, business, sports and world news.
</p>

<hr>

<p style="font-size:14px;color:#666;">
Source: AI rewritten from trusted public news sources.
</p>

</div>
"""

        print("Publishing to Blogger:", title)

        result = publish_post(
            title=title,
            content=content,
            tags=tags,
        )

        print("=================================")
        print("Published Successfully")
        print(result["url"])
        print("=================================")

        print("Publishing to Facebook...")

        publish_to_facebook(
            title=title,
            blog_url=result["url"],
        )

        posts_published += 1

    print("Publishing process finished.")


if __name__ == "__main__":
    publish_articles()
