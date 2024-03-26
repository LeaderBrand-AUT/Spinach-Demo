import camera
import classifier
import constants

frame = camera.get_frame()
processed_frame = camera.crop_frame(frame, 100, 500, 100, 500)

# TEMPORARY
import pathlib
import tensorflow as tf
img_path = pathlib.Path('./spinach_training/test/1012.jpg')
processed_frame = tf.keras.utils.load_img(img_path, target_size=(constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH))

classifier.classifyFrame(processed_frame, constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH)