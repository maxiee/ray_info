from ray_info.common import RSS_CONFIGS
import yaml


def read_rss_config():
    with open(RSS_CONFIGS, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())
