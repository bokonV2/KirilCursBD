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
    try:
        user = Users.select()\
            .where(Users.number == number, Users.password == password)\
            .get()
        return model_to_dict(user)
    except: 
        return False

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

def removeItemCart(user_id, item_index):
    cart = Carts.select().where(Carts.user_id == user_id).get()
    dCart = model_to_dict(cart)
    items = json.loads(dCart['items_list'])
    items.pop(item_index)
    cart.items_list = json.dumps(items)
    cart.save()


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

def cartSubmit(user_id, fullPrice, addres):
    cart = Carts.select().where(Carts.user_id == user_id).get()
    order = Orders.create(
        user_id = user_id,
        items_list = cart.items_list,
        fullPrice = fullPrice, 
        addres = addres
    )
    cart.delete_instance()
    return order

def getOrder(id):
    return Orders.select().where(Orders.id == id).get()

def getAllOrders():
    return Orders.select()

def getAllUsers():
    return Users.select()