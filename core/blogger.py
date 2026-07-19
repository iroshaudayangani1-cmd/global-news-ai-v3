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
    print("CLIENT ID:", BLOGGER_CLIENT_ID[:40])
    print("CLIENT SECRET:", BLOGGER_CLIENT_SECRET[:10])
    print("REFRESH TOKEN:", BLOGGER_REFRESH_TOKEN[:20])

    creds = Credentials(
        None,
        refresh_token=BLOGGER_REFRESH_TOKEN,
        token_uri=TOKEN_URL,
        client_id=BLOGGER_CLIENT_ID,
        client_secret=BLOGGER_CLIENT_SECRET,
    )

    creds.refresh(Request())

    return creds.token


def publish_post(title, content):
    access_token = get_access_token()

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
    }

    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    return response.json()
