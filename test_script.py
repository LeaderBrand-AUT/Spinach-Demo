import camera
import classifier

frame = camera.get_frame()
processed_frame = camera.crop_frame(frame, 100, 500, 100, 500)

classifier.classifyFrame(processed_frame)