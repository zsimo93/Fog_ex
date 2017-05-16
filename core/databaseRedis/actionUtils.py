#!thesis/DB

from mainDB import Database
import json


def insertAction(token, value):
    db = Database().db

    val = json.dumps(value)
    
    db.set("ACT_" + token, val)
    db.lpush("AV_" + token, [])

    return token


def availableActionName(name):
    db = Database().db

    keys = db.keys("ACT_*")

    newK = list(map(lambda x: x[4:], keys))

    ret = True
    try:
        newK.index(name)
        ret = False
    except ValueError:
        pass
    return ret
    

def deleteAction(token):
    db = Database().db
    
    db.delete("ACT_" + token)
    db.delete("AV_" + token)


def updateAvailability(actToken, nodeToken):
    db = Database().db

    db.lpush("AV_" + actToken, nodeToken)


def getActions():
    db = Database().db

    keys = db.keys("ACT_*")
    newK = list(map(lambda x: x[4:], keys))

    return newK

    
# remove the node ref from the availability list
def removeNodeAV(tokenNode):
    db = Database().db

    keys = db.keys("AV_*")

    for k in keys:
        db.lrem(k, 1, tokenNode)