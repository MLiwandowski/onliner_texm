#добываем ссылки на новые статьи из ixbt.com/news

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ixbt.config import HEADERS

# Формируем URL с текущей датой
today_date = datetime.now().strftime("%Y/%m/%d")
URL_IXBT = f"https://www.ixbt.com/news/{today_date}/"

def get_articles_urls_ixbt() -> list:
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
        if url.startswith(f"/news/{today_date}") and url not in articles_urls_list and not url.endswith("#comments"):
            full_url = f"https://www.ixbt.com{url}"
            articles_urls_list.append(full_url)

    print(f"Found {len(articles_urls_list)} article URLs for today.")
    return articles_urls_list


# # Тестируем функцию
# urls = get_articles_urls_ixbt()
# for url in urls:
#     print(url)
