import gridfs
from pymongo import MongoClient
from core.utils.fileutils import unzip
import os, uuid
from datetime import datetime

mongoclient = MongoClient(host='localhost', port=27017)
mongodb = mongoclient.my_db
fs = gridfs.GridFS(mongodb)

userdata = mongodb.userdata

try:
    userdata.files.create_index("uploadDate", expireAfterSeconds=300)
except Exception:
    pass

fsUserData = gridfs.GridFS(mongodb, collection="userdata")
print "importing FS client"

def saveActionFile(file, actionName):
    fs.put(file, _id=str(actionName), content_type=file.content_type,
           filename=file.filename)

def loadActionFile(actionName):
    
    path = "/tmp/" + actionName
    try:
        os.stat(path)
    except Exception:
        os.mkdir(path)
        f = fs.find_one(str(actionName))

        name = f.filename
        f.seek(0)
        data = f.read()

        pathfile = path + "/" + name
        # save the file in local fs
        file = open(pathfile, "w+")
        file.write(data)
        file.close()

        # if a zip, unzip it
        if name.endswith(".zip"):
            unzip(pathfile, path)
            os.remove(pathfile)
            
    return path

def removeActionFile(actionName):
    fs.delete(actionName)

def saveUserData(file):
    id = str(uuid.uuid4())
    fsUserData.put(file, _id=id, content_type=file.content_type,
                   filename=file.filename, uploadDate=datetime.utcnow())

    return id

def deleteUserData(token):
    fsUserData.delete(token)

def removeChunks():
    import time

    while True:
        chunksCollection = userdata.chunks
        chunks = chunksCollection.find()
        
        for c in chunks:
            chunkid = c["_id"]
            fileid = c["files_id"]
            if not userdata.find_one({"_id": fileid}):
                userdata.chunks.find_one_and_delete({"_id": chunkid})
        time.sleep(120)
