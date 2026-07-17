import json
import os

from google import genai

from config.settings import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    NEWS_JSON,
    REWRITTEN_JSON,
)


def rewrite_articles():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found.")

    client = genai.Client(api_key=GEMINI_API_KEY)

    with open(NEWS_JSON, "r", encoding="utf-8") as f:
        news = json.load(f)

    rewritten = []

    for article in news["articles"][:5]:
        prompt = f"""
You are a professional news editor.

Rewrite this news article into a unique, SEO-friendly blog post.

Return ONLY valid JSON in this format:

{{
"title":"",
"meta_description":"",
"tags":["","",""],
"article":""
}}

Title:
{article["title"]}

Summary:
{article["summary"]}

Source:
{article["source"]}
"""

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            text = response.text.strip()

            # Remove Markdown code fences if Gemini adds them
            text = text.replace("```json", "").replace("```", "").strip()

            rewritten.append(json.loads(text))

        except Exception as e:
            print(f"Error rewriting article: {e}")

    os.makedirs("output/news", exist_ok=True)

    with open(REWRITTEN_JSON, "w", encoding="utf-8") as f:
        json.dump(rewritten, f, indent=4, ensure_ascii=False)

    print(f"Rewrote {len(rewritten)} articles.")
