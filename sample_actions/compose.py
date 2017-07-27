from PIL import Image, ImageFile
from bson.binary import Binary
import fileModule
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fm = fileModule.FileManager()
    image = []
    data = fm.loadFile(args["id1"])
    image[0] = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id2"])
    image[1] = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id3"])
    image[2] = Image.open(io.BytesIO(data))

    data = fm.loadFile(args["id4"])
    image[3] = Image.open(io.BytesIO(data))
    
    base_width = image[0].width
    base_height = image[0].height
    new_image = Image.new('RGB', (2 * base_width, 2 * base_height))

    new_image.paste(image[0], (0, 0))
    new_image.paste(image[1], (base_width, 0))
    new_image.paste(image[2], (0, base_height))
    new_image.paste(image[3], (base_width, base_height))

    newImage = io.BytesIO()
    new_image.save(newImage, 'PNG')
    bin = Binary(newImage.getvalue())
    retId = fm.saveFile(bin, "image." + 'PNG')
    return { "retId" : retId } 

