import tensorflow as tf
import pathlib

from . import constants
from .constants import *

def evaluate_model():
    model = tf.keras.models.load_model("./models/" + constants.CURRENT_MODEL)

    data_dir = pathlib.Path('./spinach_training_processed/')
    data_dir = pathlib.Path(data_dir).with_suffix('')

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        batch_size=32
    )

    # Evaluate the model on the validation dataset
    val_loss, val_accuracy = model.evaluate(val_ds)
    print("Validation accuracy:", val_accuracy)
    print("Validation loss:", val_loss)

evaluate_model()