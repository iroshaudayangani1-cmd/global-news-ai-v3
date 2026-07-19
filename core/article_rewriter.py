prompt = f"""
You are an experienced journalist writing for Global Viral Report.

Rewrite the following news into a completely original, SEO-friendly article.

IMPORTANT RULES:

- Return ONLY valid JSON.
- Do NOT use Markdown.
- Write 600-900 words.
- Write in fluent, natural English.
- Make the article engaging and factual.
- Never copy the source text.

The article field MUST contain HTML.

Use this structure:

<h2>Introduction</h2>

<p>...</p>

<h2>What Happened?</h2>

<p>...</p>

<h2>Key Developments</h2>

<p>...</p>

<ul>
<li>...</li>
<li>...</li>
</ul>

<h2>International Response</h2>

<p>...</p>

<h2>What Happens Next?</h2>

<p>...</p>

Return ONLY this JSON:

{{
  "title": "",
  "meta_description": "",
  "tags": ["", "", ""],
  "article": ""
}}

News Title:
{article.get("title","")}

Summary:
{article.get("summary","")}

Source:
{article.get("source","")}
"""
