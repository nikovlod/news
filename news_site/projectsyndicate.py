import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_project_syndicate_news():
    print("Scraping Project Syndicate...")
    url = "https://www.project-syndicate.org/"
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
        main_content = soup.find('main', id='main')
        if not main_content:
            return articles

        for h2_tag in main_content.find_all("h2"):
            a_tag = h2_tag.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.get_text(strip=True)
                news_url = 'https://www.project-syndicate.org' + a_tag['href'] if not a_tag['href'].startswith('http') else a_tag['href']
                if title and news_url:
                    articles.append({'title': title, 'url': news_url})
    except Exception as e:
        print(f"-> Project Syndicate: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            
    return list({v['url']:v for v in articles}.values())
