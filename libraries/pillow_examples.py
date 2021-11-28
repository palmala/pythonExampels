from PIL import Image

with Image.open("rh.jpg") as image:

    print(image.filename, image.format)
    print(image.height, image.width)
    print(image.mode)
    for k, v in image.info.items():
        print(k, v)

    # converting image
    # image.save("rh.gif", "GIF")

    # default image viewer
    # image.show()

    midx = image.width / 2
    midy = image.height / 2
    croparea = (midy - 200, midx - 200, midy + 200, midx + 200)
    cropimage = image.crop(croparea)
    newimage = cropimage.resize((256, 256))
    newimage = newimage.rotate(45)
    newimage.show()