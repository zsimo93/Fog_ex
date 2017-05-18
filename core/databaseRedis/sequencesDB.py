from mainDB import Database
from actionsDB import availableActionName as notPresent
import json


def insertSequence(token, value):
    db = Database().db

    val = json.dumps(value)
    
    db.set("SEQ_" + token, val)

    return token


def availableSeqName(name):
    db = Database().db

    keys = db.keys("SEQ_*")

    newK = list(map(lambda x: x[4:], keys))

    ret = True
    try:
        newK.index(name)
        ret = False
    except ValueError:
        pass
    return ret


def deleteSequence(token):
    db = Database().db
    
    db.delete("SEQ_" + token)


def getSequences():
    db = Database().db

    keys = db.keys("SEQ_*")
    ret = []
    for k in keys:
        data = {
            "name": k[4:],
            "description": db.get(k)["description"]
        }
        ret.append(data)

    return ret

# return the first incorrect name, none if all actions are ok
def checkSequence(list):
    flatten = [item for sublist in list for item in sublist]

    for a in flatten:
        if notPresent(a):
            return a

    return None
