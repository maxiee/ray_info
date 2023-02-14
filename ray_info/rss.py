from ray_info.common import RSS_CONFIGS
import yaml
import feedparser

from ray_info.utils.html_utils import strip_tags


def read_rss_config():
    with open(RSS_CONFIGS, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def parse_feed(url):
    feed = feedparser.parse(url)
    ret = []
    for entry in feed.entries:
        ret.append(
            {
                "title": entry.title,
                "updated": entry.updated,
                "url": entry.link,
                "description": strip_tags(entry.summary),
            }
        )
    return ret
