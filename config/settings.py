import os

# ==========================
# GEMINI
# ==========================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Stable model
GEMINI_MODEL = "gemini-3.5-flash"

GEMINI_MAX_RETRIES = 5
GEMINI_RETRY_DELAY = 15


# ==========================
# BLOGGER
# ==========================
BLOG_ID = os.getenv("BLOG_ID")
BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")


# ==========================
# CLOUDINARY
# ==========================
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")


# ==========================
# FACEBOOK
# ==========================
FACEBOOK_PAGE_ID = os.getenv(108060764657541)
FACEBOOK_ACCESS_TOKEN = os.getenv("EAAWtQ8rmDZAgBSO8MBZB0M6Vi37mc8NJnILhzGQQ4CewBtoiVbfct4N9jYRovznsLZBgdWZCFEGPOggJcJF8yG78AMyAgZBHlHdOWc2ISoTqDz6ODerLInm6Cb9qmVKv2KQOxtElSW8HYVXwpKuEf47zVRJgDD8ZCY9j62OAkwZApOg5C9ERzZB3V0k2basDsR2H74VnANmDUqNklgRJw38GPzSi9YJmWcXcoyDZCYjwJUPYTmePlehBpxLa08lhMun4pP55QGfhKHpEZD")


# ==========================
# OUTPUT FILES
# ==========================
NEWS_JSON = "output/news/news.json"
REWRITTEN_JSON = "output/news/rewritten.json"


# ==========================
# IMAGES
# ==========================
IMAGE_FOLDER = "output/images"
