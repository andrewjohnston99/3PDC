import config
import datetime
from locationsharinglib import Service
import logging
import math
import numpy as np
import OpenCVTEst
import os
import pandas as pd
import requests
from sklearn.neighbors import BallTree
import threading
import time

# Load vars from config and define global vars for main and functions
cookies_file = config.cookie_file
google_email = config.rpi_google_email
person_full_name = config.person_full_name
cfb_polling_interval = config.cfb_polling_interval_secs
GA511_url = config.GA511_cctv_url
GA511_geojson = config.GA511_local_geojson
next_cleanup_time = [""]

# [Broadcast Active, Session Initiated, Session Active, ID, Directory], Global & Mutable for Threads
session_status = [False, False, False, "", "/"]
cfb_thread_started = False
session_handler_thread_started = False
cleanup_thread_started = False

# Check to see if location sharing has started. Check every polling interval secs.
def check_for_broadcast(session_status):
    while(not session_status[0]):
        time.sleep(cfb_polling_interval)
        print("Checked for Broadcast")
        service = Service(cookies_file=cookies_file, authenticating_account=google_email)
        for person in service.get_all_people():
            if (person._full_name == person_full_name):
                print("Updated Session Status")
                session_status[0] = True

# Convert radius in miles to radius in fractional km for get_cams_in_radius
def miles_to_radius(miles):
    rad_of_earth_km = 6371
    miles_to_km_factor = 1.60934
    input_in_km = miles * miles_to_km_factor
    radius_value = (input_in_km / rad_of_earth_km)
    return radius_value

# Return polling interval (s) for given speed (mph)
def calculate_polling_vars(mph):
    # Case 1, >50 mph, ~1 mi per minute
    if (mph >= 50.0):
        return (30, 0.5)
    # Case 2, 30-49.99 mph, < 1 mi per min and > 1/2 mi per minute
    elif (mph >= 30.0):
        return (60, 1)
    # Case 3, >30 mph, > 1/2 mi per minute
    else:
        return (120, 1)

