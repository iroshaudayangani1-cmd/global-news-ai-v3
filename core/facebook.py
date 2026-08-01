import requests
import requests

from config.settings import (
    FACEBOOK_PAGE_ID,
    FACEBOOK_PAGE_ACCESS_TOKEN,
)

print("=" * 60)
print("FACEBOOK SETTINGS")
print("=" * 60)
print("PAGE ID:", repr(FACEBOOK_PAGE_ID))
print("TOKEN EXISTS:", bool(FACEBOOK_PAGE_ACCESS_TOKEN))
print("=" * 60)
from config.settings import (
    FACEBOOK_PAGE_ID,
    FACEBOOK_PAGE_ACCESS_TOKEN,
)


def publish_to_facebook(title, article_html, image_url, blog_url):

    # Remove HTML tags
    import re

    article = re.sub("<.*?>", "", article_html)
    article = article.replace("\n", " ").strip()

    # Facebook only needs the first part
    article = article[:1800]

    message = f"""{title}

{article}

Read more:
{blog_url}
"""

    url = f"https://graph.facebook.com/v25.0/{FACEBOOK_PAGE_ID}/photos"

    payload = {
        "url": image_url,
        "caption": message,
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
    }

    try:

        response = requests.post(
            url,
            data=payload,
            timeout=60,
        )

        print("=" * 60)
        print("FACEBOOK DEBUG")
        print("=" * 60)
        print("Status:", response.status_code)
        print(response.text)
        print("=" * 60)

        response.raise_for_status()

        print("✓ Successfully posted to Facebook")

    except Exception as e:

        print("❌ Facebook publishing failed")
        print(e)
