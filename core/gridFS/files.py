import gridfs
from core.utils.fileutils import unzip
from core.databaseMongo.mainDB import c as mongoclient
import os, uuid
from datetime import datetime

mongodb = mongoclient.my_db
fs = gridfs.GridFS(mongodb)

userdata = mongodb.userdata

try:
    userdata.files.create_index("uploadDate", expireAfterSeconds=1000)
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

def loadUserData(token):
    f = fsUserData.find_one(str(token))
    if f:
        return f
    else:
        return None

def removeChunks():
    import time

    while True:
        try:
            chunksCollection = userdata.chunks
            chunks = chunksCollection.find()
            
            for c in chunks:
                chunkid = c["_id"]
                fileid = c["files_id"]
                if not userdata.find_one({"_id": fileid}):
                    userdata.chunks.find_one_and_delete({"_id": chunkid})
        except Exception:
            time.sleep(5)
            continue

        time.sleep(120)
