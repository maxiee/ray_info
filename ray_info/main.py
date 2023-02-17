from playwright.sync_api import sync_playwright
from ray_info.db import db, Info

from ray_info.rss import parse_feed, read_rss_config

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("http://playwright.dev")
#     print(page.title())
#     browser.close()

db.connect()
db.create_tables([Info], safe=True)

config = read_rss_config()
print(str(config))

for info in parse_feed(config["feeds"][0]["url"]):
    print(info["title"])
    print(info["url"])
    print(info["description"][:50])
    print("\n\n")
