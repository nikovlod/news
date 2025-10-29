# news_scrape.py
import json
import os
from datetime import datetime, timedelta, timezone

# --- Import all your scraper functions ---
from news_site.dailystar import scrape_daily_star_news
from news_site.prothomalo import scrape_prothom_alo_news
from news_site.bonikbarta import scrape_bonik_barta_news
from news_site.washingtonpost2 import scrape_washington_post_news
from news_site.economist import scrape_economist_news
from news_site.projectsyndicate import scrape_project_syndicate_news
from news_site.gitupload import push_to_github

# --- Configuration ---
NEWS_SOURCES = [
    {"id": "dailystar", "name": "Daily Star", "function": scrape_daily_star_news},
    {"id": "prothomalo", "name": "Prothom Alo", "function": scrape_prothom_alo_news},
    {"id": "bonikbarta", "name": "Bonik Barta", "function": scrape_bonik_barta_news},
    {"id": "economist", "name": "The Economist", "function": scrape_economist_news},
    {"id": "projectsyndicate", "name": "Project Syndicate", "function": scrape_project_syndicate_news},
    {"id": "washingtonpost", "name": "The Washington Post", "function": scrape_washington_post_news},
]

REPO_PATH = "./news/"
DATA_FILE_PATH = os.path.join(REPO_PATH, "news_data.json")
INDEX_HTML_PATH = os.path.join(REPO_PATH, "index.html")
ARCHIVE_HTML_PATH = os.path.join(REPO_PATH, "archive.html")

# --- Data Management Functions ---
def load_existing_data(filepath):
    """Loads news data from the JSON file."""
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data, filepath):
    """Saves the updated news data to the JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# --- HTML Generation Functions ---
def generate_html_page(title, nav_links, content, timestamp):
    """Generic HTML page generator."""
    nav_html = ''.join(f'<li><a href="{link["href"]}">{link["text"]}</a></li>' for link in nav_links)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
</head>
<body>
<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <div class="navbar-header"><a class="navbar-brand" href="#">News Today</a></div>
    <div class="collapse navbar-collapse" id="myNavbar"><ul class="nav navbar-nav">{nav_html}</ul></div>
  </div>
</nav>
<div class="container">
    <marquee>News last updated on: {timestamp}</marquee>
    {content}
</div>
</body>
</html>'''

def generate_news_content(all_data, time_filter):
    """Generates the HTML content for news articles based on a filter."""
    content_html = ""
    for source_config in NEWS_SOURCES:
        source_id = source_config["id"]
        source_name = source_config["name"]
        
        articles = all_data.get(source_id, [])
        filtered_articles = time_filter(articles)

        if filtered_articles:
            content_html += f"<br><h2 id='{source_id}'>News from {source_name}</h2>"
            for article in filtered_articles:
                content_html += f"<h4><a class='list-group-item list-group-item-action list-group-item-info' href='{article['url']}' target='_blank'>{article['title']}</a></h4>\n"
    return content_html

def generate_archive_content(all_data):
    """Generates grouped HTML content for the archive page."""
    archive_articles = []
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    
    # Collect all articles older than 24 hours
    for source_id in all_data:
        for article in all_data[source_id]:
            scraped_time = datetime.fromisoformat(article['scraped_at'])
            if scraped_time < one_day_ago:
                archive_articles.append(article)
    
    # Sort articles by date, newest first
    archive_articles.sort(key=lambda x: x['scraped_at'], reverse=True)

    # Group articles by date
    articles_by_date = {}
    for article in archive_articles:
        date_str = datetime.fromisoformat(article['scraped_at']).strftime('%Y-%m-%d, %A')
        if date_str not in articles_by_date:
            articles_by_date[date_str] = []
        articles_by_date[date_str].append(article)

    # Generate HTML for grouped articles
    archive_html = ""
    if not articles_by_date:
        return "<h3>No news in the archive yet.</h3>"

    for date_str, articles in articles_by_date.items():
        archive_html += f"<br><h3>{date_str}</h3>"
        for article in articles:
            archive_html += f"<h4><a class='list-group-item list-group-item-action' href='{article['url']}' target='_blank'>{article['title']}</a></h4>\n"
            
    return archive_html

# --- Main Execution Logic ---
if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    thirty_days_ago = now - timedelta(days=30)
    
    # 1. Load existing data
    all_news_data = load_existing_data(DATA_FILE_PATH)
    
    print("--- Starting News Scraping & Merging Cycle ---")
    for source in NEWS_SOURCES:
        source_id = source["id"]
        source_name = source["name"]
        
        # Get existing URLs for this source to check for duplicates
        current_articles = all_news_data.get(source_id, [])
        existing_urls = {article['url'] for article in current_articles}
        
        # Scrape for new articles
        new_articles = source["function"]()
        
        new_found_count = 0
        for article in new_articles:
            if article['url'] not in existing_urls:
                article['scraped_at'] = now.isoformat()
                current_articles.append(article)
                existing_urls.add(article['url'])
                new_found_count += 1
        
        all_news_data[source_id] = current_articles
        print(f"-> {source_name}: Found {len(new_articles)} articles, {new_found_count} were new.")

    # 2. Purge data older than 30 days
    print("\n--- Purging old data (older than 30 days) ---")
    purged_data = {}
    for source_id, articles in all_news_data.items():
        articles_within_30_days = [
            article for article in articles
            if datetime.fromisoformat(article['scraped_at']) > thirty_days_ago
        ]
        purged_data[source_id] = articles_within_30_days
        
    # 3. Save the updated and purged data
    save_data(purged_data, DATA_FILE_PATH)
    print(f"Data saved to {DATA_FILE_PATH}")
    
    # 4. Generate HTML files
    print("\n--- Generating HTML Files ---")
    current_timestamp = now.strftime("%Y-%m-%d %I:%M:%S %p %Z")

    # Generate index.html (last 24 hours)
    index_nav = [
        {'text': 'Home', 'href': 'index.html'},
        {'text': 'News Archive', 'href': 'archive.html'}
    ]
    index_filter = lambda articles: [a for a in articles if datetime.fromisoformat(a['scraped_at']) > one_day_ago]
    index_content = generate_news_content(purged_data, index_filter)
    index_html = generate_html_page("Today's News", index_nav, index_content, current_timestamp)
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"Generated {INDEX_HTML_PATH}")

    # Generate archive.html (older than 24 hours)
    archive_nav = [
        {'text': 'Home', 'href': 'index.html'},
        {'text': 'News Archive', 'href': 'archive.html'}
    ]
    archive_content = generate_archive_content(purged_data)
    archive_html = generate_html_page("News Archive", archive_nav, archive_content, current_timestamp)
    with open(ARCHIVE_HTML_PATH, "w", encoding="utf-8") as f:
        f.write(archive_html)
    print(f"Generated {ARCHIVE_HTML_PATH}")

    # 5. Push to GitHub
    print("\n--- Pushing to GitHub ---")
    try:
        push_to_github(REPO_PATH, f"News update {current_timestamp}")
        print("Successfully pushed to GitHub repository.")
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")

    print("\n--- Cycle Complete ---")
