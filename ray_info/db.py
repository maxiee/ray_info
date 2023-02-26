from peewee import *

from ray_info.common import DB_PATH

db = SqliteDatabase(DB_PATH)

db_busy = False

class Info(Model):
    title = CharField()
    updated = DateTimeField()
    url = CharField()
    site = CharField()
    site_img = CharField()
    description = CharField()
    like = IntegerField()
    # 图片 url 的 JSON List 字符串
    images = CharField()

    class Meta:
        database = db

class Record(Model):
    name = CharField()
    latest = IntegerField()

    class Meta:
        database = db

class UserDict(Model):
    word = CharField()
    freq = IntegerField()
    tag = CharField()
    like = IntegerField()

    class Meta:
        database = db