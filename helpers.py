from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Define the date range
def date_range(): 
    print('Getting the date range...')
    now = datetime.utcnow()
    past24hrs = now - timedelta(hours=168)
    date_range = past24hrs.strftime('%Y-%m-%d..')

    return date_range

# Haal de zinvolle info van de pagina op
def get_page_info(page):
    print('Getting the page info...')
    soup = BeautifulSoup(page.content, 'html.parser')
    gpt4_paragraphs = soup.find_all('p', string=lambda text: text and 'gpt-4' in text.lower())
    gpt4_paragraphs = [p for p in gpt4_paragraphs if 'gpt-4' in p.text.lower()]

    return gpt4_paragraphs

# Filter de items die niet relevant zijn
def filter_func(item):
    return not (item['link'].startswith('https://chrome.google.com') or 
                item['link'].startswith('https://chat.openai.com/') or
                item['link'].startswith('https://www.usnews.com/'))



