#!thesis/DB

from mainDB import Database
from core.databaseRedis.actionsDB import removeNodeAV
from core.common.entities import NodeID
import json


def deleteNode(token):
    db = Database().db

    db.delete("NODE_" + token)
    db.delete("NRES_" + token)

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

    id = dict.pop('id')
    # insert node info's
    key = "NODE_" + id
    value = json.dumps(dict)
    db.set(key, value)
    # prepare for node resources
    key = "NRES_" + id
    value = json.dumps({'cpu': '', 'memory': ''})
    db.set(key, value)


def getNodesIP():
    db = Database().db

    keys = db.keys("NODE_*")

    ips = list()

    for k in keys:
        r = db.get(k)
        obj = json.loads(r)
        ip = obj['ip']
        ips.append(NodeID(k[5:], ip))
    return ips


def getNode(token):
    db = Database().db

    return db.get("NODE_" + token)


def getRes(token):
    db = Database().db

    return db.get("NRES_" + token)


def getFullNode(token):
    node = json.loads(getNode(token))
    res = json.loads(getRes(token))
    node['cpu'] = res['cpu']
    node['memory'] = res['memory']
    node['id'] = token

    return node


def getNodes():
    db = Database().db

    keys = db.keys("NODE_*")

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

    key = "NRES_" + token
    db.set(key, json.dumps(value))


def updateNode(token, col, value):
    db = Database().db
    key = "NODE_" + token
    try:
        tmp = json.loads(db.get(key))
        tmp.pop(col)
        tmp[col] = value

        db.set(key, json.dumps(tmp))
        return tmp

    except Exception:
        return None
