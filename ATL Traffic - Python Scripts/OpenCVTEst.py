import numpy as np
import cv2
import os
from datetime import date
from datetime import time
from datetime import datetime

# Open a sample video available in sample-videos
stream = 'rtsp://vss15od.dot.ga.gov:80/cl/atl-cam-955.stream'
camera = stream[len(stream) - 19:len(stream) - 7].replace('/', '')
print(camera)
vcap = cv2.VideoCapture(stream)

print(str(datetime.now()))

if not vcap.isOpened():
    print("File Cannot be Opened")

frame_width = int(vcap.get(3))
frame_height = int(vcap.get(4))
size = (frame_width, frame_height)

path = os.getcwd()
print ("The current working directory is %s" % path)
finalpath = path + "\TestDirectory-" + camera + "-" + date.today().strftime("%B %d, %Y")

filename = finalpath + chr(92) + datetime.now().strftime("%Y%m%d-%H%M%S") + ".avi"
print(filename)

video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, size)


try:
    os.mkdir(finalpath)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

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