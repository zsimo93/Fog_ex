from core.databaseMongo.mainDB import c as mongoclient
from datetime import datetime
from core.container.dockerInterface import killContainer, getContList

availableCont = mongoclient.local.avCont
allCont = mongoclient.local.allCont
allCont.create_index("createTime", expireAfterSeconds=300)

def insertContainer(actionName, contId, ip):
    inDB = {
        "_id": contId,
        "actionName": actionName,
        "ip": ip,
    }
    availableCont.insert_one(inDB)

def findContainer(actionName):
    cont = availableCont.find_one_and_delete({"actionName": actionName})
    if cont:
        id = cont["_id"]
        ip = cont["ip"]
        updateTimeout(id)
        return id, ip
    return None

def insertInAll(contId, actionName):
    if not updateTimeout(contId):
        inDB = {
            "_id": contId,
            "actionName": actionName,
            "createTime": datetime.utcnow()
        }
        allCont.insert_one(inDB)

def updateTimeout(contId):
    newCont = allCont.find_one({"_id": contId})
    if newCont:
        newCont["createTime"] = datetime.utcnow()
        allCont.find_one_and_replace({"_id": contId}, newCont)
        return True
    return False

def deleteActionContainers(actName):
    found = allCont.find_one({"actionName": actName})
    while found:
        id = found["_id"]
        ac = availableCont.find_one_and_delete({"_id": id})
        if not ac:
            continue
        else:
            allCont.find_one_and_delete({"_id": id})
            killContainer(id)

        found = allCont.find_one({"actionName": actName})


def removeTimedOutCont():
    import time
    while (True):
        for container in getContList():
            cname = container.name
            if cname not in ("mongoDB", "coreGateway"):
                # DON'T TERMINATE mongo and core containers
                try:
                    if not allCont.find_one({"_id": cname}):
                        container.kill()
                        container.remove()
                except Exception:
                    pass
        time.sleep(10)
