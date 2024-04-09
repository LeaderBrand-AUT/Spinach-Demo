import numpy as np
import sys
sys.path.append("..")
from ..constants import *
from ..classifier import classifyFrame
import tensorflow as tf

def classify_frame(img_path):
    processed_frame = tf.keras.utils.load_img(img_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH))
    processed_frame = np.array(processed_frame)

    classifyFrame(processed_frame)

classify_frame('./input_data/fresh.jpg')
classify_frame('./input_data/not_fresh.jpg')
classify_frame('./input_data/not_very_fresh.jpg')
classify_frame('./input_data/very_fresh.jpg')



