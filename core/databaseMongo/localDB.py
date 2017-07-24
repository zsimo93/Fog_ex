from datetime import datetime
from core.container.dockerInterface import killContainer, getContList
from pymongo import MongoClient

mongoclient = MongoClient(host='localhost', port=27017,
                          readPreference='nearest')
availableCont = mongoclient.local.avCont
allCont = mongoclient.local.allCont
allCont.create_index("createTime", expireAfterSeconds=60)

def insertContainer(actionName, contId, ip):
    # insert container in availableDB.
    inDB = {
        "_id": contId,
        "actionName": actionName,
        "ip": ip,
    }
    availableCont.insert_one(inDB)
    insertInAll(contId, actionName)

def findContainer(actionName):
    # if container available, delete from available and update t-o in all.
    cont = availableCont.find_one_and_delete({"actionName": actionName})
    if cont:
        id = cont["_id"]
        ip = cont["ip"]
        updateTimeout(id)
        return id, ip
    return None

def insertInAll(contId, actionName):
    # if container alreasy in ALL update t-o, otherwise insert.
    if not updateTimeout(contId):
        inDB = {
            "_id": contId,
            "actionName": actionName,
            "createTime": datetime.utcnow()
        }
        allCont.insert_one(inDB)

def updateTimeout(contId):
    # if container in allDB update t-o and return true.
    # return False otherwise
    newCont = allCont.find_one({"_id": contId})
    if newCont:
        newCont["createTime"] = datetime.utcnow()
        allCont.find_one_and_replace({"_id": contId}, newCont)
        return True
    return False

def deleteActionContainers(actName):
    # delete all containers of a certain actionand kill them
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
        clist = getContList()
        for container in clist:
            cname = container.name
            if cname not in ("mongoDB", "coreGateway"):
                # DON'T TERMINATE mongo and core containers
                try:
                    if not allCont.find_one({"_id": cname}):
                        print "DELETING " + cname
                        container.kill()
                        container.remove(v=True)
                        availableCont.delete_one({"_id": cname})
                except Exception:
                    pass
        time.sleep(30)
