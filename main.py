from core.news_collector import collect_news
from core.article_rewriter import rewrite_articles
from core.image_downloader import download_images
from core.publisher import publish_articles


def main():

    print("===== GLOBAL NEWS AI =====")

    print("\nStep 1 : Collecting News")
    collect_news()

    print("\nStep 2 : Rewriting Articles")
    rewrite_articles()

    print("\nStep 3 : Downloading Images")
    download_images()

    print("\nStep 4 : Publishing to Blogger")
    publish_articles()

    print("\nAll Tasks Completed Successfully")


if __name__ == "__main__":
    main()
