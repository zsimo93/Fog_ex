from PIL import Image, ImageFile
import fileModule
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fm = fileModule.FileManager()
    data = fm.loadFile(args["id"])
    image = Image.open(io.BytesIO(data.read()))

    image = image.rotate(180)
    newImage = io.BytesIO()
    image.save(newImage, args["formatOut"])
    newImage.seek(0)
    retId = fm.saveFile(newImage, "image." + args["formatOut"])
    return { "retId" : retId }
