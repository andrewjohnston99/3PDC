import logging
import threading
import time
import config
from locationsharinglib import Service

cookies_file = config.cookie_file
google_email = config.rpi_google_email
person_full_name = config.person_full_name
cfb_polling_interval = config.cfb_polling_interval_secs

# Session Active, Session Initiated, ...
session_status = [False, False]

def check_for_broadcast(session_status):
    print("Checked!")
    service = Service(cookies_file=cookies_file, authenticating_account=google_email)
    for person in service.get_all_people():
        if (person._full_name == person_full_name):
            session_status[0] = True
            print("Updated session status!")

cfb_thread = threading.Timer((cfb_polling_interval), check_for_broadcast(session_status))

while (not session_status[0]):
    cfb_thread.start()

# while (session_status[0] and not session_status[1]):
    

# while (session_status[0] and session_status[1]):
