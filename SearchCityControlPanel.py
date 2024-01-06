import tkinter as tk
from tkinter import ttk
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
import re
import json
import requests


def insert_space_between_caps(s):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', s)

class SearchCityControlPanel:
    def __init__(self, root, city_name):
        self.root = root
        self.setup_search_controls(city_name)

    def setup_search_controls(self, city_name):
        self.root.geometry("600x400")  # Set window size
        self.result_label = ttk.Label(self.root, text=city_name, font=("Helvetica", 14))
        self.result_label.grid(row=0, column=0)
        self.suggestion_label = ttk.Label(self.root, text="", font=("Helvetica", 12))
        self.suggestion_label.grid(row=1, column=0)
        self.error_label = ttk.Label(self.root, text="", font=("Helvetica", 12))  # New label
        self.error_label.grid(row=2, column=0)  # New label
        self.perform_search(city_name)  # Call perform_search here

    def perform_search(self, city_name):
        session = WolframLanguageSession()
        search_result = ""
        try:
            interpreted_city = session.evaluate(f'Interpreter["City", AmbiguityFunction->All]["{city_name}"]')
            if 'Failure' not in str(interpreted_city):
                correct_city_name_tuple = session.evaluate(wl.CommonName(interpreted_city[0]))
                correct_city_name = correct_city_name_tuple[0]

                if correct_city_name == "City":
                    correct_city_name_tuple = session.evaluate(wl.CommonName(interpreted_city[1]))
                    correct_city_name = correct_city_name_tuple[0]

                if type(correct_city_name) is tuple:
                    correct_city_name = correct_city_name[0]

                correct_city_name = insert_space_between_caps(correct_city_name)

                if correct_city_name != city_name:
                    self.suggestion_label.config(text=f"Did you mean {correct_city_name} and not {city_name} ?")

                weather_data = fetch_weather(correct_city_name)
                if weather_data:
                    wind_speed_kph = weather_data['current']['wind_kph']
                    temp_c = weather_data['current']['temp_c']
                    humidity = weather_data['current']['humidity']
                    condition = weather_data['current']['condition']['text']
                    air_quality_data = weather_data['current']['air_quality']
                    country = weather_data['location']['country']
                    air_quality_rating = calculate_air_quality_rating(air_quality_data)

                    # Update Tkinter labels
                    self.result_label.config(text=f"Search results for {correct_city_name}, {country}.")
                    self.error_label.config(
                        text=f"Wind Speed: {wind_speed_kph} kph\nTemperature: {temp_c}°C\nHumidity: {humidity}%\nCondition: {condition}\nAir Quality Rating: {air_quality_rating}")
                else:
                    self.result_label.config(text=f"Weather data not found for {correct_city_name}.")
            else:
                self.error_label.config(text="City not found or spelling too far off.")  # Use error_label here
        except Exception as e:
            search_result = f"An error occurred: {e}"
        finally:
            session.terminate()




def calculate_air_quality_rating( air_quality_data):
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

# Your weather API function
def fetch_weather(location):
    url = "http://api.weatherapi.com/v1/current.json" #https://www.weatherapi.com/my/  from here
    params = {
        "key": "8e3936c9bedd4e4a87c112506232508",  # Your API key
        "q": location,
        "aqi": "yes"  # Include Air Quality Index
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data for {location}: {response.status_code}")
        return None

