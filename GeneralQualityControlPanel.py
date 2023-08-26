from tkinter import ttk
import tkinter as tk

class GeneralQualityControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data
        self.setup_general_quality_controls()

    def setup_general_quality_controls(self):
        ttk.Label(self.root, text="General Quality of Cities").grid(row=0, column=0, columnspan=4)
        ttk.Label(self.root,
                  text="Ideal cities are calculated based on temperature, humidity, wind speed, and air quality.").grid(
            row=1, column=0, columnspan=4)

        ttk.Label(self.root,
                  text="Temperature (20-22°C): This is considered a comfortable room temperature range for most people.").grid(
            row=2, column=0, columnspan=4)

        ttk.Label(self.root,
                  text="Humidity (30-60%): This range is generally considered comfortable and is not too dry or too humid.").grid(
            row=3, column=0, columnspan=4)

        ttk.Label(self.root,
                  text="Wind Speed (6-19 km/h): This range is generally considered to be a gentle to fresh breeze, which is pleasant for most outdoor activities.").grid(
            row=4, column=0, columnspan=4)

        ttk.Label(self.root,
                  text="Air Quality (1): A rating of 1 indicates the best possible air quality, which is ideal for all activities.").grid(
            row=5, column=0, columnspan=4)
        # Temperature
        ttk.Label(self.root, text="Temperature Range (°C):").grid(row=6, column=0)
        self.temp_entry = ttk.Entry(self.root)
        self.temp_entry.grid(row=6, column=1)
        self.temp_entry.insert(0, "20-22")  # Default: Common comfort range

        # Humidity
        ttk.Label(self.root, text="Humidity Range (%):").grid(row=6, column=2)
        self.humidity_entry = ttk.Entry(self.root)
        self.humidity_entry.grid(row=6, column=3)
        self.humidity_entry.insert(0, "30-60")  # Default: Comfortable for humans

        # Wind Speed
        ttk.Label(self.root, text="Wind Speed Range (km/h):").grid(row=7, column=0)
        self.wind_speed_entry = ttk.Entry(self.root)
        self.wind_speed_entry.grid(row=7, column=1)
        self.wind_speed_entry.insert(0, "6-19")  # Default: Gentle to fresh breeze

        # Air Quality
        ttk.Label(self.root, text="Air Quality Rating (1-10):").grid(row=7, column=2)
        self.air_quality_entry = ttk.Entry(self.root)
        self.air_quality_entry.grid(row=7, column=3)
        self.air_quality_entry.insert(0, "0-1")  # Default: Best air quality

        ttk.Button(self.root, text="Show Ideal Cities", width=20,
                   command=self.show_ideal_cities).grid(row=8, column=0, columnspan=4)

        self.ideal_cities_label = ttk.Label(self.root, text="")
        self.ideal_cities_label.grid(row=9, column=0, columnspan=4)

    def show_ideal_cities(self):
        ideal_cities = self.filter_ideal_cities()
        if ideal_cities:
            self.ideal_cities_label.config(text="\n".join(ideal_cities))
        else:
            self.ideal_cities_label.config(text="No cities found with ideal conditions.")

    def filter_ideal_cities(self):
        temp_range = list(map(int, self.temp_entry.get().split('-')))
        humidity_range = list(map(int, self.humidity_entry.get().split('-')))
        wind_speed_range = list(map(int, self.wind_speed_entry.get().split('-')))
        air_quality_rating = list(map(int, self.air_quality_entry.get().split('-')))
        ideal_cities = []
        for city in self.weather_data:
            temp = city['current']['temp_c']
            humidity = city['current']['humidity']
            wind_speed = city['current']['wind_kph']
            air_quality_data = city['current']['air_quality']
            air_quality = self.calculate_air_quality_rating(air_quality_data)

            if temp_range[0] <= temp <= temp_range[1] and humidity_range[0] <= humidity <= humidity_range[1] and \
                    wind_speed_range[0] <= wind_speed <= wind_speed_range[1] and  air_quality_rating[0] <= air_quality <= air_quality_rating[1]:
                ideal_cities.append(f"{city['location']['name']}, {city['location']['country']}")

        return ideal_cities
    def calculate_air_quality_rating(self, air_quality_data):
        us_index = air_quality_data['us-epa-index']
        gb_index = air_quality_data['gb-defra-index']
        rating = (us_index + gb_index) // 2

        # Add to the rating based on individual chemical levels
        if air_quality_data['co'] > 400: rating += 1
        if air_quality_data['co'] > 800: rating += 1
        if air_quality_data['co'] > 1200: rating += 1
        if air_quality_data['no2'] > 20: rating += 1
        if air_quality_data['no2'] > 40: rating += 1
        if air_quality_data['o3'] > 30: rating += 1
        if air_quality_data['so2'] > 10: rating += 1
        if air_quality_data['pm2_5'] > 10: rating += 1
        if air_quality_data['pm10'] > 20: rating += 1

        # Cap the rating at 10
        rating = min(rating, 10)

        return rating