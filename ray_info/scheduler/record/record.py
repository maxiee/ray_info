import peewee
import time
from ray_info.db import Record
# 用于判断上次行为时间，避免重复拉取

def is_record_need_action(name: str, interval: int) -> bool:
    """
    name: 行为名称
    interval: 时间间隔
    """
    try:
        record = Record.get(Record.name==name)
        # now 一定大于 ts
        now = time.time()
        ts = record.latest

        # 如果距离上次动作时间超过间隔，需要重新动作
        return now - ts > interval

    except peewee.DoesNotExist:
        return True

def update_record_latest(name: str):
    now = time.time()
    try:
        record = Record.get(Record.name==name)
        record.latest = now
        record.save()
    except peewee.DoesNotExist:
        record = Record.create(
            name=name,
            latest=now
        )