from mySqlBase import *


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