import cv2
from ..constants import STREAM_FPS

def get_least_blurry(frames):
    fps = STREAM_FPS
    frame_count = len(frames)
    arr_frame=[]
    arr_lap=[]

    print('calculating least blurry frame...')

    for i in range(frame_count):
        frame = frames[i]
        laplacian = cv2.Laplacian(frame, cv2.CV_64F).var()
        arr_lap.append(laplacian)
        arr_frame.append(frame)
    
    selected_frame = arr_frame[arr_lap.index(max(arr_lap))]

    print(f"Selected frame num {arr_lap.index(max(arr_lap))}")

    return selected_frame


