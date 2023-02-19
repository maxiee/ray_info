from ray_info.common import ONE_HOUR, RSS_CONFIGS
import yaml
import feedparser
import datetime
from ray_info.db import Info
from ray_info.scheduler.scheduler import Scheduler, Task
import time
from peewee import DoesNotExist
from ray_info.utils.html_utils import strip_tags


class RSSTask(Task):
    def __init__(self, name, url, repeat=False, repeat_period=0) -> None:
        super().__init__(f"RSS任务={name}", time.time() + 5, True, ONE_HOUR * 8)
        self.url = url

    def run(self):
        feed = feedparser.parse(self.url)
        for entry in feed.entries:
            title = entry.title
            updated = entry.updated  # 字符串类型
            updated_datetime = datetime.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%SZ")
            url = entry.link
            description = strip_tags(entry.summary, limit=128)

            try:
                info = Info.get(Info.url == url)
            except DoesNotExist:
                info = Info.create(
                    title=title,
                    updated=updated_datetime,
                    url=url,
                    description=description)


def read_rss_config():
    with open(RSS_CONFIGS, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def init_rss_config_to_tasks(scheduler: Scheduler):
    config = read_rss_config()["feeds"]
    for entry in config:
        scheduler.addTask(RSSTask(
            entry['name'],
            entry['url']
        ))
