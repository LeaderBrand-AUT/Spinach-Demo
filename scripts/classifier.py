import datetime

import tensorflow as tf
import numpy as np

from . import constants
# set up to run every 30 seconds or so...

# Takes in a frame and returns a success/error message. Writes output to a file
def classifyFrame(frame: bytes) -> str:
    try: 
        # load model from file
        model = tf.keras.models.load_model("./models/" + constants.CURRENT_MODEL)

        # not sure if this is needed, convert input frame to array
        img_array = tf.keras.utils.img_to_array(frame)
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        # make predictions
        predictions = model.predict(img_array)

        class_names = ['Fresh', 'Not Fresh', 'Not Very Fresh', 'Very Fresh']
        score = tf.nn.softmax(predictions[0])

        currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        reportStr = "Report {}:\n\n This image most likely belongs to {} with a {:.2f} percent confidence.".format(currentDate, class_names[np.argmax(score)], 100 * np.max(score))

        # Write some output to file
        f = open("classifications/" + currentDate + "_classification.txt", "x")

        f.write(reportStr)
        f.close()

        return reportStr + "\n\n This report has been written to a txt file."
    except Exception as e:
        print('An error occured: ' + str(e))

        return "There was an error generating the report."
        
    