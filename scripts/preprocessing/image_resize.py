import cv2
from .. import constants

# Constant, size of spinach leaf frames after processing.
RESIZE_WIDTH = 1000
RESIZE_HEIGHT = 1000

def crop_frame(frame, y1, y2, x1, x2):
    cropped_frame = frame[y1:y2, x1:x2]
    resized_frame = cv2.resize(cropped_frame, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_LINEAR)

    return resized_frame

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_LINEAR)