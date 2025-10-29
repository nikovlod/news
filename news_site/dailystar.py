# news_site/dailystar.py
import requests
from bs4 import BeautifulSoup

def scrape_daily_star_news():
    """Scrapes news titles and URLs from The Daily Star homepage."""
    print("Scraping The Daily Star...")
    url = "https://www.thedailystar.net/todays-news"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    articles = []

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        soup = BeautifulSoup(response.content, 'lxml')
        news_container = soup.find('div', class_='view-content')

        if not news_container:
            print("-> Daily Star: News container not found. Page structure may have changed.")
            return articles

        for h3_tag in news_container.find_all('h3', class_='title'):
            a_tag = h3_tag.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.get_text(strip=True)
                news_url = a_tag['href']
                
                if not news_url.startswith('http'):
                    news_url = 'https://www.thedailystar.net' + news_url
                
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})

    except requests.RequestException as e:
        print(f"-> Daily Star: Error fetching the page: {e}")
    except Exception as e:
        print(f"-> Daily Star: An unexpected error occurred: {e}")
        
    return articles
