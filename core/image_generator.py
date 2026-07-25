import json
import os
import requests
import urllib.parse

from config.settings import REWRITTEN_JSON, IMAGE_FOLDER


def generate_images():

    if not os.path.exists(REWRITTEN_JSON):
        print("No rewritten articles found.")
        return

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    os.makedirs(IMAGE_FOLDER, exist_ok=True)

    for i, article in enumerate(articles, start=1):

        prompt = article.get("image_prompt", "")

        if not prompt:
            print(f"Article {i}: No image prompt.")
            continue

        print(f"Generating image for article {i}...")

        encoded = urllib.parse.quote(prompt)

        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded}"
            "?width=1280&height=720&model=flux"
        )

        filename = os.path.join(
            IMAGE_FOLDER,
            f"article_{i}.jpg"
        )

        try:

            response = requests.get(
                image_url,
                timeout=120,
            )

            if response.status_code == 200:

                with open(filename, "wb") as img:
                    img.write(response.content)

                article["image"] = filename

                print(f"✓ Image saved: {filename}")

            else:

                print("Image generation failed.")

        except Exception as e:

            print(e)

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nFinished generating AI images.")


if __name__ == "__main__":
    generate_images()
