import peewee
import asyncio
import imgurpython
from models import *
import config

class Manager:

    db = peewee.SqliteDatabase(config.DB_NAME)

    def load(self):
        try:
            self.db.create_tables([Image, Target])
            print("Database created.")
        except peewee.OperationalError:
            print("Database loaded.")


    def add_image(self, image):
        try:
            Image.create(link=image.link, animated=image.animated)
            return True
        except IntegrityError:
            return False

    async def add_images(self, images):
        count = len(images)
        with self.db.atomic():
            for image in images:
                try:
                    Image.create(link=image.link, animated=image.animated)
                except IntegrityError:
                    count -= 1
                await asyncio.sleep(0.2) #Needed so the bot doesnt freeze (probably not the best solution)
        print("Added %d images." % count)
        return count
    
    def poolinfo(self):
        return Image.select().count()