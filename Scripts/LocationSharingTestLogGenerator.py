#Testing script for location sharing
from locationsharinglib import Service
import time

log_file = open("log.txt", "w")

while(True):
    service = Service(cookies_file="..\Scheduler\google.com_cookies.txt", authenticating_account="@gmail.com")
    for person in service.get_all_people():
        log_file.write(str(person))
    time.sleep(30)
