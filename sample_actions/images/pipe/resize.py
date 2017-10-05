from PIL import Image, ImageFile
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    data = args["image"].decode("base64")
    image = Image.open(io.BytesIO(data))

    image.thumbnail((200, 200), Image.ANTIALIAS)
    newImage = io.BytesIO()
    image.save(newImage, args["formatOut"])
    newImage.seek(0)
    dataout = newImage.read().encode("base64")
    return {"image": dataout}
