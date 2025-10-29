from news_site.washingtonpost2 import scrape_washington_post_news
from news_site.economist import scrape_economist_news
from news_site.projectsyndicate import scrape_project_syndicate_news
from datetime import datetime


current_date = datetime.now()
current_date = current_date.strftime("%Y-%m-%d %H:%M:%S")



if __name__ == "__main__":

    with open("news.txt", "w") as f:
        f.write(f"News collected on: {current_date}")

    scrape_economist_news()
    scrape_project_syndicate_news()
    scrape_washington_post_news()



