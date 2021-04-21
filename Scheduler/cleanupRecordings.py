import datetime
import shutil
import os

# Target directory takes in the base directory containing folders labelled by date
# DaysPast is how many days ago do you want to delete the files from (0 = Today, 1 = Yesterday, etc)
def cleanDirectory (targetDirectory, daysPast):
    #First, determine the exact date of the daysPast
    today = datetime.datetime.today()
    cutoff = datetime.timedelta(days=daysPast)
    targetDate = today - cutoff
    targetDateString = targetDate.strftime("%B %d, %Y")

    #Delete the entire directory
    directory = targetDirectory
    for filename in os.listdir(directory):
        if filename.find(targetDateString) > -1:
            try:
                shutil.rmtree(os.path.join(directory, filename))
            except OSError as e:
                print("Error: %s : %s" % (dir_path, e.strerror))
        else:
            continue
