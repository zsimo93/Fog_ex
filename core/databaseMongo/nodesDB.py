#!thesis/DB

from mainDB import Database
from core.databaseMongo.actionsDB import removeNodeAV
from core.common.entities import NodeID
from bson.objectid import ObjectId


def deleteNode(token):
    db = Database().db
    n = db.nodes
    nrs = db.nodesRes

    n.remove({'_id': ObjectId(token)})
    nrs.remove({'_id': ObjectId(token)})
    removeNodeAV(token)


"""
dict = {
    'id': 'AAABBBCCCDE',
    'name': 'raspi2',
    'ip': '192.168.1.10',
    'role': 'NODE',
    'architecture': 'ARM',
    'mqtt_Topic': 'node/raspi2',
}
"""
def insertNode(dict):
    db = Database().db
    n = db.nodes
    nrs = db.nodesRes

    id = n.insert_one(dict).inserted_id

    info = {
        '_id': id,
        'cpu': '',
        'memory': ''}
    nrs.insert_one(info)

    return str(id)


def getNodesIP():
    db = Database().db
    n = db.nodes

    ips = []

    for k in n.find():
        ips.append(NodeID(k['_id'], k['ip']))
    return ips


def getNode(token):
    db = Database().db
    n = db.nodes

    return n.find_one({'_id': ObjectId(token)})


def getRes(token):
    db = Database().db
    nrs = db.nodesRes

    return nrs.find_one({'_id': ObjectId(token)})


def getFullNode(token):
    node = getNode(token)
    del node['_id']
    res = getRes(token)
    node['cpu'] = res['cpu']
    node['memory'] = res['memory']
    node['id'] = token

    return node


def getNodes():
    db = Database().db
    n = db.nodes

    keys = map(lambda x: str(x["_id"]), n.find())

    nodes = []

    for k in keys:
        r = getFullNode(k[5:])
        nodes.append(r)

    return nodes

    
"""
value = {'cpu': 13.7,
         'memory': 14507.30}
"""
def updateResources(token, value):
    db = Database().db
    nrs = db.nodesRes
    id = ObjectId(token)
    ins = value

    ins["_id"] = id
    nrs.find_one_and_replace({'_id': id}, ins)


def updateNode(token, col, value):
    db = Database().db
    n = db.nodes

    try:
        tmp = n.find_one({'_id': ObjectId(token)})
        tmp.pop(col)
        tmp[col] = value

        n.find_one_and_replace({'_id': ObjectId(token)}, tmp)
        return tmp

    except Exception:
        return None
