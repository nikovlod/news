# news_site/prothomalo.py
import requests
from bs4 import BeautifulSoup

def scrape_prothom_alo_news():
    """Scrapes news titles and URLs from the Prothom Alo homepage."""
    print("Scraping Prothom Alo...")
    url = "https://www.prothomalo.com/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    articles = []
    seen_urls = set()

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all link tags that likely contain news headlines
        headline_links = soup.select('a[aria-label]')

        if not headline_links:
            print("-> Prothom Alo: No headline links found. Page structure may have changed.")
            return articles

        for link in headline_links:
            news_url = link.get('href')
            if not news_url or news_url in seen_urls:
                continue

            # Attempt to find a title within the link tag
            title_tag = link.find(['h1', 'h2', 'h3', 'h4', 'span'])
            title = title_tag.get_text(strip=True) if title_tag else link.get('aria-label', '').strip()

            if not news_url.startswith('http'):
                news_url = 'https://www.prothomalo.com' + news_url

            if title and news_url:
                articles.append({'title': title, 'url': news_url})
                seen_urls.add(news_url)

    except requests.RequestException as e:
        print(f"-> Prothom Alo: Error fetching the page: {e}")
    except Exception as e:
        print(f"-> Prothom Alo: An unexpected error occurred: {e}")

    return articles
