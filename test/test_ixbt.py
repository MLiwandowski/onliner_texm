import requests
from bs4 import BeautifulSoup
import asyncio
import json
from random import randrange
from typing import List
import time
from telegram import Bot
import aiohttp

URL_IXBT = "https://www.ixbt.com/news/?show=tape"

KEYWORDS = ["Audi", "Ford", "Great Wall", "Changan", "Chery", "Chevrolet", "GAC", "Geely", "Hyundai", "Honda",
            "Lada", "Land Rover", "Lexus", "Lynk & Co", "Mercedes", "Peugeot", "Porsche",
            "Suzuki", "Toyota", "Subaru", "Skoda", "Volkswagen", "Tesla", "кроссовер", "Нива"]

headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}

def get_articles_urls_ixbt(url: str) -> str:
    with requests.Session() as s:
        response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    articles_urls = soup.find_all("h2", class_="no-margin")

    articles_urls_list = []
    for au in articles_urls:
        art_url = "https://www.ixbt.com/" + au.find("a")["href"]
        articles_urls_list.append(art_url)

    time.sleep(randrange(20, 50))
    with open("articles_url_list_auto.txt", "w", encoding="utf-8") as file:
        for url in articles_urls_list:
            file.write(f"{url}\n")

    return "Работа по сбору ссылок выполнена"

get_articles_urls_ixbt(URL_IXBT)
# ///////////////////////////////////////////////////////////////
def get_data_ixbt(file_path: str, keywords: List[str]) -> None:
    with open(file_path) as file:
        url_list = [line.strip() for line in file.readlines()]

    urls_count = len(url_list)
    s = requests.Session()
    result_data = []

    for idx, url in enumerate(url_list[:25]):
        response = s.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")

        articles = soup.find_all("div", class_="b-article__header")
        if articles:
            article_title = articles[0].find("h1").text.strip()
            article_img = f"https://www.ixbt.com{soup.find('figure', class_='image-caption').find('img').get('src')}"

            article_text = []
            for p in soup.find_all("p"):
                article_text.append(p.text.strip().replace('\n', ''))
            article_text = '\n'.join(article_text)
            article_text = article_text[:article_text.rfind(' 2023 в ')]

            # Check if article contains any of the keywords
            if any(keyword.lower() in article_text.lower() for keyword in keywords):
                article_text = article_text.split('\n')
                # Remove everything after the publication date
                publication_date_index = next(
                    (i for i, s in enumerate(article_text) if 'Дата публикации' in s), None)
                if publication_date_index is not None:
                    article_text = '\n'.join(article_text[:publication_date_index])
                else:
                    article_text = '\n'.join(article_text)

                print(f"{article_title}\n{article_text}\n{article_img}\n{'#' * 10}")

                result_data.append(
                    {
                        "original_url": url,
                        "article_title": article_title,
                        "article_img": article_img,
                        "article_text": article_text,
                    }
                )
            else:
                print(f"Слова не найдены в статье {article_title}")

        print(f"Обработано {idx + 1}/{urls_count}")

    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)

get_data_ixbt('articles_url_list_auto.txt', KEYWORDS)
# ///////////////////////////////////////////////////////////
async def publish_articles():
    # Read data from result.json
    with open('result.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Initialize your Telegram bot
    bot_token = '5815887474:AAFz40K4cbeUjuZOhXQni2K-_gPSF5Dfr5I'
    # bot_token = '6230573565:AAGro7qOktJvU_4hzvIFazZkT9UUDug1r8g'
    bot = Bot(token=bot_token)

    # Define your Telegram channel ID
    channel_id = '@autonewsok'
    # channel_id = '@texm_by'

    # Load the previously published articles
    try:
        with open('published_articles_auto.json', 'r', encoding="utf-8") as file:
            published_articles = json.load(file)
    except FileNotFoundError:
        published_articles = []

    new_articles = []
    delay_seconds = 2  # Customize the delay duration in seconds
    for article in data:
        article_title = article['article_title']
        article_img = article['article_img']
        article_text = article['article_text']
        article_link = article['original_url']

        # Check if the article has already been published
        if article_title not in published_articles:
            # Create the message with the title, article text, and image link
            message = f"<a href='{article_img}'>&#8205;</a>\n<b>{article_title}</b>\n{article_text}\n\n<a href='{article_link}'>Читать полностью...</a>"

            # message = f"<a href='{article_img}'>&#8205;</a>\n{article_title}\n{article_text}\n\n<a href='{article_link}'>Читать полностью...</a>"
            new_articles.append({'article_title': article_title})

            try:
                # Publish the article to your Telegram channel
                await bot.send_message(chat_id=channel_id, text=message, parse_mode='HTML')
                # Add the published article to the list
                published_articles.append(article_title)
                # Delay between publishing each article
                await asyncio.sleep(delay_seconds)
            except Exception as e:
                print(f"Error publishing article: {article_title}\n{e}")

    # Write the updated published articles list to published_articles_auto.json
    with open('published_articles_auto.json', 'w', encoding="utf-8") as file:
        json.dump(published_articles, file, indent=4, ensure_ascii=False)

    print("Publishing completed.")

# Run the publishing function
asyncio.run(publish_articles())
