from pymongo import MongoClient

# , replicaset="foo"
c = MongoClient(host='localhost', port=27017, replicaset="foo")
db = c.my_db
print "connectiong to db"

def initDatabaseReplicaSet(config):
    """
    config = {'_id': 'foo', 'version': 1,
              'members': [
                  {'_id': 0, 'host': '172.17.0.2:27017', 'priority' : 1},
                  {'_id': 1, 'host': '172.17.0.3:27017', 'priority' : 0},
                  {'_id': 2, 'host': '172.17.0.4:27017', 'priority' : 0}]}
    """
    try:
        c.admin.command("replSetInitiate")  #, config)
    except Exception as e:
        print "PROBLEM HERE"
        raise e


def insertNodeReplicaSet(value):
    
    config = c.admin.command("replSetGetConfig")['config']
    members = sorted(config['members'], key=lambda m : m['_id'])
    
    priority = 1
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

    c.admin.command("replSetReconfig", config, force=True)

    return value


def removeNodeReplicaSet(value):

    config = c.admin.command("replSetGetConfig")['config']
    members = config['members']

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