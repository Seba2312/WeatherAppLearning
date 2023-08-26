from tkinter import ttk
import tkinter as tk

class HumidityControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data
        self.setup_humidity_controls()

    def setup_humidity_controls(self):
        ttk.Label(self.root, text="Enter Humidity:").grid(row=0, column=0)
        self.humidity_entry = ttk.Entry(self.root)
        self.humidity_entry.grid(row=0, column=1)

        ttk.Button(self.root, text="Find Closest City",
                   command=lambda: self.find_closest_city(self.humidity_entry.get())).grid(row=0, column=2)

        self.closest_city_label = ttk.Label(self.root, text="")
        self.closest_city_label.grid(row=1, columnspan=3)

        ttk.Button(self.root, text="Show 10 Cities with Lowest Humidity",
                   command=lambda: self.show_top_10('lowest')).grid(row=2, column=0)

        ttk.Button(self.root, text="Show 10 Cities with Highest Humidity",
                   command=lambda: self.show_top_10('highest')).grid(row=2, column=1)

        ttk.Button(self.root, text="Show Median 10 Cities",
                   command=self.show_median_10).grid(row=2, column=2)

        self.median_10_label = ttk.Label(self.root, text="")
        self.median_10_label.grid(row=4, columnspan=3)

        self.top_10_label = ttk.Label(self.root, text="")
        self.top_10_label.grid(row=3, columnspan=3)

    def find_closest_city(self, humidity):
        try:
            humidity = int(humidity)
            closest_city = None
            closest_diff = float('inf')

            for city in self.weather_data:
                city_humidity = city['current']['humidity']
                diff = abs(humidity - city_humidity)

                if diff < closest_diff:
                    closest_diff = diff
                    closest_city = city

            if closest_city is not None:
                closest_city_name = f"{closest_city['location']['name']}, {closest_city['location']['country']}: {closest_city['current']['humidity']}%"
                self.closest_city_label.config(text=closest_city_name)
            else:
                self.closest_city_label.config(text="No matching city found.")
        except ValueError:
            self.closest_city_label.config(text="Invalid input. Please enter a number.")

    def show_top_10(self, humidity_type):
        self.median_10_label.config(text="")
        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['humidity'])
        top_10 = sorted_data[:10] if humidity_type == 'lowest' else sorted_data[-10:]

        top_10_names = [f"{city['location']['name']}, {city['location']['country']}: {city['current']['humidity']}%" for city in top_10]
        self.top_10_label.config(text="\n".join(top_10_names))

    def show_median_10(self):
        self.top_10_label.config(text="")
        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['humidity'])
        median_index = len(sorted_data) // 2
        median_10 = sorted_data[median_index - 5: median_index + 5]

        median_10_names = [f"{city['location']['name']}, {city['location']['country']}: {city['current']['humidity']}%" for city in median_10]
        self.median_10_label.config(text="\n".join(median_10_names))

    def clear_labels(self):
        self.closest_city_label.config(text="")
