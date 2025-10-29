import requests
from bs4 import BeautifulSoup

def scrape_daily_star(url):
    """Scrapes a specific section of The Daily Star."""
    print(f"Scraping Daily Star URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        
        headline_tags = soup.select('.card-title a, h3.title a, h2.title a, h1.title a')
        if not headline_tags:
            headline_tags = soup.select('a h4, a h3, a h2')

        for tag in headline_tags:
            if tag.get('href') and tag.get_text(strip=True):
                title = tag.get_text(strip=True)
                news_url = tag['href']
                if not news_url.startswith('http'):
                    news_url = 'https://www.thedailystar.net' + news_url
                articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> Daily Star Error on {url}: {e}")
    return list({v['url']:v for v in articles}.values())
