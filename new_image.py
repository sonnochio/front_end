import numpy as np
from PIL import Image


def load_image(path):
    image = Image.open(path)
    return image

# 180,320,3

def resize(image):
    image = image.convert('RGB')
    width, height = image.size
    if width == 180 and height ==320:
        return image
    elif width/height == 180/230:
        return image.resize((180,320))
    else:
        rescale_height = height/180
        rescale_width = width/320
        heigth_resacled=height/rescale_height
        width_rescaled = width/rescale_width
        image_scaled = image.resize((int(width_rescaled),int(heigth_resacled)))
        return image_scaled


def convert_to_np(image):
    image_np = np.asarray(image)
    if image_np.shape[0] == 180:
        return image_np
    else:
        return 'Error with re-shaping'
    return image_np
