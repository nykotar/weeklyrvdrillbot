import random
import datetime
import peewee
import asyncio
import imgurpython
from models import *
import config

class Manager:

    db = peewee.SqliteDatabase(config.DB_NAME)

    def load(self):
        self.db.create_tables([Image, Target])
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
    
    def __gen_number(self):
        return "{}-{}".format("%04d" % random.randint(0,9999), "%04d" % random.randint(0,9999))

    def __gen_target_id(self):
        target_id = self.__gen_number()

        while Target.select().where(Target.target_id == target_id).exists():
            target_id = self.__gen_number()

        return target_id

    def new_target(self, author):
        image = Image.select().order_by(fn.Random()).limit(1)[0]
        target_id = self.__gen_target_id()
        
        target = Target()
        target.image = image
        target.target_id = target_id
        target.requested_by = author.name
        target.save()
        
        image.assigned = True
        image.save()
        return target_id
    
    def get_target(self, target_id):
        try:
            target = Target.get(Target.target_id == target_id)
            if not target.revelation_date:
                target.revelation_date = datetime.datetime.now()
            target.times_revealed += 1
            target.save()
            return target
        except DoesNotExist:
            return None
    
    def poolinfo(self):
        return Image.select().count()