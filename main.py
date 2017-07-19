from core.APIGateway import run
from core.databaseMongo import nodesDB as db1
from core.gridFS.files import removeChunks
import threading
from core.heartbeat import heartbeatMain

def setup():
    
    node = {
        'name': 'raspi1',
        'ip': '127.0.0.1',
        'role': 'MASTER',
        'architecture': 'ARM',
    }
    db1.insertNode(node)


# setup()

# thread for cleaning up chunks table for user data
# removed after TTL
# threading.Thread(target=removeChunks).start()

# heartbeatMain.startHeartBeat()

run()


