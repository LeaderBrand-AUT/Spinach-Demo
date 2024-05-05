from .constants import CURRENT_MODEL
from keras_visualizer import visualizer
from keras.models import load_model
import datetime

model = load_model(f'./models/{CURRENT_MODEL}')

currentDate = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

visualizer(model, f'./models/visualizations/{currentDate}', 'png')