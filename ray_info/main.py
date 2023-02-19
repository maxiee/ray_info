from playwright.sync_api import sync_playwright
from ray_info.db import Record, UserDict, db, Info
from ray_info.fenci.fenci import init_jieba

from ray_info.rss import init_rss_config_to_tasks, read_rss_config
from ray_info.scheduler.scheduler import Scheduler
import datetime
import time
import threading

from ray_info.server.server_main import server_main

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("http://playwright.dev")
#     print(page.title())
#     browser.close()

db.connect()
db.create_tables([Info, Record, UserDict], safe=True)

init_jieba()

scheduler = Scheduler()
init_rss_config_to_tasks(scheduler)

thread_server = threading.Thread(target=server_main)
thread_server.start()

while True:
    print("=======================")
    print(datetime.datetime.now())
    print(scheduler)
    ret = scheduler.getOnTimeTask()
    if ret is not None:
        print(f"执行 {ret.name}")
        ret.run()
    time.sleep(5)
