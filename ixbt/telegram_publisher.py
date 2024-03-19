import asyncio
from telegram import Bot
from config import BOT_TOKEN, CHANNEL_ID
from utils import load_json, save_json

async def publish_articles(data):
    bot = Bot(token=BOT_TOKEN)

    published_articles = load_json('published_articles_auto.json', default=[])

    delay_seconds = 2  # Customize the delay duration in seconds
    for article in data:
        if article['article_title'] not in published_articles:
            message = "<a href='{article_img}'>&#8205;</a>\n<b>{article_title}</b>\n{article_text}\n\n<a href='{article_link}'>Читать полностью...</a>".format(**article)
            try:
                await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
                published_articles.append(article['article_title'])
                await asyncio.sleep(delay_seconds)
            except Exception as e:
                print(f"Error publishing article: {article['article_title']}\n{e}")

    save_json(published_articles, 'published_articles_auto.json')
    print("Publishing completed.")
