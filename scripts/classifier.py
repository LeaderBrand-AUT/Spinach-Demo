import datetime
import pathlib
import os

import tensorflow as tf
import numpy as np

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from . import constants
# set up to run every 30 seconds or so...

# global variables
batch_size = 32

# Takes in a frame and returns a success/error message. Writes output to a file
def classifyFrame(frame: bytes) -> str:
    # load model from file
    model = tf.keras.models.load_model("./models/" + constants.CURRENT_MODEL)

    # not sure if this is needed, convert input frame to array
    img_array = tf.keras.utils.img_to_array(frame)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    # make predictions
    predictions = model.predict(img_array)

    class_names = ['Fresh', 'Not Fresh', 'Not Very Fresh', 'Very Fresh']
    # class_names = predictions.argmax(axis=-1)
    score = tf.nn.softmax(predictions[0])

    # print("class_names: " + str(class_names))

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

    # Write some output to file
    try:
        currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        # f = open("classifications/" + currentDate + "_classification.txt", "x")

        # f.write('some output...')
        # f.close()
    except Exception as e:
        print('An error occured: ' + str(e))
        
    