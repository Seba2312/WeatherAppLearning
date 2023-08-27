import json
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

# Initialize the Wolfram Language session
session = WolframLanguageSession()

try:
    # Fetch all countries
    all_countries = session.evaluate(wl.EntityList("Country"))

    # Initialize an empty dictionary to store country names, their populations, and ratings
    country_data = {}

    # Extract and store the country names, populations, and ratings
    for country in all_countries:
        country_name = session.evaluate(wl.CommonName(country))
        population_quantity = session.evaluate(wl.EntityValue(country, 'Population'))

        # Check if population is available
        if population_quantity != wl.Missing('NotAvailable'):
            # Extract the numerical part of the population
            population = session.evaluate(wl.QuantityMagnitude(population_quantity))

            # Assign ratings based on population ranges
            rating = 1  # Default rating for countries with unusual populations
            if 1_000_000 <= population < 5_000_000:
                rating = 3
            elif 5_000_000 <= population < 20_000_000:
                rating = 7
            elif 20_000_000 <= population < 50_000_000:
                rating = 10
            elif 50_000_000 <= population < 100_000_000:
                rating = 20
            elif 100_000_000 <= population <= 2_000_000_000:
                rating = 30

            # Remove spaces from country_name for Wolfram Language expression
            country_name_no_space = country_name.replace(" ", "")

            country_data[country_name] = {
                "population": population,
                "rating": rating
            }

    # Filter out countries with populations less than 5 million
    filtered_countries = {k: v for k, v in country_data.items() if v['population'] > 5_000_000}

    # Initialize a list to store cities
    all_cities = []

    # Call the city function for each country and add cities based on weight
    for country_name, data in filtered_countries.items():
        country_weight = data['rating']
        country_name_no_space = country_name.replace(" ", "")  # Remove spaces
        country_expression = wlexpr(f'EntityList[EntityClass["City", "Country" -> Entity["Country", "{country_name_no_space}"]]]')
        country_cities = session.evaluate(country_expression)
        weighted_cities = country_cities[:country_weight]
        all_cities.extend(weighted_cities)

    # Convert the list of city entities to a list of city names
    city_names = [session.evaluate(wl.CommonName(city)) for city in all_cities]

    # Filter out names that contain "CommonName"
    filtered_city_names = [city for city in city_names if "CommonName" not in str(city)]

    # Print the city names
    print("Cities based on assigned weight:")
    for i, city in enumerate(filtered_city_names):
        print(f"{i + 1}. {city}")

    # Create a JSON file to store the list of cities
    with open('cities.json', 'w') as json_file:
        json.dump(filtered_city_names, json_file, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the session
    session.terminate()
