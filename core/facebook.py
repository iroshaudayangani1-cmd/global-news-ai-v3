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


def publish_to_facebook(title, article, image_url, blog_url):

    url = f"https://graph.facebook.com/v25.0/{FACEBOOK_PAGE_ID}/photos"

    # Remove HTML tags for Facebook
    import re

    clean_article = re.sub("<.*?>", "", article)
    clean_article = clean_article.replace("&nbsp;", " ")

    if len(clean_article) > 1800:
        clean_article = clean_article[:1800] + "..."

    message = f"""{title}

{clean_article}

Read more:
{blog_url}
"""

    payload = {
        "url": image_url,
        "caption": message,
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
    }

    response = requests.post(
        url,
        data=payload,
        timeout=120,
    )

    print("=" * 60)
    print("FACEBOOK DEBUG")
    print("=" * 60)
    print("Status:", response.status_code)
    print(response.text)
    print("=" * 60)

    response.raise_for_status()

    print("✓ Successfully posted to Facebook")
