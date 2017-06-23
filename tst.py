from core.databaseMongo import nodesDB, actionsDB

"""
nodes = [
    {
        "name": "r1",
        "ip": "127.0.0.1"
    },
    {
        "name": "r2",
        "ip": "127.0.0.1"
    },
    {
        "name": "r3",
        "ip": "127.0.0.1"
    }
]

resources = [
    {
        'cpu': 2.0,
        'memory': 1000000000L
    },
    {
        'cpu': 4.0,
        'memory': 1000000000L
    },
    {
        'cpu': 10.0,
        'memory': 1000000000L
    }
]

ids = []

for i in range(0, 3):
    id = nodesDB.insertNode(nodes[i])
    ids.append(id)
    nodesDB.updateResources(id, resources[i])

print ids"""

actionsDB.updateAvailability("addStr", "8DCBC489D0")
actionsDB.updateAvailability("addStr", "CD10945031")

actionsDB.updateAvailability("UpperDate", "CD10945031")
actionsDB.updateAvailability("UpperDate", "73465FFAD7")


