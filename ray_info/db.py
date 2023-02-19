from peewee import *

from ray_info.common import DB_PATH

db = SqliteDatabase(DB_PATH)

class Info(Model):
    title = CharField()
    updated = DateTimeField()
    url = CharField()
    description = CharField()

    class Meta:
        database = db

class Record(Model):
    name = CharField()
    latest = IntegerField()

    class Meta:
        database = db