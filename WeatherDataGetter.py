import json
import requests
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# Initialize the Wolfram Language Session
session = WolframLanguageSession()

# Your weather API function
def fetch_weather(location):
    url = "http://api.weatherapi.com/v1/current.json"
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

try:
    # Read city names from cities.json
    with open("cities.json", "r") as f:
        city_names = json.load(f)

    # Fetch weather data for all cities in the list
    weather_data_list = []
    for city in city_names:
        weather_data = fetch_weather(city)
        if weather_data:
            weather_data_list.append(weather_data)

    # Sort by city name alphabetically
    sorted_by_city_name = sorted(weather_data_list, key=lambda x: x['location']['name'])

    # Write sorted data to JSON file
    with open("sorted_weather_data.json", "w") as f:
        json.dump(sorted_by_city_name, f, indent=4)

    print("Weather data has been written to sorted_weather_data.json")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.terminate()
