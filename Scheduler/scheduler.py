import logging
import threading
import time
import config
from locationsharinglib import Service

cookies_file = config.cookie_file
google_email = config.rpi_google_email
service = Service(cookies_file=cookies_file, authenticating_account=google_email)
for person in service.get_all_people():
    print(person)
