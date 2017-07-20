import sys

def checkMaster():
    import os
    role = os.environ.get("TH_ROLE", "MASTER")
    return role == "MASTER"

def setup(ip):
    from pymongo import MongoClient
   
    config = {'_id': 'foo',
              'members': [
                  {'_id': 0, 'host': ip + ':27017'}]}
    c = MongoClient(host=ip, port=27017)
    c.admin.command("replSetInitiate", config)
    
def createNodeMaster(ip):
    from core.databaseMongo import nodesDB as db1, mainDB
    from core.utils.fileutils import uniqueName

    node = {
        'name': 'raspi1',
        'ip': ip,
        'role': 'MASTER',
        'architecture': 'ARM',
    }

    db = mainDB.db
    n = db.nodes
    nrs = db.nodesRes
    id = uniqueName()
    node['_id'] = id
    n.insert_one(node)

    info = {
        '_id': id,
        'cpu': '',
        'memory': ''}
    nrs.insert_one(info)

    res = {"cpu": 12,
           "memory": long(300000000)}
    db1.updateResources(id, res)

def execute():
    from core.APIGateway import run
    from core.heartbeat import heartbeatMain
    from core.gridFS.files import removeChunks
            
    # thread for cleaning up chunks table for user data
    # removed after TTL
    # threading.Thread(target=removeChunks).start()
    heartbeatMain.startHeartBeat()
    run(False)


if checkMaster():
    if len(sys.argv) == 1:
        sys.exit("run the script with the IP of the localnode")
    print sys.argv[1]
    setup(sys.argv[1])
    createNodeMaster(sys.argv[1])

execute()


