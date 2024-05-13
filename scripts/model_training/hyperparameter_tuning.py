import keras_tuner as kt
import keras
from keras.callbacks import EarlyStopping
import tensorflow as tf
import pathlib
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import datetime

from ..constants import *

BATCH_SIZE = 32
DATA_DIR = pathlib.Path('./spinach_training_processed')

image_count = len(list(DATA_DIR.glob('*/*.jpg')))
print(f'{image_count} training images found.')


train_ds, val_ds = tf.keras.utils.image_dataset_from_directory(
  DATA_DIR,
  validation_split=0.2,
  subset="both",
  seed=123,
  image_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
  batch_size=BATCH_SIZE,
  shuffle=True)

class_names = train_ds.class_names
num_classes = len(class_names)

# configure keras to use GPU (NVIDIA with CUDA)
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  tf.config.experimental.set_memory_growth(gpus[0], True)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print(f'gpus available: {gpus}')

def model_builder(hp):

  num_classes = len(class_names)
  hp_dense = hp.Choice('dense units', values=[16,32,64,128,256])
  hp_conv1 = hp.Choice('conv1 units', values=[16,32,64,128,256])
  hp_conv2 = hp.Choice('conv2 units', values=[16,32,64,128,256])
  hp_conv3 = hp.Choice('conv3 units', values=[16,32,64,128,256])
  hp_dropout = hp.Choice('dropout', values=[0.0,0.5])
  model = Sequential([
  layers.Conv2D(hp_conv1, (3, 3), activation='relu', input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)),
  layers.MaxPooling2D((2, 2)),

  layers.Conv2D(hp_conv2, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),

  layers.Conv2D(hp_conv3, (3, 3), activation='relu'),
  layers.MaxPooling2D((2, 2)),

  layers.Flatten(),

  # Tune the number of units in the first Dense layer
  # Choose an optimal value between 32-512
  layers.Dense(hp_dense, activation='relu'),
  layers.Dropout(hp_dropout),
  layers.Dense(num_classes, activation='softmax')
  ])

  # Tune the learning rate for the optimizer
  # Choose an optimal value from 0.01, 0.001, or 0.0001
  hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])
  model.compile(optimizer=keras.optimizers.Adam(learning_rate=hp_learning_rate),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


  return model

model = model_builder(kt.HyperParameters())
model.summary()

tuner = kt.Hyperband(model_builder,
                     objective='val_accuracy',
                     max_epochs=10,
                     factor=3,
                     overwrite=True,
                     directory='hyperparameter_tuning',
                     project_name='leaderbrand')

stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

tuner.search(train_ds, validation_data=val_ds, epochs=20, callbacks=[stop_early])

# Get the optimal hyperparameters
best_hps=tuner.get_best_hyperparameters(num_trials=1)[0]

# Build the model with the optimal hyperparameters and train it on the data for 50 epochs
tuner_model = tuner.hypermodel.build(best_hps)
history = tuner_model.fit(train_ds,epochs=50,validation_data=val_ds,callbacks=[stop_early])

val_acc_per_epoch = history.history['val_accuracy']
best_epoch = val_acc_per_epoch.index(max(val_acc_per_epoch)) + 1
print('Best epoch: %d' % (best_epoch,))

hypermodel = tuner.hypermodel.build(best_hps)

# Retrain the model
history = hypermodel.fit(train_ds, validation_data=val_ds, epochs=best_epoch, validation_split=0.2)




# save model
currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
modelPath = "models/" + currentDate
hypermodel.save(modelPath + ".keras")
hypermodel.save(modelPath + '.h5')