import aiohttp
import asyncio
from bs4 import BeautifulSoup
import random
import json
import requests
import datetime

headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
}
url = 'https://936.shop.onliner.by/categories/elektronika?on_sale=1'

async def fetch(session, url):
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def get_product_info(url):
    async with aiohttp.ClientSession() as session:
        await asyncio.sleep(random.uniform(10, 30))  # Add a random delay between 10 and 30 seconds
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        product_items = soup.find_all("div", class_="catalog-form__offers-flex")

        products = []
        for counter, item in enumerate(product_items, start=1):
            try:
                link = item.find("div", class_="catalog-form__description catalog-form__description_primary catalog-form__description_base-additional catalog-form__description_font-weight_semibold catalog-form__description_condensed-other").find('a')['href']
                name = item.find("div", class_="catalog-form__description catalog-form__description_primary catalog-form__description_base-additional catalog-form__description_font-weight_semibold catalog-form__description_condensed-other").find('a').text.strip()
                price = item.find("div", class_="catalog-form__description catalog-form__description_huge-additional catalog-form__description_font-weight_bold catalog-form__description_condensed-default catalog-form__description_error-alter").text.strip()

                product = {
                    "name": name,
                    "price": price,
                    "link": link
                }
                products.append(product)
            except AttributeError:
                print("Error: Failed to extract information for product", counter)

        return products

# Telegram Bot API settings
telegram_token = '6230573565:AAGro7qOktJvU_4hzvIFazZkT9UUDug1r8g'
channel_id = '@texm_by'

def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {
        'chat_id': channel_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram. Status code:", response.status_code)

async def write_to_file(data, filename):
    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(data, file)

async def main():
    products = await get_product_info(url)

    # Load previously published products
    today = datetime.date.today()
    filename = f"published_products_{today}.json"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            published_products = json.load(file)
    except FileNotFoundError:
        published_products = []

    new_products = []
    for product in products:
        if product not in published_products:
            new_products.append(product)

    if new_products:
        # Publish new products
        for product in new_products[:6]:
            name = product["name"]
            price = product["price"]
            link = product["link"]

            message = f"<b>{name}</b>\nЦена: {price}: <a href='{link}'>Купить по лучшей цене в Минске</a>"
            send_message_to_telegram(message)

            # Add published product to the list
            published_products.append(product)

        # Save the updated published products
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(published_products, file)

async def run():
    while True:
        await main()
        await asyncio.sleep(100)  # Sleep for 1 hour (3600 seconds)

if __name__ == '__main__':
    asyncio.run(run())
