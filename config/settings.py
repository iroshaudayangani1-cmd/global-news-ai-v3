import os

# ==========================
# GEMINI
# ==========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# ==========================
# BLOGGER
# ==========================
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")

# ==========================
# FACEBOOK
# ==========================
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

# ==========================
# OUTPUT FILES
# ==========================
NEWS_JSON = "output/news/news.json"
REWRITTEN_JSON = "output/news/rewritten.json"
