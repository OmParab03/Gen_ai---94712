from langchain_openai import ChatOpenAI
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api = os.getenv("weather_api")
city = input("Enter city name: ")
print(api)
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"
response = requests.get(url)
data = response.json()

if response.status_code != 200 or "main" not in data:
    print("Weather API error:")
    print(data)
    exit()

print("Weather API connected ✅")

temp = data["main"]["temp"]
description = data["weather"][0]["description"]
humidity = data["main"]["humidity"]


llm2 = ChatOpenAI(
    base_url="http://127.0.0.1:1234/v1",
    model="google/gemma-3n-e4b",
    api_key="dummy_api"
)

prompt = f"""Generate summary in few lines in english using this weather of given city, data:"
    City: {city}"
    Temperature: {temp}°C"
    Weather: {description}"
    Humidity: {humidity}%"
"""

resp = llm2.invoke(prompt)
print("\nWeather Summary:\n")
print(resp.content)
