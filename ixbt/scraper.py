import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ixbt.config import HEADERS
from ixbt.get_article import get_article
from ixbt.get_publisher_tlg import send_messages

today_date = datetime.now().strftime("%Y/%m/%d")
URL_IXBT = f"https://www.ixbt.com/news/{today_date}/"

def get_articles_urls() -> list:
    print(f"Sending request to {URL_IXBT}...")
    with requests.Session() as s:
        response = s.get(url=URL_IXBT, headers=HEADERS)

    print("Response received, parsing...")
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a", href=lambda href: href and "/news/" + today_date in href)

    articles_urls_list = []
    for link in links:
        url = link.get("href")
        # Добавляем условие, чтобы пропускать ссылки, не содержащие конкретной новости
        if url.startswith(f"/news/{today_date}") and url not in articles_urls_list and not url.endswith(
                "#comments"):
            full_url = f"https://www.ixbt.com{url}"
            articles_urls_list.append(full_url)

    print(f"Found {len(articles_urls_list)} article URLs for today.")
    return articles_urls_list

def save_articles_urls(articles_urls):
    with open("articles_urls.json", "w") as file:
        json.dump(articles_urls, file)

def load_articles_urls():
    try:
        with open("articles_urls.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def find_new_articles():
    current_articles_urls = get_articles_urls()
    known_articles_urls = load_articles_urls()

    new_articles_urls = [url for url in current_articles_urls if url not in known_articles_urls]

    if new_articles_urls:
        for url in new_articles_urls:
            article_data = get_article(url)
            if article_data:
                send_messages(article_data['image_url'], article_data['title'], article_data['text'])

        # Обновляем список известных статей
        save_articles_urls(current_articles_urls)


# Пример использования
find_new_articles()
