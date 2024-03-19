# a_run_ixbt.py

import asyncio

from scraper import get_articles_urls
from processor import get_data_ixbt
from publisher import publish_articles
from config import URL_IXBT, KEYWORDS


def main():
    print("Starting article collection...")
    get_articles_urls (URL_IXBT)

    print("Processing articles...")
    get_data_ixbt('articles_url_list.txt', KEYWORDS)

    print("Publishing articles...")
    asyncio.run(publish_articles())


if __name__ == "__main__":
    main()
