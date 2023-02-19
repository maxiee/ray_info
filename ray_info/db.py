from peewee import *

from ray_info.common import DB_PATH

db = SqliteDatabase(DB_PATH)

class Info(Model):
    title = CharField()
    updated = DateTimeField()
    url = CharField()
    site = CharField()
    description = CharField()
    like = IntegerField()

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