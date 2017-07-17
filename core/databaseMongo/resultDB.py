#!thesis/DB

import mainDB

db = mainDB.db
r = db.results

"""def deleteResult(id):
    db = mainDB.db
    n = db.results

    n.delete_one({'_id': id})"""

def deleteAllRes(sessionID):
    r.delete_many({'_id': {'$regex': '^' + sessionID} })

def insertResult(sessionID, actionID, value):
    id = sessionID + "|" + actionID
    value['_id'] = id
    r.insert_one(value)

    return id


def getResult(sessionID, actionID):
    id = sessionID + "|" + actionID
    return r.find_one({'_id': id})


def getSubParam(sessionID, actID, paramName):
    res = r.find_one({'_id': sessionID + "|" + actID})

    return res[paramName]