import requests
from datetime import datetime

# https://openweathermap.org/api
API_KEY = "50cee60b5708c93ef70c36e29939aaf6"
MY_LAT = -34.571918
MY_LON = -58.488548

ow_endpoint_current = "https://api.openweathermap.org/data/2.5/weather"
ow_endpoint_forecast = "https://api.openweathermap.org/data/2.5/forecast"

ow_params = {
  "lat": MY_LAT,
  "lon": MY_LON,
  "appid": API_KEY,
  "units": "metric"
}

choice = "Current"

if choice.lower() == 'current':
  req = requests.get(ow_endpoint_current, params=ow_params)
  # print(req)
  req.raise_for_status()
  data = req.json()
  print(data)
  ow_id = data['weather'][0]['id']
  ow_weather = data['weather'][0]['main']
  ow_description = data['weather'][0]['description']
  ow_icon = data['weather'][0]['icon']
  ow_temp = round(data['main']['temp'],)
  ow_feels_like = round(data['main']['feels_like'])
  ow_temp_min = round(data['main']['temp_min'])
  ow_temp_max = round(data['main']['temp_max'])
  ow_preassure = data['main']['pressure']
  ow_humidity = data['main']['humidity']
  ow_visibility = round(float(data['visibility'] / 1000))
  ow_wind_speed = round(float(data['wind']['speed']) * 3600 / 1000)
  ow_sunrise = datetime.fromtimestamp(data['sys']['sunrise']).time()
  ow_sunset = datetime.fromtimestamp(data['sys']['sunset']).time()
  ow_city = f"{data['name']}, {data['sys']['country']}"
elif choice.lower() == 'forecast':
  req = requests.get(ow_endpoint_forecast, params=ow_params)
  # print(req)
  req.raise_for_status()
  data = req.json()
  print(data)
  rainy_days = []
  for item in data['list']:
    if int(item['weather'][0]['id']) < 700:
      rainy_days.append(item['dt_txt'])
    print(f"{item['dt_txt']}\nTemp: {round(item['main']['temp'], 1)}°C\n{item['weather'][0]['main']} ({item['weather'][0]['description']})\n")
  if len(rainy_days) > 0:
    print(f"Get an umbrella, it will rain on {rainy_days}")