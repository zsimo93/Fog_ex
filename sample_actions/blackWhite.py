from PIL import Image, ImageFile
from bson.binary import Binary
import fileModule
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fm = fileModule.FileManager()
    data = fm.loadFile(args["id"])
    image = Image.open(io.BytesIO(data))
    
    image = image.convert('1')
    newImage = io.BytesIO()
    image.save(newImage, args["formatOut"])
    bin = Binary(newImage.getvalue())
    retId = fm.saveFile(bin, "image." + args["formatOut"])
    return { "retId" : retId } 

