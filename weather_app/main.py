from tkinter import *
from weather_data import *
import pandas


# def selected(event):
#   choice = variable.get()

window = Tk()
window.title("Weather app")
window.minsize(300, 500)

# variable = StringVar(window)
# variable.set("Current") # default value
# drop_down_menu = OptionMenu(window, variable, "Current", "Forecast", command=selected)
# drop_down_menu.grid(row=0, column=1, columnspan=3)


if ow_icon == "01n":
  background_color = "midnight blue"
  foreground_color = "light slate gray"
elif ow_id == 800:
  background_color = "dodger blue"
  foreground_color = "white"
elif 600 <= ow_id < 700:
  background_color = "white smoke"
  foreground_color = "black"
elif 200 <= ow_id < 300:
  background_color = "dim gray"
  foreground_color = "white"
else:
  background_color = "light slate gray"
  foreground_color = "white"

window.config(bg=background_color)
city = Label(text=ow_city, font=("Arial", 20, "normal"), bg=background_color, fg=foreground_color)
city.grid(row=1, column=1, columnspan=3, pady=15)
temp = Label(text=f"{ow_temp}ºC", font=("Arial", 90, "bold"), bg=background_color, fg=foreground_color)
temp.grid(row=2, column=1, columnspan=3)
icon = Canvas(width=70, height=70, bg=background_color, highlightthickness=0)
icon_img = PhotoImage(file=f"./icons/{ow_icon}.png")
icon.create_image(35, 35, image=icon_img)
icon.grid(row=4, column=1, columnspan=3)
weather_condition = Label(text=f"Weather condition: {ow_weather} ({ow_description})", font=("Arial", 17, 'normal'), bg=background_color, fg=foreground_color)
feels_like = Label(text=f"FL: {ow_feels_like} ºC", bg=background_color, fg=foreground_color)
temp_max = Label(text=f"Max: {ow_temp_max} ºC", bg=background_color, fg=foreground_color)
temp_min = Label(text=f"Min: {ow_temp_min} ºC", bg=background_color, fg=foreground_color)
wind_speed = Label(text=f"Wind: {ow_wind_speed} Km/h", bg=background_color, fg=foreground_color)
visibility = Label(text=f"Visibility: {ow_visibility} Km", bg=background_color, fg=foreground_color)
humidity = Label(text=f"Humidity: {ow_humidity} %", bg=background_color, fg=foreground_color)
preassure = Label(text=f"Preassure: {ow_preassure} hpa", bg=background_color, fg=foreground_color)
sunrise = Label(text=f"Sunrise: {ow_sunrise}", bg=background_color, fg=foreground_color)
sunset = Label(text=f"Sunset: {ow_sunset}", bg=background_color, fg=foreground_color)
weather_condition.grid(row=5, column=1, columnspan=3, padx=20, pady=20)
feels_like.grid(row=3, column=1, columnspan=3)
temp_min.grid(row=6, column=1)
temp_max.grid(row=6, column=3)
wind_speed.grid(row=7, column=1, pady=20)
visibility.grid(row=7, column=3, pady=20)
humidity.grid(row=8, column=1)
preassure.grid(row=8, column=3)
sunrise.grid(row=9, column=1, pady=20)
sunset.grid(row=9, column=3, pady=20)

window.mainloop()