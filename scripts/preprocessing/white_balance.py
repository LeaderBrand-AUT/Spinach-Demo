import cv2
import numpy as np
import skimage
import os
from skimage import img_as_ubyte
from ..constants import BRIGHTNESS_FACTOR

def white_balancing(frame, brightness_factor=BRIGHTNESS_FACTOR):
    # Normalize the frame based on the 99.4th percentile
    normalized_frame = frame * 1.0 / np.percentile(frame, 99.4, axis=(0, 1))
    
    # Clip the values to keep them within the range [0, 1]
    clipped_frame = normalized_frame.clip(0, 1)
    
    # Reduce the brightness by multiplying with a factor less than 1
    adjusted_frame = clipped_frame * brightness_factor
    
    # Convert the floating-point image to 8-bit unsigned byte format
    final_image = img_as_ubyte(adjusted_frame)
    
    return final_image
