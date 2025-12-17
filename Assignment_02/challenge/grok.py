import requests
import weather
import secrets

def get_response(text):
    return text["choices"][0]["message"]["content"]

url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {secrets.grok_api}",
    "Content-Type": "application/json"
}

d1 = weather.get_weather_data(weather.data)

data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": (
                f"Here is today's weather data: {d1}. "
                "Summarize it and give me advice for a picnic plan today."
            )
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
text = response.json()

if __name__ == "__main__":
    print(get_response(text))
