
import functools
from PIL import Image


def image_transpose_exif(im, exif):
    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        #  0    (reserved)
        [],                                        #  1   top      left
        [Image.FLIP_LEFT_RIGHT],                   #  2   top      right
        [Image.ROTATE_180],                        #  3   bottom   right
        [Image.FLIP_TOP_BOTTOM],                   #  4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  #  5   left     top
        [Image.ROTATE_270],                        #  6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  #  7   right    bottom
        [Image.ROTATE_90],                         #  8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[exif[exif_orientation_tag]]
    except Exception as e:
        return im
    else:
        return functools.reduce(type(im).transpose, seq, im)

def resize_image(path, width, output=None):
    with Image.open(path) as img:
        if img.size[0] > width :
            wpercent = (width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            exif = img._getexif()
            img = img.resize((width, hsize))
        img = image_transpose_exif(img, exif)
        img.save(output if output != None else path)
