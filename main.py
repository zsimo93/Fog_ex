from core.APIGateway import run
from core.databaseMongo import nodesDB as db1

def setup():
    ids = []
    for i in range(10, 13):
        node = {
            'name': 'raspi' + str(i),
            'ip': '127.0.0.1',
            'role': 'NODE',
            'architecture': 'ARM',
        }
        ids.append(db1.insertNode(node))


    cpu = 10
    memory = 1000000

    for i in range(0, 3):
        res = {}
        res["cpu"] = cpu * (i + 1)
        res["memory"] = memory * (i + 1)
        db1.updateResources(ids[i], res)

# setup()
run()


