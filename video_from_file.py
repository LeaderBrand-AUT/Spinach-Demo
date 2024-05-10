import cv2
from scripts.constants import *

video = cv2.VideoCapture('input_data/acceptable.mp4')

def gen_frames():
    while True:
        success, frame = video.read()
        if not success:
            # If video file reached end, reset to 0
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'---frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_frame():
    success, frame = video.read()
    if not success:
        return
    else:
        return frame