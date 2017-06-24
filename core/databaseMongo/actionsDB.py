#!thesis/DB
import mainDB

def insertAction(name, value):
    db = mainDB.db
    a = db.actions
    av = db.actionsAV

    value["_id"] = name
    a.insert_one(value)
    
    avObj = {"_id": name, "nodes": []}
    av.insert_one(avObj)

    return name


def getAction(name):
    db = mainDB.db
    a = db.actions

    return a.find_one({"_id" : name})


def availableActionName(name):
    db = mainDB.db
    a = db.actions
    n = a.find({"_id" : name}).count()
    
    return n == 0
    

def deleteAction(token):
    db = mainDB.db
    a = db.actions
    av = db.actionsAV

    a.remove({"_id" : token})
    av.remove({"_id" : token})


def updateAvailability(actName, nodeTokens):
    db = mainDB.db
    av = db.actionsAV

    tokens = nodeTokens
    if type(nodeTokens) != list:
        tokens = [nodeTokens]

    val = av.find_one({"_id" : actName})
    for t in tokens:
        val["nodes"].append(t)

    av.find_one_and_replace({"_id" : actName}, val)


def getAvailability(actName):
    db = mainDB.db
    av = db.actionsAV

    r = av.find_one({"_id": actName})

    return r["nodes"]


# remove the node ref from the availability list
def removeNodeAV(nodeToken):
    db = mainDB.db
    av = db.actionsAV

    for a in av.find():
        id = a["_id"]

        try:
            a["nodes"].remove(nodeToken)
            av.find_one_and_replace({"_id": id}, a)
        except ValueError:
            pass


def getActions():
    db = mainDB.db
    a = db.actions

    ret = []
    for k in a.find():
        data = {
            "name": k["_id"],
            "description": k["description"],
            "in/out": k["in/out"]
        }
        ret.append(data)

    return ret
