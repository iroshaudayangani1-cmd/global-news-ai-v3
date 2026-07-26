import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from config.settings import (
    BLOGGER_CLIENT_ID,
    BLOGGER_CLIENT_SECRET,
    BLOGGER_REFRESH_TOKEN,
    BLOG_ID,
)

TOKEN_URL = "https://oauth2.googleapis.com/token"


def get_access_token():

    print("=" * 60)
    print("BLOGGER DEBUG")
    print("=" * 60)
    print("BLOG_ID:", BLOG_ID)
    print("CLIENT_ID:", BLOGGER_CLIENT_ID[:20] + "..." if BLOGGER_CLIENT_ID else "Missing")
    print("CLIENT_SECRET exists:", bool(BLOGGER_CLIENT_SECRET))
    print("REFRESH_TOKEN exists:", bool(BLOGGER_REFRESH_TOKEN))
    print("Refresh token length:", len(BLOGGER_REFRESH_TOKEN) if BLOGGER_REFRESH_TOKEN else 0)
    print("=" * 60)

    creds = Credentials(
        None,
        refresh_token=BLOGGER_REFRESH_TOKEN,
        token_uri=TOKEN_URL,
        client_id=BLOGGER_CLIENT_ID,
        client_secret=BLOGGER_CLIENT_SECRET,
    )

    creds.refresh(Request())

    return creds.token


def get_recent_titles():

    access_token = get_access_token()

    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/"
        f"{BLOG_ID}/posts?maxResults=20"
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        titles = set()

        for post in data.get("items", []):
            titles.add(post["title"].lower())

        return titles

    except Exception as e:

        print("Unable to read existing Blogger posts.")
        print(e)

        return set()


def publish_post(title, content, tags):

    access_token = get_access_token()

    url = (
        f"https://www.googleapis.com/blogger/v3/blogs/"
        f"{BLOG_ID}/posts/"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": tags,
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60,
        )

        print("Status Code:", response.status_code)

        response.raise_for_status()

        print("✓ Blogger accepted the post.")

        return response.json()

    except requests.HTTPError:

        print("Blogger returned an error:")
        print(response.text)
        raise

    except Exception as e:

        print("Publishing failed.")
        print(e)
        raise
