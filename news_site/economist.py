# news_site/economist.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_economist_news():
    """Scrapes news titles and URLs from The Economist homepage using Selenium."""
    print("Scraping The Economist...")
    url = "https://www.economist.com/"
    articles = []
    
    options = Options()
    options.add_argument("--headless")
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(15)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Find links within header tags (h1, h2, h3)
        for headline_link in soup.select('h1 a, h2 a, h3 a'):
            if headline_link and headline_link.get('href'):
                title = headline_link.get_text(strip=True)
                news_url = headline_link['href']
                
                if not news_url.startswith('http'):
                    news_url = 'https://www.economist.com' + news_url
                
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})

    except Exception as e:
        print(f"-> The Economist: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

    unique_articles = list({v['url']:v for v in articles}.values())
    return unique_articles
