import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_project_syndicate(url):
    """Scrapes a specific section of Project Syndicate using Selenium."""
    print(f"Scraping Project Syndicate URL: {url}")
    articles = []
    options = Options()
    options.add_argument("--headless")
    if shutil.which('firefox'):
        options.binary_location = shutil.which('firefox')
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(15)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        for tag in soup.select('h2 a, h3 a'):
            if tag.get('href') and tag.get_text(strip=True):
                title = tag.get_text(strip=True)
                news_url = tag['href'] if tag['href'].startswith('http') else 'https://www.project-syndicate.org' + tag['href']
                articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> Project Syndicate Error on {url}: {e}")
    finally:
        if driver: driver.quit()
    return list({v['url']:v for v in articles}.values())
