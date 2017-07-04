#!thesis/DB

from core.utils.fileutils import uniqueName
import mainDB

db = mainDB.db

class NodeID():
    def __init__(self, id, ip):
        self.id = id
        self.ip = ip


def deleteNode(token):
    n = db.nodes
    nrs = db.nodesRes

    old_val = n.delete_one({'_id': token})
    
    # mainDB.removeNodeReplicaSet(old_val)

    nrs.delete_one({'_id': token})
    # removeNodeAV(token)


def insertNode(value):
    """
    value = {
        'name': 'raspi2',
        'ip': '172.17.0.6',
        'role': 'NODE',
        'architecture': 'ARM',
    }
    """
    n = db.nodes
    nrs = db.nodesRes

    # value = mainDB.insertNodeReplicaSet(value)

    id = uniqueName()
    value['_id'] = id
    n.insert_one(value)

    info = {
        '_id': id,
        'cpu': '',
        'memory': ''}
    nrs.insert_one(info)

    return id


def getNodesIP():
    n = db.nodes

    ips = []

    for k in n.find():
        ips.append(NodeID(k['_id'], k['ip']))
    return ips


def getNode(token):
    n = db.nodes
    return n.find_one({'_id': token})


def getRes(token):
    nrs = db.nodesRes
    return nrs.find_one({'_id': token})

def allRes():
    nrs = db.nodesRes
    return nrs.find()

def getFullNode(token):
    node = getNode(token)
    res = getRes(token)
    node['cpu'] = res['cpu']
    node['memory'] = res['memory']
    return node


def getNodesID():
    n = db.nodes

    results = n.find()
    if results:
        keys = [str(x["_id"]) for x in results]
    else:
        keys = []

    return keys


def getNodes():
    keys = getNodesID()

    nodes = []

    for k in keys:
        r = getFullNode(k)
        nodes.append(r)

    return nodes


def updateResources(token, value):
    """
    token = Node's id
    value = {'cpu': 13.7,
         'memory': 14507.30}
    """
    nrs = db.nodesRes
    ins = value

    ins["_id"] = token
    nrs.find_one_and_replace({'_id': token}, ins)


def updateNode(token, col, value):
    n = db.nodes

    try:
        tmp = n.find_one({'_id': token})
        tmp.pop(col)
        tmp[col] = value

        n.find_one_and_replace({'_id': token}, tmp)
        return tmp

    except Exception:
        return None
