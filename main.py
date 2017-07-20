from core.APIGateway import run
from core.databaseMongo import nodesDB as db1, mainDB
from core.gridFS.files import removeChunks
import threading, os
from core.heartbeat import heartbeatMain

def setup():
    role = os.environ.get("TH_ROLE", "MASTER")
    if role != "MASTER":
        return
    
    node = {
        'name': 'raspi1',
        'ip': '192.168.1.50',
        'role': 'MASTER',
        'architecture': 'ARM',
    }
    id = db1.insertNode(node)

    config = {'_id': 'foo', 'version': 1,
              'members': [
                  {'_id': 0, 'host': '192.168.1.50:27017', 'priority' : 1}]}
    mainDB.initDatabaseReplicaSet(config)

    res = {"cpu": 12,
           "memory": long(300000000)}
    db1.updateResources(id, res)


setup()

# thread for cleaning up chunks table for user data
# removed after TTL
# threading.Thread(target=removeChunks).start()

heartbeatMain.startHeartBeat()

run()


