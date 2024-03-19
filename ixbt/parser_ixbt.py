import requests
from bs4 import BeautifulSoup

# The URL of the news site
url = 'https://www.ixbt.com/news/'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Assuming the news items are contained in a specific class, you would find all instances of that class
# This is an example and may need adjustment based on the actual page structure
news_items = soup.find_all('div', class_='news-item-class')  # Replace 'news-item-class' with the correct class name

# Extract and print the title and URL of each news item
for item in news_items:
    title = item.find('a').get_text()  # Find the title
    link = item.find('a')['href']  # Find the URL
    print(f"Title: {title}, Link: {link}")
