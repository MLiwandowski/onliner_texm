# отправляет текст в Телеграм канал

import requests
from ixbt.config import HEADERS, BOT_TOKEN, CHANNEL_ID
from get_article import get_article

def send_messages(photo_url, title, text):
    # Обрезка текста до 1024 символов с учётом заголовка и HTML-разметки
    max_caption_length = 1024
    base_caption = f'<b>{title}</b>\n\n{text}'
    # Учёт HTML-тегов в подсчёте длины
    actual_length = len(base_caption.encode('utf-16-le')) // 2  # Примерное кол-во символов с учётом UTF-16

    if actual_length > max_caption_length:
        # Оставляем место для многоточия и закрывающего тега
        available_text_length = max_caption_length - len('<b></b>\n\n...') - len(title.encode('utf-16-le')) // 2
        text = text[:available_text_length] + "..."
        caption = f'<b>{title}</b>\n\n{text}'
    else:
        caption = base_caption

    data = {
        'chat_id': CHANNEL_ID,
        'photo': photo_url,
        'caption': caption,
        'parse_mode': 'HTML'
    }
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', json=data, headers=HEADERS)
    print(response.text)

# # Пример использования
# article_url = 'https://www.ixbt.com/news/2024/03/19/sony-playstation-5-pro.html'
# article_data = get_article(article_url)  # Получаем данные статьи
# send_messages(article_data['image_url'], article_data['title'], article_data['text'])
