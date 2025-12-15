import requests
import hide

def get_weather(city):
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
         f"?q={city}&appid={hide.weather_api}&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return {
        "city": data["name"],
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"]
    }
