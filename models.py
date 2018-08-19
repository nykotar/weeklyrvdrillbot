from peewee import *
import datetime
import config

db = SqliteDatabase(config.DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

class Image(BaseModel):
    link = CharField(unique=True)
    animated = BooleanField()
    assigned = BooleanField(default=False)

class Target(BaseModel):
    image = ForeignKeyField(Image, backref="targets")
    target_id = CharField(unique=True)
    assigned_date = DateTimeField(default=datetime.datetime.now)
    requested_by = CharField()
    revelation_date = DateTimeField(null=True)
    times_revealed = IntegerField(default=0)
