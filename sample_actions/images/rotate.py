from PIL import Image, ImageFile
import fileModule
import io, time

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fm = fileModule.FileManager()
    begin = time.time()
    data = fm.loadFile(args["id"])
    elapsed = time.time() - begin
    print ("read Time " + repr(elapsed))
    image = Image.open(io.BytesIO(data.read()))

    image = image.rotate(180)
    newImage = io.BytesIO()
    image.save(newImage, args["formatOut"])
    newImage.seek(0)
    begin = time.time()
    retId = fm.saveFile(newImage, "image." + args["formatOut"])
    elapsed = time.time() - begin
    print ("write Time " + repr(elapsed))
    return {"retId": retId}
