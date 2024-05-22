import datetime
import tensorflow as tf
import numpy as np

from . import constants
from .database import db
from .report import Report

import cv2
# set up to run every 30 seconds or so...

#these didnt work for me - matei
# f = open("classifications/" + currentDate + "_classification.txt", "x")
# model = tf.keras.models.load_model("./models/" + constants.CURRENT_MODEL)
# f = open("classifications/" + currentDate + "_classification.txt", "x")


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

        class_names = ['Acceptable', 'Too Dry', 'Too Moist']
        score = tf.nn.softmax(predictions[0])

        currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        reportStr = "Report {}:\n\n This image most likely belongs to {} with a {:.2f} percent confidence.".format(currentDate, class_names[np.argmax(score)], 100 * np.max(score))

        # Write some output to file (DOES NOT WORK WITH ':' IN FILENAME (FROM currentDate) - Logan)
        # f = open("./classifications/" + currentDate + "_classification.txt", "x")

        # f.write(reportStr)
        # f.close()

        # # Development, save image along with report
        # cv2.imwrite("./classifications/images/" + currentDate + ".jpg", frame)

        # Add report to database
        new_report = Report(
            time=currentDate,
            accuracy=float(np.max(score)),
            moisture_level=class_names[np.argmax(score)]
        )
        db.session.add(new_report)
        db.session.commit()

        report = {
            "report_text": reportStr,
            "time": currentDate,
            "accuracy": float(np.max(score)),
            "moisture_level": class_names[np.argmax(score)]
        }

        print(report)

        return report
    
    except Exception as e:
        print('An error occured: ' + str(e))

        return "There was an error generating the report."