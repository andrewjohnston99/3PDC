import numpy as np
import cv2
import os
from datetime import date
# Open a sample video available in sample-videos
vcap = cv2.VideoCapture('rtsp://vss2live.dot.ga.gov:80/lo/gdot-cam-017.stream')
if not vcap.isOpened():
    print("File Cannot be Opened")

frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))
size = (frame_width, frame_height)

filename = date.today().strftime("%B %d, %Y") + ".avi"

video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

while(True):
    # Capture frame-by-frame
    ret, frame = vcap.read()
    #print cap.isOpened(), ret
    if frame is not None:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        video.write(frame)
        # Press q to close the video windows before it ends if you want
        if cv2.waitKey(22) & 0xFF == ord('q'):
            break
    else:
        print("is None")
        break

# When everything done, release the capture
vcap.release()
video.release()
cv2.destroyAllWindows()
print("Video stop")