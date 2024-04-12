from peewee import *
import datetime
import config
import peeweedbevolve

db = PostgresqlDatabase(config.DB_NAME, user=config.DB_USERNAME, password=config.DB_PASSWORD, host='alexnum_postgres')
#db = SqliteDatabase('karma.db')

class BaseModel(Model):
    class Meta:
        database = db
    
class User(BaseModel):
    telegram_id = TextField()
    registration_date = DateTimeField(default=datetime.datetime.now())
    
with db.atomic():
    #db.drop_tables([User])
    try:
        db.create_tables([User])
    except:
        db.evolve(interactive=True)
    
    #migrate(
    #    migrator.add_column('user', 'order_type', order_type))    
    

