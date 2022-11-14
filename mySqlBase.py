from peewee import *

mysql_db = MySQLDatabase('kiril', user='root', password='root')

class BaseModel(Model):
    class Meta:
        database = mysql_db

class Users(BaseModel):
    name = TextField()
    lastName = TextField()
    number = IntegerField()
    mail = TextField()
    password = TextField()

class Carts(BaseModel):
    user_id = ForeignKeyField(Users)
    items_list = TextField()

class Orders(BaseModel):
    user = ForeignKeyField(Users)
    items_list = TextField()
    date = DateTimeField()

class Sections(BaseModel):
    name = TextField()

class Supersections(BaseModel):
    name = TextField()
    section = ForeignKeyField(Sections, backref='section')

class Items(BaseModel):
    name = TextField()
    image = TextField()
    count = IntegerField()
    coast = IntegerField()
    description = TextField()
    section = ForeignKeyField(Supersections)
