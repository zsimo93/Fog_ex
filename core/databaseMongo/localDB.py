from datetime import datetime, timedelta
from core.container.dockerInterface import (killContainer,
                                            getUsedMem)
from pymongo import MongoClient

mongoclient = MongoClient(host='localhost', port=27017,
                          readPreference='nearest')
availableCont = mongoclient.local.avCont
allCont = mongoclient.local.allCont
timedelta = timedelta(seconds=60)
# allCont.create_index("createTime", expireAfterSeconds=60)
# availableCont.create_index("createTime", expireAfterSeconds=60)

def insertContainer(actionName, contId, ip, loglength):
    # insert container in availableDB.
    memused, createTime = insertInAll(contId, actionName)
    inDB = {
        "_id": contId,
        "actionName": actionName,
        "memused": memused,
        "ip": ip,
        "loglength": loglength,
        "createTime": createTime
    }
    availableCont.insert_one(inDB)

def findContainer(actionName):
    # if container available, delete from available and update t-o in all.
    cont = availableCont.find_one_and_delete({"actionName": actionName})
    if cont:
        id = cont["_id"]
        ip = cont["ip"]
        logl = cont["loglength"]
        updateTimeout(id)
        return id, ip, logl
    return None

def insertInAll(contId, actionName, loglength=0):
    # if container alreasy in ALL update t-o, otherwise insert.
    # return base memory used by container
    memused, createTime = updateTimeout(contId)
    if not memused:
        # create new container
        memused = getUsedMem(contId)
        createTime = datetime.utcnow()
        inDB = {
            "_id": contId,
            "actionName": actionName,
            "memused": memused,
            "loglength": loglength,
            "createTime": createTime
        }
        allCont.insert_one(inDB)
    return memused, createTime

def updateTimeout(contId):
    # if container in allDB update t-o and return base memory used by container
    # return None otherwise
    newCont = allCont.find_one({"_id": contId})
    if newCont:
        newCont["createTime"] = datetime.utcnow()
        allCont.find_one_and_replace({"_id": contId}, newCont)
        return newCont["memused"], newCont["createTime"]
    return None, None

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
        minAgo = datetime.utcnow() - timedelta

        for cont in allCont.find():
            if minAgo > cont["createTime"]:
                cid = cont["_id"]
                allCont.delete_one({"_id": cid})
                availableCont.delete_one({"_id": cid})
                killContainer(cid)
                print "DELETING " + cid

        # clist = getContList()
        # for container in clist:
        #     cname = container.name
        #     if cname not in ("mongoDB", "coreGateway"):
        #         # DON'T TERMINATE mongo and core containers
        #         try:
        #             if not allCont.find_one({"_id": cname}):
        #                 print "DELETING " + cname
        #                 container.kill()
        #                 container.remove(v=True)
        #                 availableCont.delete_one({"_id": cname})
        #         except Exception:
        #             pass
        time.sleep(60)

def getAvUsedMem():
    tot = 0
    for cont in availableCont.find():
        tot += cont["memused"]

    return tot
