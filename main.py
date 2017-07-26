import sys, os
import threading

def checkMaster():
    role = os.environ.get("TH_ROLE")
    return role == "MASTER"

def setup(ip):
    from pymongo import MongoClient
   
    config = {'_id': 'foo',
              'members': [
                  {'_id': 0, 'host': ip + ':27017',
                   "votes": 1, "priority": 1}]}
    c = MongoClient(host=ip, port=27017)
    c.admin.command("replSetInitiate", config)
    
def createNodeMaster(ip):
    from core.databaseMongo import nodesDB as db1, mainDB

    node = {
        '_id': 'raspi1',
        'name': 'raspi1',
        'ip': ip,
        'role': 'MASTER',
        'architecture': 'ARM',
        'replica_id': 0
    }

    db = mainDB.db
    n = db.nodes
    nrs = db.nodesRes
    n.insert_one(node)

    info = {
        '_id': 'raspi1',
        'cpu': '',
        'memory': ''}
    nrs.insert_one(info)

    res = {"cpu": 12,
           "memory": long(300000000)}
    db1.updateResources('raspi1', res)

def execute():
    from core.APIGateway import run
    from core.heartbeat import heartbeatMain
    from core.databaseMongo.localDB import removeTimedOutCont
    
    threading.Thread(target=removeTimedOutCont).start()
    heartbeatMain.startHeartBeat()
    run(False)


if checkMaster():
    if len(sys.argv) == 1:
        sys.exit("run the script with the IP of the localnode")
    ip = sys.argv[1]
    os.environ["TH_MASTERIP"] = ip
    setup(ip)
    createNodeMaster(ip)
    from core.gridFS.files import removeChunks
            
    # thread for cleaning up chunks table for user data
    # removed after TTL
    threading.Thread(target=removeChunks).start()

execute()