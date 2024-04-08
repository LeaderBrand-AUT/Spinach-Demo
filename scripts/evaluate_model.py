import tensorflow as tf
from . import constants

def evaluate_model():
    model = tf.keras.models.load_model("./models/" + constants.CURRENT_MODEL)

    model.get_metrics_result()
