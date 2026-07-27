import requests

from config.settings import (
    FACEBOOK_PAGE_ID,
    FACEBOOK_PAGE_ACCESS_TOKEN,
)


def publish_to_facebook(title, blog_url):

    url = f"https://graph.facebook.com/v25.0/{FACEBOOK_PAGE_ID}/feed"

    message = f"""{title}

Read the full story here:
{blog_url}

#BreakingNews #WorldNews #TheGlobalBrief
"""

    payload = {
        "message": message,
        "access_token": FACEBOOK_PAGE_ACCESS_TOKEN,
    }

    response = requests.post(
        url,
        data=payload,
        timeout=60,
    )

    print("Facebook Status:", response.status_code)

    if response.status_code == 200:

        print("✓ Posted to Facebook")

    else:

        print("Facebook Error")
        print(response.text)
