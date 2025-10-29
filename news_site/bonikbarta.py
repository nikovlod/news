# news_site/bonikbarta.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_bonik_barta_news():
    print("Scraping Bonik Barta...")
    url = "https://bonikbarta.com/"
    articles = []
    options = Options()
    options.add_argument("--headless")
    
    driver = None
    try:
        # CORRECTED INITIALIZATION: No hardcoded service path needed.
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(10)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        for headline_tag in soup.select('h2 a, h3 a'):
            if headline_tag and headline_tag.get('href'):
                title = headline_tag.get_text(strip=True)
                news_url = headline_tag['href']
                
                if not news_url.startswith('http'):
                    news_url = 'https://bonikbarta.com' + news_url
                
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})
                    
    except Exception as e:
        print(f"-> Bonik Barta: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            
    unique_articles = list({v['url']:v for v in articles}.values())
    return unique_articles
