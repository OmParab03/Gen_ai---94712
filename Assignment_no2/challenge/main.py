import grok
import weather

print(f"City Weather : ","\n",weather.get_weather_data(weather.data))
print("Answer : ","\n",grok.get_response(grok.text))