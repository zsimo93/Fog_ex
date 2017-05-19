from mainDB import Database
from actionsDB import availableActionName as notPresent


def insertSequence(name, value):
    db = Database().db
    s = db.sequences

    value["_id"] = name
    s.insert_one(value)
    
    return name


def availableSeqName(name):
    db = Database().db
    s = db.sequences

    n = s.find({"_id" : name}).count()
    
    return n == 0


def deleteSequence(token):
    db = Database().db
    s = db.sequences
    
    s.remove({"_id" : token})


def getSequences():
    db = Database().db
    s = db.sequences

    ret = []
    for k in s.find():
        data = {
            "name": k["_id"],
            "description": k["description"]
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
