from core.utils.fileutils import uniqueName
import mainDB

db = mainDB.db
t = db.tokens

def newToken(actionName):
    token = uniqueName(15)

    t.insert_one({"_id": token, "action": actionName})
    return token

def checkToken(actionName, token):
    ret = t.find({"action": actionName})
    if not ret:
        return False
    for keys in ret:
        print keys["_id"]
        if keys["_id"] == token:
            return True
    return False

def deleteToken(actionName):
    t.delete_many({"action": actionName})