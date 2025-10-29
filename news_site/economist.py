import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_economist_news():
    print("Scraping The Economist...")
    url = "https://www.economist.com/"
    articles = []
    
    options = Options()
    options.add_argument("--headless")
    
    # Auto-detect Firefox binary location.
    firefox_path = shutil.which('firefox')
    if firefox_path:
        options.binary_location = firefox_path
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(15)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for headline_link in soup.select('h1 a, h2 a, h3 a'):
            if headline_link and headline_link.get('href'):
                title = headline_link.get_text(strip=True)
                news_url = 'https://www.economist.com' + headline_link['href'] if not headline_link['href'].startswith('http') else headline_link['href']
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> The Economist: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

    return list({v['url']:v for v in articles}.values())
