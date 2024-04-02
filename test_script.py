import numpy as np
import camera
import scripts.classifier as classifier
import scripts.preprocessing.constants as constants
import scripts.preprocessing.white_balance as white_balance
import cv2
import scripts.preprocessing.image_resize
    

images = [cv2.imread('3.jpg'), cv2.imread('6.jpg')]
balanced = []

for image in images:
    balanced.append(white_balance.white_balancing(image))

combined_images = np.concatenate(images, axis=0)
cv2.imshow('test', combined_images)
combined_balanced = np.concatenate(balanced, axis=0)
cv2.imshow('test 2', combined_balanced)

final_img = np.concatenate((combined_images, combined_balanced), axis=1)

cv2.imshow('image', final_img)
cv2.waitKey(0)




# TEMPORARY
# import pathlib
# import tensorflow as tf
# img_path = pathlib.Path('./spinach_training/test/1012.jpg')
# processed_frame = tf.keras.utils.load_img(img_path, target_size=(constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH))
# processed_frame = np.array(processed_frame)

# classifier.classifyFrame(processed_frame, constants.IMAGE_HEIGHT, constants.IMAGE_WIDTH)