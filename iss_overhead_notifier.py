import requests
from datetime import datetime
import math
import smtplib
import time
from os import environ

MY_LAT = -34.571918
MY_LON = -58.488548

# http://api.open-notify.org
def get_iss_position():
  req = requests.get("http://api.open-notify.org/iss-now.json")
  req.raise_for_status()
  # print(req.json())
  iss_lat = float(req.json()['iss_position']['latitude'])
  iss_long = float(req.json()['iss_position']['longitude'])
  iss_position = (iss_lat, iss_long)
  print(f"ISS position: {iss_position}")
  return iss_position

def is_iss_overhead(iss_lat, iss_long):
  is_overhead = math.isclose(MY_LAT, iss_lat, abs_tol=5) and math.isclose(MY_LON, iss_long, abs_tol=5)
  print(f"Is ISS overhead?: {is_overhead}\n")
  return is_overhead

# https://sunrise-sunset.org/api
def get_sunrise_sunset():
  parameters = {
    "lat": MY_LAT,
    "lng": MY_LON,
    "formatted": 0
  }

  # req2 = requests.get(f"https://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LON}")
  req2 = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
  req2.raise_for_status()
  data = req2.json()
  # print(data['results'])
  sunrise = data['results']['sunrise']
  sunset = data['results']['sunset']
  sunrise_datetime = datetime.strptime(sunrise.split('+')[0], "%Y-%m-%dT%H:%M:%S")
  sunset_datetime = datetime.strptime(sunset.split('+')[0], "%Y-%m-%dT%H:%M:%S")
  return {"sunrise": sunrise_datetime, "sunset": sunset_datetime}

def is_night(sunrise, sunset):
  now = datetime.now()
  # print(f"Now: {now}")
  now_utc = now.utcnow()
  print(f"Current time: {now_utc}")
  night = (sunset < now_utc) or (sunrise > now_utc)
  print(f"Is it night?: {night}\n")
  return night

def send_email(iss_position):
  source_email = environ.get("SOURCE_EMAIL")
  source_pwd = environ.get("SOURCE_AUTH_KEY")
  target_email = environ.get("TARGET_EMAIL")
  smtp_server = environ.get("YH_SMTP_SERVER")
  subject = "Look up!"
  message = f"The ISS is visible now at {iss_position}!!"

  connection = smtplib.SMTP(smtp_server)
  connection.starttls() # To make it secure
  connection.login(user=source_email, password=source_pwd)
  connection.sendmail(from_addr=source_email, to_addrs=target_email, msg=f"Subject:{subject}\n\n{message}")
  connection.close()

sunstate = get_sunrise_sunset()

while True:
  print(f"---------------------------------------------------------\nMy location: {MY_LAT, MY_LON}")
  print(f"Sunrise: {sunstate['sunrise']}, Sunset: {sunstate['sunset']}\n")
  
  iss_position = get_iss_position()
  overhead = is_iss_overhead(iss_position[0], iss_position[1])
  night = is_night(sunrise=sunstate['sunrise'], sunset=sunstate['sunset'])
  is_visible = overhead and night

  print(f"ISS is visible?: {is_visible}\n")

  if is_visible:
    send_email(iss_position)
    print("Mail sent")
  
  time.sleep(60)

