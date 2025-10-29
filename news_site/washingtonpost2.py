# news_site/washingtonpost2.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_washington_post_news():
    """Scrapes news titles and URLs from The Washington Post homepage using Selenium."""
    print("Scraping The Washington Post...")
    url = "https://www.washingtonpost.com/"
    articles = []
    
    options = Options()
    options.add_argument("--headless")
    
    driver = None
    try:
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(20) # This site can be slow to fully load dynamic content
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # The main content area helps to filter out non-article links
        main_content = soup.find('main', id='main-content')
        if not main_content:
            print("-> Washington Post: Main content area not found.")
            return articles

        for h2_tag in main_content.find_all("h2"):
            a_tag = h2_tag.find('a')
            if a_tag and a_tag.get('href'):
                title = a_tag.get_text(strip=True)
                news_url = a_tag['href']
                
                # The URL is already absolute on this site
                if title and news_url.startswith('http'):
                    articles.append({'title': title, 'url': news_url})

    except Exception as e:
        print(f"-> Washington Post: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
            
    unique_articles = list({v['url']:v for v in articles}.values())
    return unique_articles
