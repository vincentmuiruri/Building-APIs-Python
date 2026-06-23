# import requests

# API_KEY = "53622f0f124134700025b1dc334768b6"
# city = "Nairobi"

# try:
#     response = requests.get(
#         "http://api.openweathermap.org/data/2.5/weather",
#         params={
#             "q": city,
#             "appid": API_KEY,
#             "units": "metric"  # Use "imperial" for Fahrenheit
#     }
#     )

#     if response.status_code == 200:
#         data = response.json()
#         temp = data["main"]["temp"]
#         weather_description = data["weather"][0]["description"]
#         print(f"{city}: {temp}°C, {weather_description}")

#     else:
#         print("Failed to get weather data.")

# except requests.exceptions.Timeout:
#     print("The request timed out.")

# except requests.exceptions.HTTPError as e:
#     print(f"HTTP error: {e.response.status_code} - {e.response.text}")

# except requests.exceptions.ConnectionError:
#     print("Could not connect to the server.")

# except requests.exceptions.RequestException as e:
#     print(f"An error occurred: {e}")


import argparse
import os
import sys
from datetime import datetime

import requests


def format_weather(data: dict, city: str, units: str) -> str:
    temp = data["main"]["temp"]
    feels_like = data["main"].get("feels_like")
    humidity = data["main"]["humidity"]
    weather_description = data["weather"][0]["description"].capitalize()
    wind_speed = data["wind"]["speed"]
    unit_symbol = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
    return (
        f"🌍 Weather for {city}\n"
        f"📍 Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"🌡️ Temperature: {temp}{unit_symbol}"
        + (f" (feels like {feels_like}{unit_symbol})" if feels_like is not None else "")
        + "\n"
        f"💧 Humidity: {humidity}%\n"
        f"🌤️ Conditions: {weather_description}\n"
        f"💨 Wind Speed: {wind_speed} m/s"
    )


def get_weather(city: str, api_key: str, units: str, timeout: int = 10) -> dict:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }
    response = requests.get(url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch current weather from OpenWeatherMap.")
    parser.add_argument("city", nargs="?", default="Nairobi", help="City name to fetch weather for")
    parser.add_argument("--apikey", help="OpenWeatherMap API key. Falls back to OPENWEATHER_API_KEY env variable.")
    parser.add_argument("--units", choices=["metric", "imperial", "standard"], default="metric", help="Units for temperature")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = args.apikey or os.environ.get("OPENWEATHER_API_KEY")

    if not api_key:
        print("❌ Please set OPENWEATHER_API_KEY environment variable or pass --apikey.")
        return 1

    try:
        data = get_weather(args.city, api_key, args.units)
        print(format_weather(data, args.city, args.units))
        return 0

    except requests.exceptions.Timeout:
        print("⏰ The request timed out. Please check your internet connection.")
        return 1

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status == 401:
            print("🔑 Invalid API key. Please check your OpenWeatherMap API key.")
        elif status == 404:
            print(f"❌ City '{args.city}' not found. Please check the spelling.")
        else:
            message = e.response.text if e.response is not None else str(e)
            print(f"❌ HTTP error: {status} - {message}")
        return 1

    except requests.exceptions.ConnectionError:
        print("🔌 Could not connect to the server. Please check your internet connection.")
        return 1

    except requests.exceptions.RequestException as e:
        print(f"⚠️ An error occurred: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())