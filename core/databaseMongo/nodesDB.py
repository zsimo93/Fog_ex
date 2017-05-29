#!thesis/DB

from core.databaseMongo.actionsDB import removeNodeAV
from bson.objectid import ObjectId


class NodeID():
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip


def deleteNode(token):
    db = mainDB.db
    n = db.nodes
    nrs = db.nodesRes

    old_val = n.delete_one({'_id': ObjectId(token)})
    
    mainDB.removeNodeReplicaSet(old_val)

    nrs.delete_one({'_id': ObjectId(token)})
    removeNodeAV(token)


"""
value = {
    'id': 'AAABBBCCCDE',
    'name': 'raspi2',
    'ip': '172.17.0.6',
    'role': 'NODE',
    'architecture': 'ARM',
}
"""
def insertNode(value):
    db = mainDB.db
    n = db.nodes
    nrs = db.nodesRes

    value = mainDB.insertNodeReplicaSet(value)

    id = n.insert_one(value).inserted_id

    info = {
        '_id': id,
        'cpu': '',
        'memory': ''}
    nrs.insert_one(info)

    return str(id)


def getNodesIP():
    db = mainDB.db
    n = db.nodes

    ips = []

    for k in n.find():
        ips.append(NodeID(k['_id'], k['ip']))
    return ips


def getNode(token):
    db = mainDB.db
    n = db.nodes

    return n.find_one({'_id': ObjectId(token)})


def getRes(token):
    db = mainDB.db
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
    db = mainDB.db
    n = db.nodes

    keys = map(lambda x: str(x["_id"]), n.find())

    nodes = []

    for k in keys:
        r = getFullNode(k[5:])
        nodes.append(r)

    return nodes

    

def updateResources(token, value):
    """
    token = Node's id
    value = {'cpu': 13.7,
         'memory': 14507.30}
    """
    db = mainDB.db
    nrs = db.nodesRes
    id = ObjectId(token)
    ins = value

    ins["_id"] = id
    nrs.find_one_and_replace({'_id': id}, ins)


def updateNode(token, col, value):
    db = mainDB.db
    n = db.nodes

    try:
        tmp = n.find_one({'_id': ObjectId(token)})
        tmp.pop(col)
        tmp[col] = value

        n.find_one_and_replace({'_id': ObjectId(token)}, tmp)
        return tmp

    except Exception:
        return None
