import json
import tkinter as tk
from tkinter import ttk

from GeneralQualityControlPanel import GeneralQualityControlPanel
from SearchCityControlPanel import SearchCityControlPanel
from TemperatureControlPanel import TemperatureControlPanel
from HumidityControlPanel import HumidityControlPanel
from AirQualityControlPanel import AirQualityControlPanel
from WindSpeedControlPanel import WindSpeedControlPanel


class WeatherControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data

    def clear_labels(self):
        pass  # To be implemented in child classes

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def open_temperature_window():
    temp_window = tk.Toplevel(root)
    temp_window.title("Temperature Features")
    temp_panel = TemperatureControlPanel(temp_window, weather_data)

def open_humidity_window():
    humidity_window = tk.Toplevel(root)
    humidity_window.title("Humidity Features")
    humidity_panel = HumidityControlPanel(humidity_window, weather_data)

# air quality is a bit dubious, as many countries have great air quality and other do not, but generally works
def open_air_quality_window():
    air_quality_window = tk.Toplevel(root)
    air_quality_window.title("Air Quality Features")
    air_quality_panel = AirQualityControlPanel(air_quality_window, weather_data)

def open_wind_window():
    wind_window = tk.Toplevel(root)
    wind_window.title("Wind Features")
    wind_panel = WindSpeedControlPanel(wind_window, weather_data)

def open_general_quality_window():
    general_quality_window = tk.Toplevel(root)
    general_quality_window.title("General Quality")
    general_quality_panel = GeneralQualityControlPanel(general_quality_window, weather_data)
    search_panel = None  # Declare as global at the top of your script

def open_search_window(city_name):
    global search_panel  # Declare as global
    search_window = tk.Toplevel(root)
    search_window.title("Search for City")
    search_panel = SearchCityControlPanel(search_window, city_name)  # Pass city_name as an argument

search_panel = None  # Declare as global at the top of your script

def search_function():
    city_name = city_entry.get()
    open_search_window(city_name)  # Call open_search_window with city_name

def main():
        global weather_data, root, city_entry
        weather_data = read_json_file('sorted_weather_data.json')
        root = tk.Tk()
        root.title("Weather Finder")

        city_entry = tk.Entry(root, width=30)
        city_entry.pack(side="top")
        city_entry.insert(0, "Enter city name")

        # Create a Search button
        tk.Button(root, text="Search for a City", command=search_function, width=20, height=2).pack(side="top")

        # Create buttons with increased width and height
        tk.Button(root, text="Temperature", command=open_temperature_window, width=20, height=2).pack(side="left")
        tk.Button(root, text="Humidity", command=open_humidity_window, width=20, height=2).pack(side="left")
        tk.Button(root, text="Air Quality", command=open_air_quality_window, width=20, height=2).pack(side="left")
        tk.Button(root, text="Wind", command=open_wind_window, width=20, height=2).pack(side="left")
        tk.Button(root, text="General Quality", command=open_general_quality_window, width=20, height=2).pack(side="left")


        root.mainloop()

if __name__ == "__main__":
    main()
