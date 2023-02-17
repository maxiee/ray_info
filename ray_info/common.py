from pathlib import Path

# 数据存储目录，更换为你自己的
DATA_PATH = Path("D:\\SynologyDrive\\ray_info")

# 存放 RSS Feed 源
RSS_CONFIGS = DATA_PATH.joinpath("rss.yaml")

# SQLite 数据库
DB_PATH = DATA_PATH.joinpath('ray_info.db')