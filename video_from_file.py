import cv2
import numpy as np
from collections import deque
from scripts.constants import STREAM_FPS

video = cv2.VideoCapture('./input_data/acceptable.mp4', cv2.CAP_FFMPEG)

seconds_to_capture = 3 # for calculating least blurry frame
buffer_size = STREAM_FPS * seconds_to_capture

# store the last x seconds of frames
frame_buffer = deque(maxlen=buffer_size)

def gen_frames():
    while True:
        success, frame = video.read()
        if not success:
            # If video file reached end, reset to 0
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            print('something not right, or reached end')
            continue
        else:
            # add frame to buffer
            frame_buffer.append(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame")
                continue
            frame = buffer.tobytes()
            
            yield (b'---frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_frame():
    success, frame = video.read()
    if not success:
        return
    else:
        return frame
    
def get_clip():
    clip = list(frame_buffer)
    clip_array = np.array(clip)

    return clip_array

