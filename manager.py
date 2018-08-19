import peewee
import imgurpython
from models import *
import config
import asyncio

class Manager:

    def __init__(self):
        db = peewee.SqliteDatabase(config.DB_NAME)
        try:
            db.create_tables([Image, Target])
            print("Database created.")
        except peewee.OperationalError:
            print("Database loaded.")

    async def refreshpool(self, images):
        for img in images:
            Image.create(link=img.link, animated=img.animated)
            await asyncio.sleep(0.2) #Needed so the bot doesnt freeze (probably not the best solution)
    
    def poolinfo(self):
        return Image.select().count()