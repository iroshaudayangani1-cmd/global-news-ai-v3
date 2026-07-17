import os

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Blogger
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_ACCESS_TOKEN = os.getenv("BLOGGER_ACCESS_TOKEN")

# Facebook
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# Output
NEWS_JSON = "output/news/news.json"
REWRITTEN_JSON = "output/news/rewritten.json"

# Gemini Model
GEMINI_MODEL = "gemini-2.5-flash"
