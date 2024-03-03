import cv2

ip = '192.168.88.109'
port = '8080'

rtspLink = 'rtsp://' + ip + ':' + port + '/h264_ulaw.sdp'

camera = cv2.VideoCapture(rtspLink)
print(rtspLink)

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'---frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')