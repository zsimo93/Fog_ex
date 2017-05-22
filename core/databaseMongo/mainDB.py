from pymongo import MongoClient


class DatabaseMaster():
    c = MongoClient(host='localhost', port=27017)

    config = {'_id': 'foo', 'version': 1,
              'members': [
                  {'_id': 0, 'host': '172.17.0.2:27017', 'priority' : 1},
                  {'_id': 1, 'host': '172.17.0.3:27017', 'priority' : 0},
                  {'_id': 2, 'host': '172.17.0.4:27017', 'priority' : 0}]}

    c.admin.command("replSetInitiate", config)
    """def __init__(self):
                    self.db.create_collection("actions")
                    self.db.create_collection("actionsAV")"""

