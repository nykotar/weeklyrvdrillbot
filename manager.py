import peewee
from models import *
import config

class Manager:

    def __init__(self):
        db = peewee.SqliteDatabase(config.DB_NAME)
        try:
            db.create_tables([Image, Target])
            print("Database created.")
        except peewee.OperationalError:
            print("Database loaded.")
    
    