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
    # Fetch all countries
    all_countries = session.evaluate(wl.EntityList("Country"))

    # Initialize an empty dictionary to store country names and their populations
    country_population = {}

    # Extract and print the country names and their populations
    for country in all_countries:
        country_name = session.evaluate(wl.CommonName(country))
        population_quantity = session.evaluate(wl.EntityValue(country, 'Population'))

        # Check if population is available
        if population_quantity != wl.Missing('NotAvailable'):
            # Extract the numerical part of the population
            population = session.evaluate(wl.QuantityMagnitude(population_quantity))
            country_population[country_name] = population

    # Filter out countries with populations less than 5 million
    filtered_countries = {k: v for k, v in country_population.items() if v > 5_000_000}

    # Extract and print the capitals of filtered countries
    capitals = [session.evaluate(wl.EntityValue(country, 'CapitalCity')) for country in all_countries if
                session.evaluate(wl.CommonName(country)) in filtered_countries.keys()]
    capital_names = [session.evaluate(wl.CommonName(capital)) for capital in capitals]

    # Fetch weather data for all capitals in the list
    weather_data_list = []
    for city in capital_names:
        weather_data = fetch_weather(city)
        if weather_data:
            weather_data_list.append(weather_data)

    # Your sorting logic here
    # ...


    # Sort by temperature
    sorted_by_temperature = sorted(weather_data_list, key=lambda x: x['current']['temp_c'])

    # Sort by humidity
    sorted_by_humidity = sorted(weather_data_list, key=lambda x: x['current']['humidity'])

    # Sort by air quality (if available)
    sorted_by_air_quality = sorted(weather_data_list, key=lambda x: x['current']['air_quality']['us-epa-index'] if 'air_quality' in x['current'] else float('inf'))

    with open("sorted_weather_data.json", "w") as f:
        json.dump(sorted_by_air_quality, f, indent=4)

    print("Weather data has been written to sorted_weather_data.json")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.terminate()
