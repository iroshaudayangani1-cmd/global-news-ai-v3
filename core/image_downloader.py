import json
import os
import requests

from config.settings import (
    REWRITTEN_JSON,
    IMAGE_FOLDER,
)


def download_images():

    if not os.path.exists(REWRITTEN_JSON):
        print("No rewritten articles found.")
        return

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, article in enumerate(articles, start=1):

        keyword = article.get("image_keywords", "")

        if not keyword:
            print(f"Article {i}: No image keyword.")
            continue

        image_url = (
            "https://source.unsplash.com/1200x675/?"
            + keyword.replace(" ", ",")
        )

        filename = os.path.join(
            IMAGE_FOLDER,
            f"article_{i}.jpg"
        )

        try:

            response = requests.get(
                image_url,
                headers=headers,
                timeout=30,
                allow_redirects=True,
            )

            if response.status_code == 200:

                with open(filename, "wb") as img:
                    img.write(response.content)

                article["image"] = filename

                print(f"✓ Downloaded image for article {i}")

            else:

                print(f"Failed image {i}")

        except Exception as e:

            print(e)

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("Finished downloading images.")


if __name__ == "__main__":
    download_images()
