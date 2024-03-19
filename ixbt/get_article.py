# добывает из статьи заголовок, текст и фото

import requests
from bs4 import BeautifulSoup

def get_article(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Получение заголовка
    title_element = soup.find('h1', id='newsheader')
    if title_element:
        title = title_element.text.strip()
    else:
        # Если заголовок не найден, возвращаем None или подходящее сообщение об ошибке
        return None

    # Получение текста статьи
    article_body = soup.find('div', itemprop='articleBody')
    if article_body:
        paragraphs = article_body.find_all('p')
        text = '\n'.join([paragraph.text.strip() for paragraph in paragraphs if paragraph.text.strip()])
    else:
        # Если тело статьи не найдено, возвращаем None или подходящее сообщение об ошибке
        return None

    # Получение URL изображения
    image = article_body.find('div', class_='image-center').find('img') if article_body else None
    image_url = 'https://www.ixbt.com' + image['src'] if image else None

    return {
        'title': title,
        'text': text,
        'image_url': image_url
    }


# # URL статьи
# article_url = 'https://www.ixbt.com/news/2024/03/19/sony-playstation-5-pro.html'
#
# # Получение и вывод деталей статьи
# article_details = get_article (article_url)
# print(article_details)
