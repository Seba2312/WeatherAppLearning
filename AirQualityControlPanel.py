from tkinter import ttk
import tkinter as tk

class AirQualityControlPanel:
    def __init__(self, root, weather_data):
        self.root = root
        self.weather_data = weather_data
        self.setup_air_quality_controls()

    def setup_air_quality_controls(self):
        ttk.Label(self.root, text="Enter CO Level:").grid(row=0, column=0)
        self.co_entry = ttk.Entry(self.root)
        self.co_entry.grid(row=0, column=1)

        ttk.Button(self.root, text="Find Closest City",
                   command=lambda: self.find_closest_city(self.co_entry.get())).grid(row=0, column=2)

        self.closest_city_label = ttk.Label(self.root, text="")
        self.closest_city_label.grid(row=1, columnspan=3)

        self.air_quality_label = ttk.Label(self.root, text="")
        self.air_quality_label.grid(row=2, columnspan=3)

        ttk.Button(self.root, text="Top 10 Best Air Quality",
                   command=self.show_top_10_best).grid(row=3, column=0)

        ttk.Button(self.root, text="Top 10 Worst Air Quality",
                   command=self.show_top_10_worst).grid(row=3, column=1)

        ttk.Button(self.root, text="Median 10 Air Quality",
                   command=self.show_median_10).grid(row=3, column=2)

        self.top_10_label = ttk.Label(self.root, text="")
        self.top_10_label.grid(row=4, columnspan=3)

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

    def find_closest_city(self, co_level):
        try:
            co_level = float(co_level)
            closest_city = None
            closest_diff = float('inf')

            for city in self.weather_data:
                city_co = city['current']['air_quality']['co']
                diff = abs(co_level - city_co)

                if diff < closest_diff:
                    closest_diff = diff
                    closest_city = city

            if closest_city is not None:
                closest_city_name = f"{closest_city['location']['name']}, {closest_city['location']['country']}: CO Level {closest_city['current']['air_quality']['co']}"
                self.closest_city_label.config(text=closest_city_name)

                # Calculate air quality rating
                rating = self.calculate_air_quality_rating(closest_city['current']['air_quality'])

                # Color-code the rating
                color = f"#{int(255 * rating / 10):02x}{int(255 * (10 - rating) / 10):02x}00"
                self.air_quality_label.config(text=f"Air Quality Rating: {rating}/10", background=color)
            else:
                self.closest_city_label.config(text="No matching city found.")
        except ValueError:
            self.closest_city_label.config(text="Invalid input. Please enter a number.")

    def show_top_10_best(self):
        self.show_top_10('best')

    def show_top_10_worst(self):
        self.show_top_10('worst')

    def show_top_10(self, quality_type):
        sorted_data = sorted(self.weather_data,
                             key=lambda x: self.calculate_air_quality_rating(x['current']['air_quality']))
        top_10 = sorted_data[:10] if quality_type == 'best' else sorted_data[-10:]

        # Debug: Print the worst city's rating to the console
        if quality_type == 'worst':
            worst_city = sorted_data[-1]
            worst_rating = self.calculate_air_quality_rating(worst_city['current']['air_quality'])
            print(f"Worst city's rating: {worst_rating}")

        top_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: Rating {self.calculate_air_quality_rating(city['current']['air_quality'])}/10"
            for city in top_10]
        self.top_10_label.config(text="\n".join(top_10_names))

    def show_median_10(self):
        sorted_data = sorted(self.weather_data,
                             key=lambda x: self.calculate_air_quality_rating(x['current']['air_quality']))

        median_index = len(sorted_data) // 2

        # Get the 5 cities before and 5 cities after the median index
        median_10 = sorted_data[median_index - 5: median_index + 5]

        median_10_names = [
            f"{city['location']['name']}, {city['location']['country']}: Rating {(city['current']['air_quality']['us-epa-index'] + city['current']['air_quality']['gb-defra-index']) // 2}/10"
            for city in median_10]
        self.top_10_label.config(text="\n".join(median_10_names))
    def clear_labels(self):
        self.closest_city_label.config(text="")
        self.air_quality_label.config(text="")
        self.top_10_label.config(text="")