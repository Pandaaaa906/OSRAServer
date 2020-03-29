from PIL import Image, ImageFilter


def binary_image_file(fp, threshold=230):
    img = Image.open(fp)
    img.load()
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])
    limg = background.convert('L')
    table = [x > threshold and 1 or 0 for x in range(256)]
    bimg = limg.point(table, '1')
    bimg.save(fp)
