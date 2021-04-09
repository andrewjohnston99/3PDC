import numpy as np
import cv2
import os
import requests
from datetime import date
from datetime import time
from datetime import datetime


def recordCamera(directory, streamLink, imageLink):
    # Open a sample video available in sample-videos
    stream = streamLink
    url = imageLink
    camera = stream[stream.rfind("/"):stream.rfind(".")].replace('/', '')
    # print(stream.rfind("/"))
    # print(stream.rfind("."))
    # print(camera)
    vcap = cv2.VideoCapture(stream)
    tripNum = 2

    print(str(datetime.now()))

    path = directory
    print ("The current working directory is %s" % path)
    firstpath = path

    try:
        os.mkdir(firstpath)
    except OSError:
        print ("Creation of the directory %s failed" % firstpath)
    else:
        print ("Successfully created the directory %s " % firstpath)

    finalpath = firstpath + "\TestDirectory-" + camera + "-" + date.today().strftime("%B %d, %Y")

    filename = finalpath + chr(92) + datetime.now().strftime("%Y%m%d-%H%M%S") + ".avi"
    print(filename)

    try:
        os.mkdir(finalpath)
    except OSError:
        print ("Creation of the directory %s failed" % finalpath)
    else:
        print ("Successfully created the directory %s " % finalpath)

    if not vcap.isOpened():
        print("File Cannot be Opened")
        r = requests.get(url)
        filenamePicture = finalpath + chr(92) + datetime.now().strftime("%Y%m%d-%H%M%S") + r".jpg"
        print(filenamePicture)
        with open(filenamePicture, "wb") as f:
            f.write(r.content)
    else:
        frame_width = int(vcap.get(3))
        frame_height = int(vcap.get(4))
        size = (frame_width, frame_height)

        video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

        # try:
        #     os.mkdir(finalpath)
        # except OSError:
        #     print ("Creation of the directory %s failed" % finalpath)
        # else:
        #     print ("Successfully created the directory %s " % finalpath)

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