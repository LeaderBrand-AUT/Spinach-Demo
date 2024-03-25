import cv2

ip = '192.168.88.109'
port = '8080'

rtspLink = 'http://takemotopiano.aa1.netvolante.jp:8190/nphMotionJpeg?Resolution=640x480&Quality=Standard&Framerate=30'

camera = cv2.VideoCapture(rtspLink)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'---frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_frame():
    success, frame = camera.read()
    if not success:
        return
    else:
        return frame

def crop_frame(frame, y1, y2, x1, x2):
    # Constant, size of spinach leaf frames after processing.
    RESIZE_WIDTH = 1000
    RESIZE_HEIGHT = 1000

    cropped_frame = frame[y1:y2, x1:x2]
    resized_frame = cv2.resize(cropped_frame, (RESIZE_WIDTH, RESIZE_HEIGHT), interpolation=cv2.INTER_LINEAR)

    return resized_frame