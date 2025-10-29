# news_scrape.py
import json
import os
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# --- Import all scraper functions ---
from news_site.dailystar import scrape_daily_star
from news_site.prothomalo import scrape_prothom_alo
from news_site.bonikbarta import scrape_bonik_barta
from news_site.washingtonpost2 import scrape_washington_post
from news_site.economist import scrape_economist
from news_site.projectsyndicate import scrape_project_syndicate

# --- Configuration for all news sources and their subsections ---
NEWS_SOURCES = {
    "dailystar": {
        "name": "The Daily Star", "scraper": scrape_daily_star,
        "subsections": {
            "Home": "https://www.thedailystar.net/", "Today's News": "https://www.thedailystar.net/todays-news",
            "Opinion": "https://www.thedailystar.net/opinion", "Business": "https://www.thedailystar.net/business",
            "Editorial": "https://www.thedailystar.net/opinion/editorial", "Politics": "https://www.thedailystar.net/politics",
            "International": "https://www.thedailystar.net/news/world",
        }
    },
    "prothomalo": {
        "name": "Prothom Alo", "scraper": scrape_prothom_alo,
        "subsections": {
            "Home": "https://www.prothomalo.com/", "Latest News": "https://www.prothomalo.com/collection/latest",
            "Opinion": "https://www.prothomalo.com/opinion", "Editorial": "https://www.prothomalo.com/opinion/editorial",
            "Business": "https://www.prothomalo.com/business", "Politics": "https://www.prothomalo.com/politics",
            "International": "https://www.prothomalo.com/world",
        }
    },
    "bonikbarta": {
        "name": "Bonik Barta", "scraper": scrape_bonik_barta,
        "subsections": {
            "Home": "https://www.bonikbarta.com/", "Latest News": "https://bonikbarta.com/latest",
            "Editorial": "https://bonikbarta.com/editorial/", "Economy": "https://bonikbarta.com/economy/",
            "International": "https://bonikbarta.com/international/",
        }
    },
    "washingtonpost": {
        "name": "The Washington Post", "scraper": scrape_washington_post,
        "subsections": {
            "Home": "https://www.washingtonpost.com/", "Opinions": "https://www.washingtonpost.com/opinions/",
            "Business": "https://www.washingtonpost.com/business/", "Politics": "https://www.washingtonpost.com/politics/",
            "International": "https://www.washingtonpost.com/world/",
        }
    },
    "economist": {
        "name": "The Economist", "scraper": scrape_economist,
        "subsections": {
            "Home": "https://www.economist.com/", "Columns": "https://www.economist.com/topics/columns",
            "Leaders": "https://www.economist.com/topics/leaders", "Business": "https://www.economist.com/topics/business",
            "Finance & Economics": "https://www.economist.com/topics/finance-and-economics", "International": "https://www.economist.com/topics/international",
        }
    },
    "projectsyndicate": {
        "name": "Project Syndicate", "scraper": scrape_project_syndicate,
        "subsections": {
            "Home": "https://www.project-syndicate.org/", "Economics": "https://www.project-syndicate.org/section/economics",
            "Politics": "https://www.project-syndicate.org/section/politics-world-affairs", "Sustainability": "https://www.project-syndicate.org/section/environment-sustainability",
        }
    }
}

REPO_PATH = "."
DATA_FILE_PATH = os.path.join(REPO_PATH, "news_data.json")
INDEX_HTML_PATH = os.path.join(REPO_PATH, "index.html")
ARCHIVE_INDEX_PATH = os.path.join(REPO_PATH, "archive.html")

# --- Helper Functions ---
def load_data():
    if not os.path.exists(DATA_FILE_PATH): return {}
    try:
        with open(DATA_FILE_PATH, 'r', encoding='utf-8') as f: return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError): return {}

def save_data(data):
    with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f: json.dump(data, f, indent=2)

