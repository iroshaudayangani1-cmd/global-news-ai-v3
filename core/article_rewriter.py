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

    # Free plan = rewrite only one article
    for i, article in enumerate(articles[:1], start=1):

        print(f"\nRewriting article {i}...")

        prompt = f"""
You are a senior Reuters/BBC style journalist writing for Global Viral Report.

Your job is to rewrite the news professionally.

IMPORTANT

Return ONLY valid JSON.
No Markdown.
No explanations.
No extra text.

GENERAL RULES

- Write 450-650 words.
- Professional journalism.
- Easy to read.
- Short paragraphs.
- Never invent facts.
- Never speculate.
- Never add fake expert opinions.
- Use ONLY the supplied information.
- Rewrite completely in your own words.

ARTICLE STRUCTURE

<h2>Introduction</h2>
<p>60-90 words</p>

<h2>What Happened?</h2>
<p>80-120 words</p>

<h2>Key Facts</h2>

<ul>
<li>Fact 1</li>
<li>Fact 2</li>
<li>Fact 3</li>
<li>Fact 4</li>
</ul>

<h2>Why It Matters</h2>
<p>80-120 words</p>

<h2>What Happens Next?</h2>
<p>60-100 words</p>

Return EXACTLY this JSON:

{{
"title":"",
"slug":"",
"category":"",
"meta_description":"",
"tags":[],
"image_keywords":"",
"article":""
}}

TITLE

- SEO friendly
- Maximum 65 characters
- Clickable
- Natural
- No clickbait
- No ALL CAPS

SLUG

lowercase-only
hyphen-separated

CATEGORY

Choose ONE

World
Politics
Business
Technology
Sports
Health
Science
Entertainment

TAGS

Choose 2 or 3.

META DESCRIPTION

Maximum 155 characters.

IMAGE KEYWORDS

Instead of a simple keyword, generate an AI image prompt.

Example:

Ultra realistic editorial news photograph of world leaders meeting during a peace summit, dramatic lighting, highly detailed, professional journalism style, 16:9 composition, no text, no watermark.

The prompt must match THIS article.

News Title:

{article.get("title","")}

Summary:

{article.get("summary","")}

Source:

{article.get("source","")}
"""

        success = False

        for attempt in range(1, GEMINI_MAX_RETRIES + 1):

            try:

                print(f"Attempt {attempt}/{GEMINI_MAX_RETRIES}")
                print("=" * 60)
                print("MODEL SENT TO API:", repr(GEMINI_MODEL))
                print("=" * 60)

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
