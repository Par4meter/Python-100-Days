from PIL import Image, ImageFilter


def base_info():
    image = Image.open('../res/guido.jpg')
    print(image.format)
    print(image.size)
    print(image.mode)
    image.show()


def crop_image():
    image = Image.open('../res/guido.jpg')
    rect = (80, 20, 310, 360)
    image.crop(rect).show()


def thumbnail():
    image = Image.open('../res/guido.jpg')
    size = 128, 128
    image.thumbnail(size)
    image.show()


def paste():
    image1 = Image.open('../res/guido.jpg')
    image2 = Image.open('../res/luohao.png')
    rect = 80, 20, 310, 360
    guido_head = image1.crop(rect)
    width, height = guido_head.size
    image2.paste(guido_head.resize((int(width / 1.5), int(height / 1.5))), (172, 40))
    image2.show()


def reverse():
    image = Image.open('../res/guido.jpg')
    image.rotate(180).show()
    image.transpose(Image.FLIP_LEFT_RIGHT).show()


def pixels():
    image = Image.open('../res/guido.jpg')
    for i in range(80, 310):
        for y in range(20, 360):
            image.putpixel((i, y), (128, 128, 128))

    image.show()


def image_filter():
    image = Image.open('../res/guido.jpg')
    image.filter(ImageFilter.CONTOUR).show()


def main():
    # base_info()
    # crop_image()
    # thumbnail()
    # paste()
    # reverse()
    # pixels()
    image_filter()


if __name__ == '__main__':
    main()
