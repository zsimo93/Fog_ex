import gridfs
from pymongo import MongoClient
from core.utils.fileutils import unzip
import os

fs = gridfs.GridFS(MongoClient(host='localhost', port=27017).fs)
print "importing FS client"

def saveFile(file, actionName):
    fs.put(file, _id=actionName, content_type=file.content_type,
           filename=file.filename)


def loadFile(actionName):
    f = fs.find_one(actionName)

    name = f.filename
    f.seek(0)
    data = f.read()

    path = "/tmp/" + actionName

    try:
        os.stat(path)
        return path
    
    except Exception:
        os.mkdir(path)

        pathfile = "/tmp/" + actionName + "/" + name
        # save the file in local fs
        file = open(pathfile, "w+")
        file.write(data)
        file.close()

        #if a zip, unzip it
        if name.endswith(".zip"):
            print ("unzip")
            unzip(pathfile, path)
        
        return "/tmp/" + actionName

def removeFile(actionName):
    fs.delete(actionName)
