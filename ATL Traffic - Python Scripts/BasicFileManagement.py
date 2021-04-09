import os
from datetime import date
import OpenCVTEst

OpenCVTEst.recordCamera(r'C:\Users\clayw\Documents\ATL Traffic\ATLTrafficLog\Function-Directory-Test',r'rtsp://vss15od.dot.ga.gov:80/cl/gdot-cam-i-75-lol.stream',r'http://navigator-c2c.dot.ga.gov/snapshots/ATL-CAM-908.jpg')

path = os.getcwd()
print ("The current working directory is %s" % path)
finalpath = path + "\TestDirectory-" + date.today().strftime("%B %d, %Y")

try:
    os.mkdir(finalpath)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)