import requests
import secrets


def get_weather_data(data):
    source=["City:",data["name"],
               "Temperature:",data["main"]["temp"],"°C",
               "humidity:",data["main"]["humidity"],"%",
               "weather:",data["weather"][0]["description"]]
   
    return source

def get_city_name():
    city=str(input("Enter city name: "))
    return city   
   
api=f"{secrets.weather_api}"
url = f"http://api.openweathermap.org/data/2.5/weather?q={get_city_name()}&appid={api}&units=metric"


response=requests.get(url)
data=response.json()


if __name__ == "__main__":
    print(get_weather_data(data))