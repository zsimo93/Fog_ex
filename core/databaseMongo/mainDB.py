from pymongo import MongoClient

c = MongoClient(host='localhost', port=27017, replicaset="foo")
db = c.my_db
print "connectiong to db"

def resetReplicaSet():
    cl = MongoClient(host='localhost', port=27017)
    config = cl.admin.command("replSetGetConfig")['config']
    statusMembers = cl.admin.command("replSetGetConfig")['members']
    configMembers = config["members"]

    deadMembers = []
    for m in statusMembers:
        if m["health"] < 1:
            deadMembers.append(m["_id"])
    configMembers = [m for m in configMembers if m["_id"] not in deadMembers]
    config["members"] = configMembers
    config["version"] += 1

    cl.admin.command("replSetReconfig", config, force=True)

    n = db.nodes
    nrs = db.nodesRes
    for m in deadMembers:
        old = n.find_one_and_delete({"replica_id": m})
        nrs.delete_one({"_id": old["_id"]})

def insertNodeReplicaSet(value):

    config = c.admin.command("replSetGetConfig")['config']
    members = sorted(config['members'], key=lambda m: m['_id'])

    config["version"] += 1

    priority = 0.5
    votes = 1

    id = freeID(members)

    if len(config['members']) >= 7:
        priority = 0
        votes = 0

    member = {
        "votes": votes,
        "priority": priority,
        "host": value['ip'] + ":27017",
        "_id": id
    }

    value['replica_id'] = id

    config['members'].append(member)

    c.admin.command("replSetReconfig", config)

    return value


def removeNodeReplicaSet(value):

    config = c.admin.command("replSetGetConfig")['config']
    members = config['members']

    config["version"] += 1

    id = value["replica_id"]

    new_members = []
    non_vonting = []
    voting = 0
    to_remove = None

    # remove old node from list and take all non voting members
    for f in members:
        if f["_id"] != id:
            new_members.append(f)
            if f['votes'] != 0:
                voting += 1
            else:
                non_vonting.append(f)
        else:
            to_remove = f

    # if old node was a voting one and there are non voting nodes, promote one.
    if to_remove['votes'] != 0 and len(non_vonting) > 0:
        newV = non_vonting[0]
        new_members.remove(newV)
        newV["priority"] = 1
        newV["votes"] = 1
        new_members.append(newV)
    config['members'] = new_members

    c.admin.command("replSetReconfig", config, force=True)


def freeID(l):
    if len(l) == 255:
        raise NoMoreNodes("Reached the maxium number of nodes")

    last = l[-1]["_id"]
    if last < 255:
        return last + 1

    id = 0
    # find free id
    for m in l:
        if m['_id'] > id:
            break
        else:
            id += 1
    return id

class NoMoreNodes(Exception):
    pass