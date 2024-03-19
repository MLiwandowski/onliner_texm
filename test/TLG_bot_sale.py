import json
import asyncio
from telegram import Bot

# Load data from JSON file
with open('result_onliner.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize Telegram bot with API token
bot = Bot('5815887474:AAFz40K4cbeUjuZOhXQni2K-_gPSF5Dfr5I')

# Keep track of the last sent article
last_sent = ''

async def main():
    global last_sent  # use global variable
    # Loop through each article in data
    for article in data:
        # Check if the article has a different title and URL from the last sent article
        if article['article_title'] != last_sent and article['original_url'] != last_sent:
            # Create the HTML message with a link to the title and the image
            title_link = f"<a href='{article['original_url']}'>{article['article_title']}</a>"
            message = f"{title_link}\n\n{article['article_text']}"

            # Send message to Telegram channel
            await bot.send_message(chat_id='@texnomir_sale', text=message, parse_mode='HTML', disable_web_page_preview=False)
            print('Sent message:', message)

            # Update last sent article
            last_sent = article['article_title']
            await asyncio.sleep(20)  # Wait 20 seconds before sending the next message

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
