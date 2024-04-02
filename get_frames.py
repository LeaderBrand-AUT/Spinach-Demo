import cv2

def get_least_blurry(video, filename):
    fps = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(int(frame_count/fps)):
        arr_frame=[]
        arr_lap=[]
        for j in range(fps):
            success, frame = video.read()
            laplacian = cv2.Laplacian(frame, cv2.CV_64F).var()
            arr_lap.append(laplacian)
            arr_frame.append(frame)
    
    selected_frame = arr_frame[arr_lap.index(max(arr_lap))]

    cv2.imwrite(filename, selected_frame)
    return selected_frame

# get_least_blurry(cv2.VideoCapture('videos/Acceptable/1.2_.MOV'), '1.jpg')


