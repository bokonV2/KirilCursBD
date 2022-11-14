from mySqlBase import *
from playhouse.shortcuts import model_to_dict, dict_to_model
import json

def getSections():
    return Sections.select()

def getAllSupersections():
    supersectionsList = [
        Supersections.select().where(Supersections.section == 1),
        Supersections.select().where(Supersections.section == 2),
        Supersections.select().where(Supersections.section == 3),
        Supersections.select().where(Supersections.section == 4),
        Supersections.select().where(Supersections.section == 5),
    ]
    return supersectionsList

def getAllItems(id):
    return Items.select().where(Items.section == id)

def addNewSection(name, section_id):
    Supersections.create(name=name, section_id=section_id)

def addNewItem(name, image, count, coast, description, section_id):
    Items.create(
        name=name,
        image=image,
        count=count,
        coast=coast,
        description=description,
        section_id=section_id
    )

def registerNewUser(name, lastName, number, mail, password):
    Users.create(
        name = name,
        lastName = lastName,
        number = number,
        mail = mail,
        password = password,
    )

def userLogin(number, password):
    user = Users.select()\
        .where(Users.number == number, Users.password == password)\
        .get()
    return model_to_dict(user)

def addItemTocart(user_id, item_id):
    print(user_id)
    try:
        cart = Carts.select().where(Carts.user_id == user_id).get()
        dCart = model_to_dict(cart)
        items = json.loads(dCart['items_list'])
        items.append(item_id)
        cart.items_list = json.dumps(items)
        cart.save()
    except:
        cart = Carts.create(
            user_id = user_id,
            items_list = [item_id, ]
        )
        pass

def getCartLen(user_id):
    try:
        cart = Carts.select().where(Carts.user_id == user_id).get()
        dCart = model_to_dict(cart)
        items = json.loads(dCart['items_list'])
        return len(items)
    except:
        return 0

def getAllCart(user_id):
    cart = Carts.select().where(Carts.user_id == user_id).get()
    dCart = model_to_dict(cart)
    items = json.loads(dCart['items_list'])
    products = []
    for item in items:
        products.append(
            Items.select().where(Items.id == item).get()
        )
    fullPrice = 0
    for item in products:
        fullPrice += item.coast
    return products, fullPrice