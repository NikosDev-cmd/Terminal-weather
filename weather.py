import requests

def get_coordinates(city):
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1}  # Limit to one result
    response = requests.get(geo_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and data["results"]:
            result = data["results"][0]
            return result["latitude"], result["longitude"], result["name"], result["country"]
        else:
            print("City not found. Please try another location.")
            return None
    else:
        print("Error retrieving coordinates.")
        return None

def get_weather(latitude, longitude):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }
    response = requests.get(weather_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Error retrieving weather data.")
        return None

def display_weather(weather_data, location_info):
    """
    Display the current weather details.
    """
    if "current_weather" in weather_data:
        current = weather_data["current_weather"]
        print(f"\nCurrent weather for {location_info}:")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Wind Speed: {current['windspeed']} km/h")
        print(f"Weather Code: {current['weathercode']} (see Open-Meteo docs for details)")
    else:
        print("No current weather data available.")

def main():
    print("Welcome to the Weather Forecast CLI using Open-Meteo!")
    city = input("Enter the location (city name): ").strip()
    
    coords = get_coordinates(city)
    if coords:
        latitude, longitude, city_name, country = coords
        weather_data = get_weather(latitude, longitude)
        if weather_data:
            location_info = f"{city_name}, {country}"
            display_weather(weather_data, location_info)

if __name__ == "__main__":
    main()
