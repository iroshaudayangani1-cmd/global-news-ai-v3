from core.news_collector import collect_news
from core.article_rewriter import rewrite_articles


def main():
    print("===== GLOBAL NEWS AI =====")

    print("\nStep 1: Collecting news...")
    collect_news()

    print("\nStep 2: Rewriting articles with Gemini...")
    rewrite_articles()

    print("\nAll tasks completed successfully.")


if __name__ == "__main__":
    main()
