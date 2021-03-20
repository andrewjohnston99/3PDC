import os
from datetime import date

path = os.getcwd()
print ("The current working directory is %s" % path)
finalpath = path + "\TestDirectory-" + date.today().strftime("%B %d, %Y")

try:
    os.mkdir(finalpath)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)