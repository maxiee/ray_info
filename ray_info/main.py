from playwright.sync_api import sync_playwright
from ray_info.db import db, Info

from ray_info.rss import init_rss_config_to_tasks, read_rss_config
from ray_info.scheduler.scheduler import Scheduler

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("http://playwright.dev")
#     print(page.title())
#     browser.close()

db.connect()
db.create_tables([Info], safe=True)

scheduler = Scheduler()
init_rss_config_to_tasks(scheduler)


