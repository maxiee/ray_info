from playwright.sync_api import sync_playwright
from ray_info.db import Record, db, Info

from ray_info.rss import init_rss_config_to_tasks, read_rss_config
from ray_info.scheduler.scheduler import Scheduler
import datetime
import time

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("http://playwright.dev")
#     print(page.title())
#     browser.close()

db.connect()
db.create_tables([Info, Record], safe=True)

scheduler = Scheduler()
init_rss_config_to_tasks(scheduler)


while True:
    print('=======================')
    print(datetime.datetime.now())
    print(scheduler)
    ret = scheduler.getOnTimeTask()
    if ret is not None:
        print(f'执行 {ret.name}')
        ret.run()
    time.sleep(5)