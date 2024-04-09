import cv2
import numpy as np
import sys
import skimage

def white_balancing(frame):
    return skimage.img_as_ubyte((frame*1.0 / np.percentile(frame, 99.4, axis=(0, 1))).clip(0, 1))

