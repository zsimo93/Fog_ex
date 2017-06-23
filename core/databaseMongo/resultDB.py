#!thesis/DB

from core.utils.fileutils import uniqueName
import mainDB

def deleteResult(id):
    db = mainDB.db
    n = db.results

    n.delete_one({'_id': id})


def insertResult(value):
    db = mainDB.db
    r = db.results
    id = uniqueName()
    value['_id'] = id
    r.insert_one(value)

    return id


def getResult(id):
    db = mainDB.db
    n = db.results

    return n.find_one({'_id': id})
