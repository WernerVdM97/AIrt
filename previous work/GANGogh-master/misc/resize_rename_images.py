"""
A script designed to:
1) resize all of the downloaded images to desired dimension (DEFAULT 64x64 pixels) and
2) rename images in folders from 1.png to n.png for ease of use in training
"""

import os
import random
# import PIL
# from PIL import Image
#import scipy.misc
#import imageio
from PIL import Image

from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings

original_images_dir = Path(settings.ORIGINAL_IMAGES_PATH)
resized_images_dir = Path(settings.RESIZED_IMAGES_PATH)


def resize_image(base_path, dest_path):
    # """
    # Source: https://opensource.com/life/15/2/resize-images-python
    # """
    TARGET_BASEWIDTH = 64

    image = Image.open(base_path)
    image = image.resize((TARGET_BASEWIDTH,TARGET_BASEWIDTH),Image.ANTIALIAS)
    image.save(fp=dest_path)
    # img = Image.open(base_path)

    # img = img.resize((TARGET_BASEWIDTH, TARGET_BASEWIDTH), PIL.Image.ANTIALIAS)
    # img.convert('RGB').save(dest_path, "PNG")


for subdir, dirs, files in os.walk(str(original_images_dir)):
    if subdir == original_images_dir.name:
        continue

    style = Path(subdir).name

    name = style
    # Remove parent directory from name
    name = name.replace(original_images_dir.name + "/", "")

    dest_dir = Path.joinpath(resized_images_dir, name)

    if len(style) < 1:
        continue

    dest_dir.mkdir(parents=True, exist_ok=True)

    style = Path(style)
    i = 0
    for f in files:
        source = Path.joinpath(original_images_dir, style, f)
        try:
            dest_path = Path.joinpath(dest_dir, str(i) + ".png")
            resize_image(source, dest_path)
            i += 1
        except Exception as e:
            print(e)
            print("missed it: " + str(source))

#resize_image('C:/Users/wvdm2/Documents/GitHub/AIrt/GANGogh-master/archive/images',
#             'C:/Users/wvdm2/Documents/GitHub/AIrt/GANGogh-master/archive/resized_images')