import json
import os
import time

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_MAX_RETRIES,
    GEMINI_RETRY_DELAY,
    NEWS_JSON,
    REWRITTEN_JSON,
)


def clean_json(text):
    """Remove markdown code blocks if Gemini returns them."""
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def rewrite_articles():

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found.")

    if not os.path.exists(NEWS_JSON):
        raise FileNotFoundError(f"{NEWS_JSON} not found.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    with open(NEWS_JSON, "r", encoding="utf-8") as f:
        news = json.load(f)

    articles = news.get("articles", [])

    print(f"Found {len(articles)} articles.")

    rewritten = []

    # Change back to [:5] after testing
    for i, article in enumerate(articles[:1], start=1):

        print(f"\nRewriting article {i}...")

        prompt = f"""
You are an experienced journalist writing for Global Viral Report.

Rewrite the following news into a completely original, SEO-friendly article.

IMPORTANT RULES

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Write between 700 and 1000 words.
- Write in fluent professional English.
- Never copy the original wording.
- Make the article engaging, factual and easy to read.
- The "article" field MUST contain HTML.

The HTML article MUST use this structure:

<h2>Introduction</h2>
<p>...</p>

<h2>What Happened?</h2>
<p>...</p>

<h2>Key Developments</h2>
<p>...</p>

<ul>
<li>...</li>
<li>...</li>
<li>...</li>
</ul>

<h2>International Response</h2>
<p>...</p>

<h2>What Happens Next?</h2>
<p>...</p>

Return ONLY this JSON:

{{
    "title":"",
    "slug":"",
    "category":"",
    "meta_description":"",
    "tags":[],
    "image_keywords":"",
    "article":""
}}

Rules:

"title"
- SEO friendly.
- Maximum 70 characters.

"slug"
- Lowercase only.
- Hyphens only.
- No spaces.

"category"
Choose ONLY ONE:

World
Politics
Business
Technology
Sports
Health
Science
Entertainment

"tags"

Choose between 1 and 3 labels from:

World
Politics
Business
Technology
Sports
Health
Science
Entertainment

"image_keywords"

Write one short search phrase that would find a high-quality news image.

"meta_description"

Maximum 160 characters.

News Title:
{article.get("title", "")}

Summary:
{article.get("summary", "")}

Source:
{article.get("source", "")}
"""

        success = False

        for attempt in range(1, GEMINI_MAX_RETRIES + 1):

            try:

                print(f"Attempt {attempt}/{GEMINI_MAX_RETRIES}")

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                )

                text = clean_json(response.text)

                rewritten.append(json.loads(text))

                print("✓ Success")

                success = True
                break

            except Exception as e:

                print(f"Attempt {attempt} failed: {e}")

                if "503" in str(e) and attempt < GEMINI_MAX_RETRIES:
                    wait_time = GEMINI_RETRY_DELAY * attempt
                    print(f"Gemini busy. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue

                break

        if not success:
            print("Skipping article.")

    os.makedirs("output/news", exist_ok=True)

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(
            rewritten,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(f"\nFinished! Rewrote {len(rewritten)} articles.")


if __name__ == "__main__":
    rewrite_articles()
