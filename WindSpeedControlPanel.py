from tkinter import ttk
import tkinter as tk

class WindSpeedControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data
        self.setup_wind_speed_controls()

    def setup_wind_speed_controls(self):
        ttk.Label(self.root, text="Enter Wind Speed:").grid(row=0, column=0)
        self.wind_speed_entry = ttk.Entry(self.root)
        self.wind_speed_entry.grid(row=0, column=1)

        self.unit_var = tk.StringVar(value='kph')
        ttk.Radiobutton(self.root, text='KPH', variable=self.unit_var, value='kph').grid(row=0, column=2)
        ttk.Radiobutton(self.root, text='MPH', variable=self.unit_var, value='mph').grid(row=0, column=3)

        ttk.Button(self.root, text="Find Closest City",
                   command=lambda: self.find_closest_city(self.wind_speed_entry.get(), self.unit_var.get())).grid(row=0,
                                                                                                                  column=4)

        ttk.Button(self.root, text="Show 10 Calmest Cities",
                   command=lambda: self.show_top_10('calmest', self.unit_var.get())).grid(row=2, column=0)

        ttk.Button(self.root, text="Show 10 Windiest Cities",
                   command=lambda: self.show_top_10('windiest', self.unit_var.get())).grid(row=2, column=1)

        ttk.Button(self.root, text="Show Median 10 Cities",
                   command=lambda: self.show_median_10(self.unit_var.get())).grid(row=2, column=2)

        self.closest_city_label = ttk.Label(self.root, text="")
        self.closest_city_label.grid(row=3, columnspan=5)  # Moved to row 3

        self.median_10_label = ttk.Label(self.root, text="")
        self.median_10_label.grid(row=4, columnspan=5)

        self.top_10_label = ttk.Label(self.root, text="")
        self.top_10_label.grid(row=5, columnspan=5)

    def find_closest_city(self, wind_speed, unit):
        try:
            wind_speed = float(wind_speed)
            closest_city = None
            closest_diff = float('inf')

            for city in self.weather_data:
                city_wind_speed = city['current']['wind_kph'] if unit == 'kph' else city['current']['wind_mph']
                diff = abs(wind_speed - city_wind_speed)

                if diff < closest_diff:
                    closest_diff = diff
                    closest_city = city

            if closest_city is not None:
                closest_city_wind_speed = closest_city['current']['wind_kph'] if unit == 'kph' else closest_city['current']['wind_mph']
                closest_city_name = f"{closest_city['location']['name']}, {closest_city['location']['country']}: {closest_city_wind_speed} {unit}"
                self.closest_city_label.config(text=closest_city_name)
            else:
                self.closest_city_label.config(text="No matching city found.")
        except ValueError:
            self.closest_city_label.config(text="Invalid input. Please enter a number.")


    def show_top_10(self, wind_type, unit):
        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['wind_kph']) if unit == 'kph' else sorted(
            self.weather_data, key=lambda x: x['current']['wind_mph'])
        top_10 = sorted_data[:10] if wind_type == 'calmest' else sorted_data[-10:]

        top_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: {city['current']['wind_kph']} KPH" if unit == 'kph' else f"{city['location']['name']}, {city['location']['country']}: {city['current']['wind_mph']} MPH"
            for city in top_10]
        self.closest_city_label.config(text="\n".join(top_10_names))

    def show_median_10(self, unit):
        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['wind_kph']) if unit == 'kph' else sorted(
            self.weather_data, key=lambda x: x['current']['wind_mph'])
        median_index = len(sorted_data) // 2

        # Get the 5 cities before and 5 cities after the median index
        median_10 = sorted_data[median_index - 5: median_index + 5]

        median_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: {city['current']['wind_kph']} KPH" if unit == 'kph' else f"{city['location']['name']}, {city['location']['country']}: {city['current']['wind_mph']} MPH"
            for city in median_10]
        self.closest_city_label.config(text="\n".join(median_10_names))
