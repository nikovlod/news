# news_site/prothomalo.py
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

def scrape_prothom_alo(url):
    """Scrapes a specific section of Prothom Alo using Selenium with targeted logic."""
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
        # Wait for the dynamic content and article cards to load
        time.sleep(12) 
        
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # --- NEW LOGIC ---
        # 1. Find all parent containers for the articles.
        article_cards = soup.find_all('div', class_='card-with-image-zoom')

        if not article_cards:
            print(f"-> Prothom Alo: Could not find any 'card-with-image-zoom' divs on {url}. The site structure may have changed.")
            # As a fallback, try the old method
            for link in soup.select('a[aria-label]'):
                 if link.get('href'):
                    title = link.get('aria-label', '').strip()
                    news_url = 'https://www.prothomalo.com' + link['href'] if not link['href'].startswith('http') else link['href']
                    if title and news_url:
                        articles.append({'title': title, 'url': news_url})
            return list({v['url']:v for v in articles}.values())

        for card in article_cards:
            title = None
            news_url = None

            # 2. Find the link tag specifically with class 'title-link'
            link_tag = card.find('a', class_='title-link')
            if link_tag and link_tag.get('href'):
                news_url = link_tag['href']

            # 3. Find the title from the specific span tag
            title_tag = card.find('span', class_='tilte-no-link-parent')
            if title_tag:
                title = title_tag.get_text(strip=True)
            
            # If the title span isn't found, try the aria-label as a backup
            elif link_tag and link_tag.get('aria-label'):
                 title = link_tag.get('aria-label', '').strip()

            # 4. Add the data if both title and url were found
            if title and news_url:
                if not news_url.startswith('http'):
                    news_url = 'https://www.prothomalo.com' + news_url
                articles.append({'title': title, 'url': news_url})
                
    except Exception as e:
        print(f"-> Prothom Alo Error on {url}: {e}")
    finally:
        if driver:
            driver.quit()
            
    # Return a list of unique articles to avoid duplicates
    return list({v['url']:v for v in articles}.values())
