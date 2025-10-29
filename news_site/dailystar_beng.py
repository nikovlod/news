import requests
from bs4 import BeautifulSoup
import time


def scrape_daily_star_news():
    print("Scraping Dailystar")
    # URL of the page to scrape
    base_url = "https://bangla.thedailystar.net/"
    
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    with open("./news/index.html", "a") as f:
        f.write("<h2 id = dailystar>News from Daily Star</h2>")


    try:
        # Make a request to get the HTML content of the page
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'lxml')

        # Find the news container - adjust the selector based on the actual HTML structure
        news_container = soup.find('div', class_='view-content')  # Update this selector
        if not news_container:
            print("Could not find news container. The website structure might have changed.")
            return

        # Find all news articles
        news_articles = news_container.find_all('h3', class_='title')

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
                    news_url = 'https://www.thedailystar.net' + news_url
                    with open("./news/index.html","a") as f:
                        f.write(f"<h4><a class='list-group-item list-group-item-action list-group-item-info' href={news_url}>{news_title}</a></h4>\n")

                else:
                    print(f"Could not find article content for: {news_title}")

            except Exception as e:
                print(f"Error processing article: {str(e)}")
                continue

    except requests.RequestException as e:
        print(f"Error fetching the webpage: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")




