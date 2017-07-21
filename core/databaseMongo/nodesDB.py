#!thesis/DB

import mainDB

db = mainDB.db
n = db.nodes
nrs = db.nodesRes

def deleteNode(token):
    old_val = n.find_one({'_id': token})
    if old_val["role"] == "MASTER":
        return "Cannot remove master node"

    n.delete_one({'_id': token})
    mainDB.removeNodeReplicaSet(old_val)
    nrs.delete_one({'_id': token})
    return "DONE"

def insertNode(value):
    value = mainDB.insertNodeReplicaSet(value)
    name = value["name"]
    value['_id'] = name
    n.insert_one(value)

    info = {
        '_id': name,
        'cpu': -1,
        'memory': -1}
    nrs.insert_one(info)

    return name


def getNodesIP():
    class NodeID():
        def __init__(self, id, ip):
            self.id = id
            self.ip = ip

    ips = []
    for k in n.find():
        ips.append(NodeID(k['_id'], k['ip']))
    return ips

def getNode(token):
    return n.find_one({'_id': token})


def getRes(token):
    return nrs.find_one({'_id': token})

def allRes():
    return nrs.find()

def getFullNode(token):
    node = getNode(token)
    res = getRes(token)
    node['cpu'] = res['cpu']
    node['memory'] = res['memory']
    return node


def getNodesID():
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
    ins = value

    ins["_id"] = token
    nrs.find_one_and_replace({'_id': token}, ins)


def updateNode(token, col, value):
    try:
        tmp = n.find_one({'_id': token})
        tmp.pop(col)
        tmp[col] = value

        n.find_one_and_replace({'_id': token}, tmp)
        return tmp

    except Exception:
        return None
