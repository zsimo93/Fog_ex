#!thesis/DB

import mainDB

def deleteResult(id):
    db = mainDB.db
    n = db.results

    n.delete_one({'_id': id})

def deleteAllRes(sessionID):
    db = mainDB.db
    n = db.results

    n.delete_many({'_id': {'$regex': '^' + sessionID} })

def insertResult(id, value):
    db = mainDB.db
    r = db.results
    value['_id'] = id
    r.insert_one(value)

    return id


def getResult(id):
    db = mainDB.db
    n = db.results

    return n.find_one({'_id': id})


def getSubParam(sessionID, actID, paramName):
    db = mainDB.db
    n = db.results

    res = n.find_one({'_id': sessionID + "|" + actID})

    return res[paramName]