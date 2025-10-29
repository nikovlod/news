import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_bonik_barta(url):
    """Scrapes a specific section of Bonik Barta using Selenium."""
    print(f"Scraping Bonik Barta URL: {url}")
    articles = []
    options = Options()
    options.add_argument("--headless")
    if shutil.which('firefox'):
        options.binary_location = shutil.which('firefox')
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(12)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        for tag in soup.select('h1 a, h2 a, h3 a'):
            if tag.get('href') and tag.get_text(strip=True):
                title = tag.get_text(strip=True)
                news_url = tag['href'] if tag['href'].startswith('http') else 'https://bonikbarta.com' + tag['href']
                articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> Bonik Barta Error on {url}: {e}")
    finally:
        if driver: driver.quit()
    return list({v['url']:v for v in articles}.values())
