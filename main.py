import requests
import matplotlib.pyplot as plt
import sys

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key.
# You can get one by signing up at https://openweathermap.org/api
API_KEY = '03910e557ff4c75d4cce224412772d0c'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather_data(city_name, api_key):
    """
    Fetches current weather data for a given city from OpenWeatherMap API.

    Args:
        city_name (str): The name of the city.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: A dictionary containing weather data if successful, None otherwise.
    """
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # Use 'metric' for Celsius, 'imperial' for Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return None
    except ValueError as json_err:
        print(f"Error decoding JSON response: {json_err}")
        print(f"Response text: {response.text}")
        return None

def visualize_weather_data(weather_data, city_name):
    """
    Visualizes current weather data using Matplotlib.

    Args:
        weather_data (dict): A dictionary containing parsed weather data.
        city_name (str): The name of the city for the plot title.
    """
    if not weather_data:
        print("No weather data to visualize.")
        return

    try:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed'] # in m/s if units='metric'

        # Prepare data for plotting
        categories = ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)']
        values = [temperature, humidity, wind_speed]
        colors = ['skyblue', 'lightcoral', 'lightgreen']

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(categories, values, color=colors)

        # Add labels and title
        ax.set_ylabel('Value')
        ax.set_title(f'Current Weather in {city_name}')
        ax.set_ylim(0, max(values) * 1.2) # Set y-axis limit for better visualization

        # Add value labels on top of bars
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2),
                    ha='center', va='bottom')

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() # Adjust layout to prevent labels from overlapping
        plt.show()

    except KeyError as e:
        print(f"Error: Missing key in weather data: {e}. Please check the API response structure.")
    except Exception as e:
        print(f"An unexpected error occurred during visualization: {e}")

if __name__ == "__main__":
    if API_KEY == 'YOUR_API_KEY':
        print("ERROR: Please replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key.")
        print("You can get one from https://openweathermap.org/api")
        sys.exit(1) # Exit the script if API key is not set

    # --- Main execution ---
    city = input("Enter the city name (e.g., London, New York, Tokyo): ")
    if not city:
        print("City name cannot be empty. Exiting.")
        sys.exit(1)

    print(f"Fetching weather data for {city}...")
    weather_data = get_weather_data(city, API_KEY)

    if weather_data:
        print("\n--- Weather Data Fetched ---")
        print(f"City: {weather_data.get('name')}")
        print(f"Temperature: {weather_data['main']['temp']} °C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s")
        print(f"Description: {weather_data['weather'][0]['description'].capitalize()}")

        print("\n--- Generating Visualization ---")
        visualize_weather_data(weather_data, city)
    else:
        print(f"Could not retrieve weather data for {city}. Please check the city name and your API key.")

