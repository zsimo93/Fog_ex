import uuid
from gridfs import GridFS
from pymongo import MongoClient
from datetime import datetime

class FileManager:

    mongoclient = MongoClient(host='172.17.0.1', port=27017)
    mongodb = mongoclient.my_db
    coll = mongodb.userdata
    fs = GridFS(mongodb, collection="userdata")

    def saveFile(self, file, filename):
        id = str(uuid.uuid4())
        self.fs.put(file, _id=id, filename=filename,
                    uploadDate=datetime.utcnow())
        return id

    def loadFile(self, fileID):
        f = self.fs.find_one(str(fileID))
        if f:
            return f.read()
        else:
            return None