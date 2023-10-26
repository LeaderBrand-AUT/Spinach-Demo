import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Sequential
import pathlib
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
#from keras.preprocessing.image import preprocess_input
from tensorflow.keras.applications.resnet50 import preprocess_input
#from keras.preprocessing.image import decode_predictions
from tensorflow.keras.applications.resnet50 import decode_predictions

#Function parameters
img_height = 180
img_width = 180
class_names = ['Fresh', 'Not Fresh', 'Not very Fresh', 'Very Fresh']
model_path = 'model/spinach_model'

def classifySpinach(filename):
    model = tf.keras.models.load_model(model_path)
    img_loc = 'spinach_test/' + filename
    img = tf.keras.preprocessing.image.load_img(img_loc, target_size=(img_height, img_width))
    
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch
    
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    
    ret = "This spinach leaf is {}, with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
    return ret
    

