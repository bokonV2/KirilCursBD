from mySqlBase import *


def getSections():
    return Sections.select()

def getAllSupersections():
    a = Supersections.select().where(Supersections.section == 1)
    for tweet in a:
        print(tweet.name, '->', tweet.id)
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