def generate_html_shell(title, content, timestamp):
    """Generates the full HTML page with corrected UI, search, and nested accordions."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | News Today</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
        body {{ background-color: #f8f9fa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 16px; }}
        .navbar-inverse {{ background-color: #343a40; border-color: #23272b; }}
        .main-container {{ padding-top: 70px; }}
        .panel-group .panel {{ border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 0; border: 1px solid #e3e3e3; }}
        .panel-group .panel + .panel {{ margin-top: 10px; }}
        .panel-heading {{ border-radius: 3px 3px 0 0; }}
        .panel-default > .panel-heading {{ background-color: #fff; color: #333; }}
        .panel-title > a {{ display: block; padding: 12px 15px; text-decoration: none; font-weight: bold; font-size: 18px; color: #333; }}
        .panel-title > a:hover, .panel-title > a:focus {{ color: #000; }}
        .sub-panel .panel-heading {{ background-color: #f9f9f9; }}
        .sub-panel .panel-title > a {{ font-size: 16px; font-weight: normal; color: #555; }}
        .list-group-item {{ border-left: none; border-right: none; font-size: 16px; }}
        a.list-group-item {{ color: #337ab7; }} a.list-group-item:hover {{ background-color: #f0f8ff; }}
        .search-bar-container {{ position: sticky; top: 51px; background-color: #f8f9fa; padding: 10px 0; z-index: 1020; margin-bottom: 15px; border-bottom: 1px solid #eee; }}
        .footer-note {{ text-align: center; padding: 25px 0; color: #999; }}
    </style>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
  <div class="container-fluid">
    <div class="navbar-header"><a class="navbar-brand" href="index.html">News Today</a></div>
    <ul class="nav navbar-nav"><li><a href="index.html">Home (24h)</a></li><li><a href="archive.html">Archive</a></li></ul>
  </div>
</nav>
<div class="container main-container">
    <div class="search-bar-container"><input type="text" id="searchInput" class="form-control" placeholder="Search for articles..."></div>
    <p class="text-center text-muted" style="margin-bottom:15px;">Last updated on: {timestamp}</p>
    {content}
    <p class="footer-note">End of results</p>
</div>
<script>
$(document).ready(function() {{
    // CORRECTED ACCORDION LOGIC: Only affects siblings within the same panel-group.
    $('.panel-group').on('show.bs.collapse', function (e) {{
        $(e.target).closest('.panel-group').find('.panel-collapse.in').not(e.target).collapse('hide');
    }});

    // CORRECTED SEARCH FUNCTIONALITY
    $('#searchInput').on('keyup', function() {{
        let searchTerm = $(this).val().toLowerCase().trim();

        if (searchTerm === "") {{
            $('.news-item, .sub-panel, .main-panel').show();
            $('.panel-collapse').collapse('hide');
            return;
        }}

        $('.main-panel').each(function() {{
            let mainPanel = $(this);
            let mainHasVisible = false;

            mainPanel.find('.sub-panel').each(function() {{
                let subPanel = $(this);
                let subHasVisible = false;

                subPanel.find('.news-item').each(function() {{
                    let item = $(this);
                    if (item.text().toLowerCase().includes(searchTerm)) {{
                        item.show();
                        subHasVisible = true;
                    }} else {{
                        item.hide();
                    }}
                }});

                if (subHasVisible) {{
                    subPanel.show();
                    mainHasVisible = true;
                }} else {{
                    subPanel.hide();
                }}
            }});

            if (mainHasVisible) {{
                mainPanel.show();
                mainPanel.children('.panel-collapse').collapse('show');
            }} else {{
                mainPanel.hide();
            }}
        }});
    }});
}});
</script>
</body></html>'''

def generate_content_html(data, time_filter=None):
    """Generates the nested accordion HTML for news content."""
    main_accordion_id = 'main-accordion'
    content_html = f'<div class="panel-group" id="{main_accordion_id}">'
    
    for i, (source_id, config) in enumerate(NEWS_SOURCES.items()):
        source_data = data.get(source_id, {})
        
        sub_accordion_id = f'sub-accordion-{source_id}'
        sub_panels_html = ""
        
        for j, (sub_name, articles) in enumerate(source_data.items()):
            filtered_articles = time_filter(articles) if time_filter else articles

            if filtered_articles:
                article_html = "".join([f"<div class='list-group-item news-item'><a href='{a['url']}' target='_blank'>{a['title']}</a></div>" for a in filtered_articles])
                sub_panels_html += f'''
                <div class="panel panel-default sub-panel">
                    <div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#{sub_accordion_id}" href="#collapse-{source_id}-sub-{j}">{sub_name}</a></h4></div>
                    <div id="collapse-{source_id}-sub-{j}" class="panel-collapse collapse"><div class="list-group">{article_html}</div></div>
                </div>'''
        
        if sub_panels_html:
            content_html += f'''
            <div class="panel panel-default main-panel">
                <div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#{main_accordion_id}" href="#collapse-main-{i}">{config["name"]}</a></h4></div>
                <div id="collapse-main-{i}" class="panel-collapse collapse">
                    <div class="panel-body"><div class="panel-group" id="{sub_accordion_id}">{sub_panels_html}</div></div>
                </div>
            </div>'''
            
    content_html += '</div>'
    return content_html

# --- Main Execution Logic ---
if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    one_day_ago = now - timedelta(days=1)
    thirty_days_ago = now - timedelta(days=30)
    
    all_data = load_data()
    
    print("--- Starting Full Scrape & Merge Cycle ---")
    for source_id, config in NEWS_SOURCES.items():
        if source_id not in all_data or not isinstance(all_data.get(source_id), dict):
            all_data[source_id] = {}
        for sub_name, url in config['subsections'].items():
            if sub_name not in all_data[source_id]: all_data[source_id][sub_name] = []
            current_articles = all_data[source_id][sub_name]
            existing_urls = {a['url'] for a in current_articles}
            new_articles = config['scraper'](url)
            new_found = 0
            for article in new_articles:
                if article['url'] not in existing_urls:
                    article['scraped_at'] = now.isoformat()
                    current_articles.append(article)
                    new_found += 1
            print(f"-> {config['name']} ({sub_name}): Scraped {len(new_articles)}, Added {new_found} new.")
            all_data[source_id][sub_name] = [a for a in current_articles if datetime.fromisoformat(a['scraped_at']) > thirty_days_ago]
    
    save_data(all_data)
    print("\n--- Data saved to news_data.json ---")

    print("\n--- Generating HTML Files ---")
    timestamp = now.strftime("%Y-%m-%d %I:%M:%S %p %Z")

    # Generate index.html (Last 24 Hours)
    index_filter = lambda articles: [a for a in articles if datetime.fromisoformat(a['scraped_at']) > one_day_ago]
    index_content = generate_content_html(all_data, time_filter=index_filter)
    with open(INDEX_HTML_PATH, "w", encoding="utf-8") as f: f.write(generate_html_shell("Today's News", index_content, timestamp))
    print(f"Generated {INDEX_HTML_PATH}")

    # Generate Monthly Archives
    archive_articles = [a for src in all_data.values() for sub in src.values() for a in sub if datetime.fromisoformat(a['scraped_at']) <= one_day_ago]
    monthly_archives = defaultdict(list)
    for article in archive_articles: monthly_archives[datetime.fromisoformat(article['scraped_at']).strftime('%Y-%m')].append(article)

    archive_links = []
    for month_key, articles in sorted(monthly_archives.items(), reverse=True):
        month_name = datetime.strptime(month_key, '%Y-%m').strftime('%B %Y')
        archive_filename = f"archive_{month_key}.html"
        archive_links.append({"name": month_name, "file": archive_filename})
        articles.sort(key=lambda x: x['scraped_at'], reverse=True)
        
        archive_data_for_month = defaultdict(lambda: defaultdict(list))
        for article in articles:
             for sid, config in NEWS_SOURCES.items():
                 for sub_name, sub_articles in all_data.get(sid, {}).items():
                     if any(a['url'] == article['url'] for a in sub_articles):
                         archive_data_for_month[sid][sub_name].append(article)
                         break
                 else: continue
                 break
        
        month_content = f'<h2>Archive for {month_name}</h2>' + generate_content_html(archive_data_for_month)
        with open(os.path.join(REPO_PATH, archive_filename), "w", encoding="utf-8") as f: f.write(generate_html_shell(f"Archive: {month_name}", month_content, timestamp))
        print(f"Generated {archive_filename}")

    # Generate Main Archive Index Page
    archive_index_content = "<h2>News Archives by Month</h2><div class='list-group'>" + ("".join([f"<a href='{link['file']}' class='list-group-item'>{link['name']}</a>" for link in archive_links]) or "<p>No archived news available yet.</p>") + "</div>"
    with open(ARCHIVE_INDEX_PATH, "w", encoding="utf-8") as f: f.write(generate_html_shell("Archive Index", archive_index_content, timestamp))
    print(f"Generated {ARCHIVE_INDEX_PATH}")
    
    print("\n--- Python script complete. Handing over to workflow for git push. ---")
