import gridfs
from pymongo import MongoClient
# import io


fs = gridfs.GridFS(MongoClient(host='localhost', port=27017).fs)

def saveFile(file, actionName):
    fs.put(file, _id=actionName, content_type=file.content_type,
           filename=file.filename)


"return the byte string"
def loadFile(actionName):
    f = fs.find_one(actionName)

    name = f.filename
    f.seek(0)
    data = f.read()
    type = f.content_type

    path = "/tmp/" + name
    file = open(path, "w+")
    file.write(data)
    file.close()

    return (path, type)

def removeFile(actionName):
    fs.delete(actionName)


"""file = io.open("/media/sf_Simone/workspace_thesis/downloads/file.zip", 'r')

print file

saveFile("aaaaa", "file.zip", file)

file.close()

openZip()"""