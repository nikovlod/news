from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from bs4 import BeautifulSoup
import random

def scrape_washington_post_news():
# Set up Firefox options
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Run in headless mode
    firefox_options.set_preference("javascript.enabled", False)


# Set the path to the Geckodriver executable
    geckodriver_service = Service('/usr/local/bin/geckodriver')

# Initialize the WebDriver
    driver = webdriver.Firefox(service=geckodriver_service, options = firefox_options)

    
    with open("news_english.txt", "a") as f:
        f.write("\n\nNews from Washington Post")

# Example usage: open a webpage
    driver.get('https://www.washingtonpost.com/')

    time.sleep(20)

    page_source = driver.page_source

# Use BeautifulSoup to parse the rendered HTML
    soup = BeautifulSoup(page_source, 'lxml')

# Now you can extract content as needed
    news_container = soup.find('main', id = 'main-content')

    news_articles = news_container.find_all("h2")

#input(len(news_articles))

    for article in news_articles:
        try:
            a_tag = article.find('a')
            if not a_tag:
                continue

            news_title = a_tag.get_text(strip=True)
            news_url = a_tag.get('href')
            
            if not news_url:
                continue

            # Construct full URL if needed
            if not news_url.startswith('http'):
                news_url = 'https://www.washingtonpost.com' + news_url

            #print(news_url + "\n")


            # Add a delay to prevent overwhelming the server
            #time.sleep(2)

            # Make a request to the news URL
            driver.get(news_url)

            time.sleep(random.randrange(20,40))

            news_response = driver.page_source

            news_soup = BeautifulSoup(news_response, 'lxml')

            # Find the main article content container
            article_container = news_soup.find('article', {'data-qa':'main'})  # Update this selector
            
            if article_container:
                # Get all paragraphs from the article container
                
                p_tags = article_container.find_all('p', attrs={'data-testid': True})

                #p_tags = article_container.select('p:not([class])')

                news_content = '\n'.join([p.get_text(strip=True) for p in p_tags if p.get_text(strip=True)])

#            input(news_content)


                with open("news_english.txt", "a") as f:
                    f.write(f"\n\nTitle: {news_title}\n\n")
                    f.write(f"URL: {news_url}\n\n")
                    f.write(f"Content: {news_content}\n\n")
                    f.write("="*80)
                    print(f"Added {news_title}\n")

            else:
                print(f"Could not find article content for: {news_title}")


        except Exception as e:
            print(f"Error processing article: {str(e)}")
            continue


#print(content.text)

# Quit the WebDriver
    driver.quit()

if __name__ == "__main__":
    scrape_washington_post_news()
