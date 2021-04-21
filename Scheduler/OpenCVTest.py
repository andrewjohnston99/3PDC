import numpy as np
import cv2
import os
import requests
from datetime import date
from datetime import time
from datetime import timedelta
from datetime import datetime

#Raspberry Pi version of the recording script
def recordCamera(directory, streamLink, imageLink, duration, eventNumber):
    
    stream = streamLink
    url = imageLink

    #Extract the camera's name from the video link
    camera = stream[stream.rfind("/"):stream.rfind(".")].replace('/', '')
    # print(stream.rfind("/"))
    # print(stream.rfind("."))
    # print(camera)

    #Establish a connection with the stream link
    vcap = cv2.VideoCapture(stream)


    print(str(datetime.now()))

    path = directory
    print ("The current working directory is %s" % path)

    #Folder for today's date
    firstpath = path + "/" + date.today().strftime("%B %d, %Y")
    try:
        os.mkdir(firstpath)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    #Folder for the event number
    midpath = firstpath + r"/Event-" + str(eventNumber)
    try:
        os.mkdir(midpath)
    except OSError:
        print ("Creation of the directory %s failed" % midpath)
    else:
        print ("Successfully created the directory %s " % midpath)

    #Folder for the Camera's name
    finalpath = midpath + "/" + camera
    #Name the video with a timestamp
    filename = finalpath + "/" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".avi"
    print(filename)

    try:
        os.mkdir(finalpath)
    except OSError:
        print ("Creation of the directory %s failed" % finalpath)
    else:
        print ("Successfully created the directory %s " % finalpath)

    #If the establishment of a connection to the video stream failed, retrieve the picture instead
    if not vcap.isOpened():
        print("Vide File Cannot be Opened")
        r = requests.get(url)
        #Timestamp the practure and save it
        filenamePicture = finalpath + "/" + datetime.now().strftime("%Y%m%d-%H%M%S") + r".jpg"
        print(filenamePicture)
        with open(filenamePicture, "wb") as f:
            f.write(r.content)
    else:
        #Otherwise, begin recording the video
        frame_width = int(vcap.get(3))
        frame_height = int(vcap.get(4))
        size = (frame_width, frame_height)

        #Save frames in a videowriter data structure
        video = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), 10, size)

        # try:
        #     os.mkdir(finalpath)
        # except OSError:
        #     print ("Creation of the directory %s failed" % finalpath)
        # else:
        #     print ("Successfully created the directory %s " % finalpath)

        #Record the video for the specified amount of time
        endTime = datetime.now() + timedelta(seconds=duration)
        while(True):
            # Capture the video frame-by-frame
            ret, frame = vcap.read()
            #print cap.isOpened(), ret
            if frame is not None:
                # Display the retrieved frame
                # cv2.imshow('frame',frame)
                video.write(frame)
                # For testing purposes, press q to end the video stream manually
                if cv2.waitKey(22) & 0xFF == ord('q'):
                    break
                # Video ends if the duration is over
                if datetime.now() >= endTime:
                    break
            else:
                print("is None")
                break

        # Release the capture when everything is finished
        vcap.release()
        video.release()
        cv2.destroyAllWindows()
        print("Video stop")


#Windows version of the video recording script. Primarily for testing purposes.
def recordCameraWindows(directory, streamLink, imageLink, duration):
    
    stream = streamLink
    url = imageLink

    # Extract the camera's name from the video link
    camera = stream[stream.rfind("/"):stream.rfind(".")].replace('/', '')
    # print(stream.rfind("/"))
    # print(stream.rfind("."))
    # print(camera)
    
    #Establish a connection with the stream link
    vcap = cv2.VideoCapture(stream)

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

    #Use the picture if the video cannot be found
    if not vcap.isOpened():
        print("Video File Cannot be Opened")
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
        endTime = datetime.now() + timedelta(seconds=duration)
        while(True):
            # Capture the video frame-by-frame
            ret, frame = vcap.read()
            #print cap.isOpened(), ret
            if frame is not None:
                # Display the retrieved frame
                # cv2.imshow('frame',frame)
                video.write(frame)
                # For testing purposes, press q to end the video stream manually
                if cv2.waitKey(22) & 0xFF == ord('q'):
                    break
                # Video ends if the duration is over
                if datetime.now() >= endTime:
                    break
            else:
                print("is None")
                break

        # Release the capture when everything is finished
        vcap.release()
        video.release()
        cv2.destroyAllWindows()
        print("Video stop") 
