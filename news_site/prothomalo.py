# news_site/prothomalo.py
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_prothom_alo(url):
    """Scrapes a specific section of Prothom Alo using Selenium."""
    print(f"Scraping Prothom Alo URL: {url}")
    articles = []
    options = Options()
    options.add_argument("--headless")
    if shutil.which('firefox'):
        options.binary_location = shutil.which('firefox')
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        # Wait for the dynamic content to load
        time.sleep(12) 
        
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # This selector remains very effective for finding headlines
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
    finally:
        if driver:
            driver.quit()
            
    # Return a list of unique articles
    return list({v['url']:v for v in articles}.values())
