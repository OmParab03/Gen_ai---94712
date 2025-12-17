import requests
from challenge import secrets
api=f"{secrets.weather_api}"

city="Mumbai"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"


response=requests.get(url)
data=response.json()

print("City:",data["name"])
print("Temperature:",data["main"]["temp"],"°C"
       " |  humidity:",data["main"]["humidity"],"%"
       " |  weather:",data["weather"][0]["description"])

