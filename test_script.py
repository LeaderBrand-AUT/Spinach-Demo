import numpy as np
import camera
import scripts.classifier as classifier
import scripts.constants as constants

# TEMPORARY
import pathlib
import tensorflow as tf

def classify_frame(img_path):
    processed_frame = tf.keras.utils.load_img(img_path, target_size=(constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH))
    processed_frame = np.array(processed_frame)

    classifier.classifyFrame(processed_frame)

classify_frame('./input_data/fresh.jpg')
classify_frame('./input_data/not_fresh.jpg')
classify_frame('./input_data/not_very_fresh.jpg')
classify_frame('./input_data/very_fresh.jpg')



