from PIL import Image, ImageFile
from bson.binary import Binary
import fileModule
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fm = fileModule.FileManager()
    data = fm.loadFile(args["id1"])
    image0 = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id2"])
    image1 = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id3"])
    image2 = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id4"])
    image3 = Image.open(io.BytesIO(data))
    
    base_width = image0.width
    base_height = image0.height
    new_image = Image.new('RGB', (2 * base_width, 2 * base_height))

    new_image.paste(image0, (0, 0))
    new_image.paste(image1, (base_width, 0))
    new_image.paste(image2, (0, base_height))
    new_image.paste(image3, (base_width, base_height))

    newImage = io.BytesIO()
    new_image.save(newImage, 'PNG')
    bin = Binary(newImage.getvalue())
    retId = fm.saveFile(bin, "image." + 'PNG')
    return { "retId" : retId } 

