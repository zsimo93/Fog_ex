from pymongo import MongoClient


class Database():
    db = MongoClient(host='localhost', port=27017).my_db

    """def __init__(self):
                    self.db.create_collection("actions")
                    self.db.create_collection("actionsAV")"""