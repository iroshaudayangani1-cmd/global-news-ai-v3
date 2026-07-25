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
        raise FileNotFoundError(NEWS_JSON)

    client = genai.Client(api_key=GEMINI_API_KEY)

    with open(NEWS_JSON, "r", encoding="utf-8") as f:
        news = json.load(f)

    articles = news.get("articles", [])

    print(f"Found {len(articles)} articles.")

    rewritten = []

    # Free Gemini = rewrite only ONE article
    for i, article in enumerate(articles[:1], start=1):

        print(f"\nRewriting article {i}...")

        prompt = f"""
You are a senior Reuters and BBC journalist writing for Global Viral Report.

Rewrite the following news article professionally.

IMPORTANT

Return ONLY valid JSON.
No markdown.
No explanations.
No extra text.

GENERAL RULES

- Write between 450 and 650 words.
- Use professional journalism.
- Never invent facts.
- Never speculate.
- Never copy the original wording.
- Keep paragraphs short.
- Use HTML only inside the article field.

ARTICLE STRUCTURE

<h2>Introduction</h2>
<p>...</p>

<h2>What Happened?</h2>
<p>...</p>

<h2>Key Facts</h2>

<ul>
<li>...</li>
<li>...</li>
<li>...</li>
<li>...</li>
</ul>

<h2>Why It Matters</h2>
<p>...</p>

<h2>What Happens Next?</h2>
<p>...</p>

Return EXACTLY this JSON:

{{
"title":"",
"slug":"",
"category":"",
"meta_description":"",
"tags":[],
"image_prompt":"",
"article":""
}}

TITLE

- Maximum 65 characters
- SEO friendly
- Natural
- No clickbait

SLUG

- lowercase
- hyphen-separated

CATEGORY

Choose ONE only:

World
Politics
Business
Technology
Sports
Health
Science
Entertainment

TAGS

Choose 2 or 3 tags.

META DESCRIPTION

Maximum 155 characters.

IMAGE PROMPT

Generate a detailed AI image prompt for a realistic editorial news photograph.

Requirements:

- ultra realistic
- photojournalism
- cinematic lighting
- highly detailed
- realistic people
- 16:9 composition
- suitable for a news website
- no text
- no logo
- no watermark

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

                    wait = GEMINI_RETRY_DELAY * attempt

                    print(f"Gemini busy. Waiting {wait} seconds...")

                    time.sleep(wait)

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
