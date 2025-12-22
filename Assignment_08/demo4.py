from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
import requests 
import os
import json

commands_file="commands.txt"


@tool
def calculator(expression):
    """
    this calculator function is used to solve basic arithmaetic equation's 
    and it can do calculations using operators eg,+,-,*,/ etc
    :parameter expression : str  arithmetic expression 
    :return expression result as str:
    """
    try:
        result=eval(expression)
        return str(result)
    except:
        return "Error can't solve expression."
    
@tool
def get_weather(city):
    """_summary_: this get_weather function is used to get the present weather of given city.  

    Args:
        city (_type_): get the str city name.

    Returns:
        _type_: it returns the temprature in str.
    """
    try:
        api = os.getenv("weather_api")
        if not api:
            return "ERROR: API key missing"

        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api}&units=metric&q={city}"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return "ERROR"

        return json.dumps({
            "city": city,
            "temp": data["main"]["temp"],
            "weather": data["weather"][0]["description"]
        })
    except Exception as e:
        return "ERROR"

    
@tool
def automation_for_every(search: str, mode: str = "youtube") -> str:
    """
    Sends an automation command by writing into a shared command file.
    
    mode:
    - "youtube": play a YouTube video
    - "google": search on Google Chrome
    """
    if mode == "youtube":
        command = f"PLAY::{search}"
    elif mode == "google":
        command = f"SEARCH::{search}"
    else:
        return "Invalid mode. Use 'youtube' or 'google'."

    with open(commands_file, "a") as f:
        f.write(command + "\n")

    return f"Automation command sent: {command}"

llm=init_chat_model(
    model="qwen/qwen3-8b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_api"
    )
conversation=[]
agent=create_agent(
    model=llm,
    tools=[calculator,
           get_weather,
           automation_for_every,
           ],
    system_prompt="You are a helpful ai assistant that gives answer in few lines or if necessary only in one line , if not have answer returns 'ERROR'."
)


while True:
    prompt=input("ask.. :  ")
    if prompt=="exit":
        break
    conversation.append({"role": "user","content":prompt})
    conversation=conversation[-6:]
    reply=agent.invoke({"messages":conversation})
    
    ai_msg = reply["messages"][-1]
    print("(＾▽＾) ⬇️ ",ai_msg.content)
    conversation=reply["messages"]
