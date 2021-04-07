import logging
import threading
import time
import datetime
import config
from locationsharinglib import Service

cookies_file = config.cookie_file
google_email = config.rpi_google_email
person_full_name = config.person_full_name
cfb_polling_interval = config.cfb_polling_interval_secs
next_cleanup_time = [""]

# [Broadcast Active, Session Initiated, Session Active, ID, Directory], Global & Mutable for Threads
session_status = [False, False, False, "", "/"]
cfb_thread_started = False
cleanup_thread_started = False

# Check to see if location sharing has started. Check every polling interval secs.
def check_for_broadcast(session_status):
    while(not session_status[0]):
        time.sleep(cfb_polling_interval)
        print("Checked!")
        service = Service(cookies_file=cookies_file, authenticating_account=google_email)
        for person in service.get_all_people():
            if (person._full_name == person_full_name):
                print("Updated session status!")
                session_status[0] = True

# Create folders and setup anything else necessary for a collection session.
def initialize_session(session_status):
    print("Now initializing!")
    # TODO Create Folders...

    # Sleep to simulate loading...
    time.sleep(10)

    name = (person_full_name.replace(" ","") + "_")
    init_date = datetime.datetime.now()
    session_ID = name + init_date.strftime("%Y-%m-%d_%H:%M")

    print(session_ID)

    session_status[3] = session_ID
    session_status[1] = True

# Poll location more frequently and handle invoking camera recordings
def session_handler(session_status):
    # TODO
    return

# Main Decision Tree Scheduling Loop
while(True):
    # Case 1 - Just started, not polling, no active session
    if (not cfb_thread_started and not session_status[0]):
        cfb_thread = threading.Thread(check_for_broadcast(session_status))
        cfb_thread.start()
        cfb_thread_started = True

    # Case 2 - Polling found new session, no active session
    if (cfb_thread_started and session_status[0] and not session_status[1] and not session_status[2]):
        cfb_thread._stop()
        cfb_thread_started = False
        int_session = threading.Thread(initialize_session(session_status))
        int_session.start()

    # Case 3 - Session Initialized but not active
    if (not cfb_thread_started and session_status[0] and session_status[1]):
        int_session._stop()
        # session_handler_thread = threading.Thread(session_handler(session_status))

    # Case 4 - Session Active

    # Case 5 - Start Cleanup
