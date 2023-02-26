from pathlib import Path

# 数据存储目录，更换为你自己的
DATA_PATH = Path("D:\\Ray\\RaySystem\\ray_info")

WEIBO_STORAGE = DATA_PATH.joinpath('weibo.json')

# 存放 RSS Feed 源
RSS_CONFIGS = DATA_PATH.joinpath("rss.yaml")

# SQLite 数据库
DB_PATH = DATA_PATH.joinpath('ray_info.db')

ONE_HOUR = 3600 # 1小时=3600秒
ONE_MINUTE = 60

SERVER_BUSY = False
DB_BUSY = False