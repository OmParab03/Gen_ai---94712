import streamlit as st
import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

st.set_page_config(page_title="Weather Summary", layout="centered")
st.title("🌤️ Weather Summary App")
st.write("Enter a city name to fetch live weather data and generate an AI summary.")

api_key = os.getenv("weather_api")

if not api_key:
    st.error("Weather API key not found. Please set weather_api in .env")
    st.stop()


city = st.chat_input("Enter city name")

if city:
    with st.spinner("Fetching weather data..."):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

    if response.status_code != 200 or "main" not in data:
        st.error("Weather API error")
        st.json(data)
        st.stop()

    st.success("Weather API connected ✅")

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    st.subheader("🌍 Current Weather (●'◡'●)")
    col0,col1, col2, col3 = st.columns(4)
    col0.metric("city",f"{city.upper()}")
    col1.metric("Temperature", f"{temp} °C")
    col2.metric("Condition", description.title())
    col3.metric("Humidity", f"{humidity} %")

    llm = ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        model="qwen/qwen3-8b",
        api_key="dummy_api"
    )

    prompt = f"""
    Generate a short weather summary in English (2–3 lines).

    City: {city}
    Temperature: {temp}°C
    Weather: {description}
    Humidity: {humidity}%
    """

    st.subheader("🧠 AI Weather Summary")
    summary_box = st.empty()
    summary_text = ""

    for chunk in llm.stream(prompt):
        if chunk.content:
            summary_text += chunk.content
            summary_box.markdown(summary_text)
else:
    st.info("Type a city name and press Enter")
