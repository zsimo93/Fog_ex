from core.API import mainAPI
from core.databaseRedis import mainDB


mainAPI.run()


function = {
    "type": "function",
    "name": "foo1",
    "cloud": True,
    "timeout": 500,
    "language": "python"
}

response = {'cpu': 13.7,
            'memory': 14507.30}

"""

for i in range(10, 20):
    id = str(uuid.uuid1())
    node = {
        'id': id,
        'name': 'raspi2',
        'ip': '192.168.1.' + str(i),
        'role': 'NODE',
        'architecture': 'ARM',
        'mqtt_Topic': 'node/raspi2',
        'cpu': 10.0,
        'memory': 1222.00
    }
    db1.insertNode(node)

for ip in db1.getNodesIP():
    print ip.ip

hb.sendAll()


print mainDB.Database().db.keys()
"""
"""
print db1.getRes(id)

db1.updateResources(id, response)

print db1.getRes(id)

print db1.updateNode(id, 'ip', '192.168.1.11')
print db1.getNode(id)

db1.deleteNode(id)
"""