# Find miles between two points (direct path)
def get_distance_between_miles(latitude_0, longitude_0, latitude_1, longitude_1):
    rad_of_earth_km = 6371
    miles_to_km_factor = 1.60934

    lat_deg_0 = math.radians(latitude_0)
    lat_deg_1 = math.radians(latitude_1)
    long_deg_0 = math.radians(longitude_0)
    long_deg_1 = math.radians(longitude_1)

    dist_lat = lat_deg_1 - lat_deg_0
    dist_long = long_deg_1 - long_deg_0

    a = math.sin(dist_lat / 2)**2 + math.cos(latitude_0) * math.cos(latitude_1) * math.sin(dist_long / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = rad_of_earth_km * c
    distance_mi = distance_km / miles_to_km_factor
    
    return distance_mi

# Approximate Speed
def approx_speed(distance_mi, time_0, time_1):
    difference = time_1 - time_0
    hours = ((difference.total_seconds() / 60) / 60)
    estimated_mph = round((distance_mi/hours), 2)
    return estimated_mph

# Find all cams in x km radius of lat long coordinates
def get_cams_in_radius(latitude, longitude, radius):
    bt = BallTree(np.deg2rad(geojson[["latitude", "longitude"]].values), metric='haversine')
    indices = bt.query_radius(np.deg2rad(np.c_[latitude, longitude]), r=radius)
    return indices[0]

# Create folders and setup anything else necessary for a collection session.
def initialize_session(session_status):
    print("Now Initializing")
    
    name = (person_full_name.replace(" ","") + "_")
    init_date = datetime.datetime.now()
    session_ID = name + init_date.strftime("%Y-%m-%d_%H%M")

    try:
        path_string = r"/mnt/usbdrive/NAS/ATLTrafficLogArchive/" + session_ID
        os.mkdir(path_string)
    except:
        path = os.path.split(os.getcwd())
        path_string = path[0] + "\\" + session_ID
        os.mkdir(path_string)

    session_status[4] = path_string
    session_status[3] = session_ID
    session_status[1] = True

# Get location of user (for use during session)
def get_location():
    updated = None
    latitude = None
    longitude = None
    service = Service(cookies_file=cookies_file, authenticating_account=google_email)
    for person in service.get_all_people():
        if (person._full_name == person_full_name):
            updated = person.datetime
            latitude = person.latitude
            longitude = person.longitude
    return((latitude,longitude,updated))

# Handle Session, Poll location more frequently and handle invoking camera recordings
def session_handler(session_status):
    print("Session Handler Now Active")
    session_active = True
    cam_thread_num = 0
    polling_time_s = 60
    polling_radius_miles = 0.5
    estimated_speed_mph = 0
    last_loc = [None, None, None]
    curr_loc = [None, None, None]
    while (session_active):
        result = get_location()
        last_loc = curr_loc
        curr_loc = [result[0], result[1], result[2]]
        print(curr_loc)
        if (curr_loc == [None, None, None]):
            print("Marking End")
            session_active = False
            session_status[2] = False
            break
        if (last_loc != curr_loc):
            radius = miles_to_radius(polling_radius_miles)
            indices = get_cams_in_radius(curr_loc[0],curr_loc[1],radius)
            if (last_loc != [None, None, None]):
                distance = get_distance_between_miles(last_loc[0],last_loc[1],curr_loc[0],curr_loc[1])
                print(distance)
                estimated_speed_mph = approx_speed(distance, last_loc[2],curr_loc[2])
                print(estimated_speed_mph)
                polling_time_s, polling_radius_miles = calculate_polling_vars(estimated_speed_mph)
                print(polling_time_s)
                print(polling_radius_miles)
            for index in indices:
                rtsp = geojson.iloc[index].rtsp
                url = geojson.iloc[index].url
                print(rtsp)
                print(url)
                # threading.Thread(target = OpenCVTEst.recordCamera, args = (session_status[4],rtsp,url,polling_time_s)).start()
        time.sleep(polling_time_s)

# Initialize everything before scheduling loop
# Load latest cctv geojson from GA511, fallback to local on failure
try:
    result = requests.get(GA511_url)
    if (result.ok):
        open(GA511_geojson, "wb").write(result.content)
except:
    print("Unable to fetch geojson, falling back on local copy")

geojson = pd.DataFrame(columns = ["cam_id","latitude","longitude","rtsp","url"])
raw_geojson = pd.read_json(GA511_geojson)
if (raw_geojson.columns[0] == "features"):
    features_index = 0
else:
    features_index = 1

for row in raw_geojson.T.iteritems():
    try:
        properties = row[1][features_index].get("properties")
        rtsp = properties.get("RTSP", "")
        url = properties.get("url", "")
    except:
        properties = ""
        rtsp = ""
        url = ""
    try:
        coordinates = row[1][features_index].get("geometry").get("coordinates", "")
        latitude = float(coordinates[1])
        longitude = float(coordinates[0])
    except:
        coordinates = None
    cam_id = row[1][features_index].get("id", "")
    geojson = geojson.append({"cam_id" : cam_id, "latitude" : latitude, "longitude" : longitude, "rtsp" : rtsp, "url" : url}, ignore_index = True)
print("Loaded geojson")

# Main Decision Tree Scheduling Loop
while(True):
    # Case 1 - Just started, not polling, no active session
    if (not cfb_thread_started and not session_status[0]):
        cfb_thread = threading.Thread(target = check_for_broadcast, args = ([session_status]))
        cfb_thread_started = True
        cfb_thread.start()

    # Case 2 - Polling found new session, no active session
    if (cfb_thread_started and session_status[0] and not session_status[1] and not session_status[2]):
        cfb_thread._stop()
        cfb_thread_started = False
        int_session = threading.Thread(target = initialize_session, args = ([session_status]))
        int_session.start()

    # Case 3 - Session Initialized but not active
    if (not cfb_thread_started and session_status[0] and session_status[1] and not session_status[2]):
        int_session._stop()
        session_status[2] = True
        session_handler_thread_started = True
        session_handler_thread = threading.Thread(target = session_handler, args = ([session_status]))
        session_handler_thread.start()

    # Case 4 - Session Completed, reset everything and start from scratch
    if (session_handler_thread_started and not session_status[2]):
        print("Stopping Session")
        session_handler_thread._stop()
        session_handler_thread_started = False
        session_status = [False, False, False, "", "/"]

    # Case 5 - Start Cleanup
    # TODO - Need to handle setting next cleanup time, need thread active var too
