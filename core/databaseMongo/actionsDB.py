#!thesis/DB
import mainDB

db = mainDB.db
a = db.actions
dep = db.dependencies

def insertAction(name, value):

    value["_id"] = name
    a.insert_one(value)
    """
    avObj = {"_id": name, "nodes": []}
    av.insert_one(avObj)
    """
    depRecord = {"_id": name, "dep": []}
    dep.insert_one(depRecord)
    
    return name


def getAction(name):

    return a.find_one({"_id" : name})


def availableActionName(name):
    n = a.find({"_id" : name}).count()
    
    return n == 0
    

def deleteAction(token):
    from sequencesDB import deleteSequence

    ret = a.find_one_and_delete({"_id" : token})
    
    deplist = dep.find_one_and_delete({"_id" : token})
    for dep in deplist["dep"]:
        if not availableActionName(dep):
            deleteAction(dep)
        else:
            deleteSequence(dep)

    return ret

def removeAWS():
    


"""
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
"""

def getActions():
    ret = []
    for k in a.find():
        data = {
            "name": k["_id"],
            "description": k["description"],
            "in/out": k["in/out"]
        }
        ret.append(data)

    return ret
