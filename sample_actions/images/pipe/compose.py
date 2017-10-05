from PIL import Image, ImageFile
import io

def main(args):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    data = args["image1"].decode("base64")
    image0 = Image.open(io.BytesIO(data))

    data = args["image2"].decode("base64")
    image1 = Image.open(io.BytesIO(data))

    data = args["image3"].decode("base64")
    image2 = Image.open(io.BytesIO(data))

    data = args["image4"].decode("base64")
    image3 = Image.open(io.BytesIO(data))

    base_width, base_height = image0.size
    new_image = Image.new('RGB', (2 * base_width, 2 * base_height))

    new_image.paste(image0, (0, 0))
    new_image.paste(image1, (base_width, 0))
    new_image.paste(image2, (0, base_height))
    new_image.paste(image3, (base_width, base_height))

    newImage = io.BytesIO()
    new_image.save(newImage, 'PNG')
    newImage.seek(0)
    dataout = newImage.read().encode("base64")
    return {"image": dataout}
