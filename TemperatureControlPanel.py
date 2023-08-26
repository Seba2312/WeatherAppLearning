from tkinter import ttk
import tkinter as tk


class TemperatureControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data
        self.setup_temperature_controls()

    def setup_temperature_controls(self):
        ttk.Label(self.root, text="Enter Temperature:").grid(row=0, column=0)
        self.temp_entry = ttk.Entry(self.root)
        self.temp_entry.grid(row=0, column=1)

        self.unit_var = tk.StringVar(value='C')
        ttk.Radiobutton(self.root, text='Celsius', variable=self.unit_var, value='C').grid(row=0, column=2)
        ttk.Radiobutton(self.root, text='Fahrenheit', variable=self.unit_var, value='F').grid(row=0, column=3)

        ttk.Button(self.root, text="Find Closest City",
                   command=lambda: self.find_closest_city(self.temp_entry.get(), self.unit_var.get())).grid(row=0,
                                                                                                            column=4)

        self.closest_city_label = ttk.Label(self.root, text="")
        self.closest_city_label.grid(row=1, columnspan=5)

        ttk.Button(self.root, text="Show 10 Coldest Cities",
                   command=lambda: self.show_top_10('coldest', self.unit_var.get())).grid(row=2, column=0)

        ttk.Button(self.root, text="Show 10 Hottest Cities",
                   command=lambda: self.show_top_10('hottest', self.unit_var.get())).grid(row=2, column=1)

        ttk.Button(self.root, text="Show Median 10 Cities",
                   command=lambda: self.show_median_10(self.unit_var.get())).grid(row=2, column=2)

        self.median_10_label = ttk.Label(self.root, text="")
        self.median_10_label.grid(row=4, columnspan=5)

        self.top_10_label = ttk.Label(self.root, text="")
        self.top_10_label.grid(row=3, columnspan=5)

    # ... (Include the find_closest_city, show_top_10, and show_median_10 methods here)

    def find_closest_city(self, temp, unit):
        try:
            temp = float(temp)  # Attempt to convert input to float
            closest_city = None
            closest_diff = float('inf')

            for city in self.weather_data:
                city_temp = city['current']['temp_c'] if unit == 'C' else city['current']['temp_f']
                diff = abs(temp - city_temp)

                if diff < closest_diff:
                    closest_diff = diff
                    closest_city = city

            if closest_city is not None:  # Check if a closest city was found
                closest_city_temp = closest_city['current']['temp_c'] if unit == 'C' else closest_city['current'][
                    'temp_f']
                closest_city_name = f"{closest_city['location']['name']}, {closest_city['location']['country']}: {closest_city_temp}°{unit}"
                self.closest_city_label.config(text=closest_city_name)
            else:
                self.closest_city_label.config(text="No matching city found.")
        except ValueError:  # Catch errors related to float conversion
            self.closest_city_label.config(text="Invalid input. Please enter a number.")

    def show_top_10(self, temp_type, unit):
        self.median_10_label.config(text="")  # clears name so not distracting

        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['temp_c']) if unit == 'C' else sorted(
            self.weather_data, key=lambda x: x['current']['temp_f'])
        top_10 = sorted_data[:10] if temp_type == 'coldest' else sorted_data[-10:]

        top_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: {city['current']['temp_c']}°C" if unit == 'C' else f"{city['location']['name']}, {city['location']['country']}: {city['current']['temp_f']}°F"
            for city in top_10]
        self.top_10_label.config(text="\n".join(top_10_names))

    def show_median_10(self, unit):
        self.top_10_label.config(text="")  # clears name so not distracting

        sorted_data = sorted(self.weather_data, key=lambda x: x['current']['temp_c']) if unit == 'C' else sorted(
            self.weather_data, key=lambda x: x['current']['temp_f'])
        median_index = len(sorted_data) // 2

        # Get the 5 cities before and 5 cities after the median index
        median_10 = sorted_data[median_index - 5: median_index + 5]

        median_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: {city['current']['temp_c']}°C" if unit == 'C' else f"{city['location']['name']}, {city['location']['country']}: {city['current']['temp_f']}°F"
            for city in median_10]
        self.median_10_label.config(text="\n".join(median_10_names))

    def clear_labels(self):
        self.closest_city_label.config(text="")
