import streamlit as st
import requests
from secret import api_key  


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "logout" not in st.session_state:
    st.session_state.logout = False

if not st.session_state.logged_in and not st.session_state.logout:
    st.title("Login Page")
        

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == password and username != "":
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Invalid username or password")

elif st.session_state.logged_in:
    

    st.title("Weather App 🌤")

    city = st.text_input("Enter City Name")
    se = api_key
    if st.button("Get Weather"):
        if city != "":
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={se}&units=metric"

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                st.subheader(f"Weather in {city}")
                st.write("🌡 Temperature:", data["main"]["temp"], "°C")
                st.write("☁ Condition:", data["weather"][0]["description"])
                st.write("💧 Humidity:", data["main"]["humidity"], "%")
            else:
                st.error("City not found")
        else:
            st.warning("Please enter a city name")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.logout = True

else:
    st.title("Thank You 🙏")
    st.write("Thanks for using the Weather App")