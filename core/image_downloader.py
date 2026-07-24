import json
import os

from config.settings import (
    REWRITTEN_JSON,
)


def download_images():
    """
    Instead of downloading copyrighted images from the internet,
    generate an original AI image prompt for each article.
    """

    if not os.path.exists(REWRITTEN_JSON):
        print("No rewritten articles found.")
        return

    with open(REWRITTEN_JSON, "r", encoding="utf-8") as f:
        articles = json.load(f)

    for i, article in enumerate(articles, start=1):

        title = article.get("title", "")
        keywords = article.get("image_keywords", "")
        category = article.get("category", "News")

        prompt = f"""
Ultra realistic editorial news photograph.

Topic:
{title}

Keywords:
{keywords}

Category:
{category}

Style:
Professional photojournalism,
cinematic lighting,
high detail,
8k,
natural colors,
realistic people,
realistic environment,
news agency quality,
no text,
no watermark,
no logo,
16:9 composition.
""".strip()

        article["image_prompt"] = prompt

        print(f"✓ Generated AI image prompt for article {i}")

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print("\nFinished generating AI image prompts.")


if __name__ == "__main__":
    download_images()
