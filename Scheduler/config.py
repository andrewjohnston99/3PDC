# Config File for 3PDC Scheduler

platform = "LINUX" # Replace with "WINDOWS" for Development on Windows, defaut Linux for Pi
cookie_file = "google.com_cookies.txt"
rpi_google_email = "YOUR_PI_EMAIL_HERE"
person_full_name = "YOUR FULL NAME HERE (From Google Account that will initiate the share)"
max_cams = 10 # Only change if using system more powerful than Pi, may break for large numbers
cfb_polling_interval_secs = 60 # Default 1 min
GA511_cctv_url = "https://ga.cdn.iteris-atis.com/geojson/icons/metadata/icons.cctv.geojson"
GA511_local_geojson = "icons.cctv.geojson"
