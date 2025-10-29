import requests
from bs4 import BeautifulSoup

def scrape_prothom_alo(url):
    """Scrapes a specific section of Prothom Alo."""
    print(f"Scraping Prothom Alo URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')

        for link in soup.select('a[aria-label]'):
            if link.get('href'):
                title = link.get('aria-label', '').strip()
                news_url = link['href']
                if not news_url.startswith('http'):
                    news_url = 'https://www.prothomalo.com' + news_url
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> Prothom Alo Error on {url}: {e}")
    return list({v['url']:v for v in articles}.values())
