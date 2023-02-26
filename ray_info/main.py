import datetime
import threading
import time

from playwright.sync_api import sync_playwright
from ray_info.common import DB_BUSY, SERVER_BUSY

from ray_info.db import Info, Record, UserDict, db
from ray_info.fenci.fenci import init_jieba
from ray_info.rss import init_rss_config_to_tasks, read_rss_config
from ray_info.scheduler.scheduler import Scheduler
from ray_info.server.server_main import server_main
from ray_info.site.weibo.weibo import WeiboTask

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
scheduler.addTask(WeiboTask())
init_rss_config_to_tasks(scheduler)

thread_server = threading.Thread(target=server_main)
thread_server.start()

while True:
    print("=======================")
    print(datetime.datetime.now())
    print(scheduler)

    if SERVER_BUSY:
        print('PunkOS 访问中，调度器暂停工作')
        time.sleep(30)
        continue

    ret = scheduler.getOnTimeTask()
    if ret is not None:
        DB_BUSY = True
        print(f"执行 {ret.name}")
        ret.run()
        DB_BUSY = False
    time.sleep(5)
