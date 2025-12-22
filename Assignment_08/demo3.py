from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
# import requests 
# import os

# @tool
# def calculator(expression):
#     """
#     this calculator function is used to solve basic arithmaetic equation's 
#     and it can do calculations using operators eg,+,-,*,/ etc
#     :parameter expression : str  arithmetic expression 
#     :return expression result as str:
#     """
#     try:
#         result=eval(expression)
#         return result
#     except:
#         return "Error can't solve expression."
    
# @tool
# def get_weather(city):
#     """
#     this get_weather function in used to get the present time weather data for given city ,it only gives todays,not yesterday or any past data.
#     if data not get featched then it returns the "ERROR".
#     """
#     try:
       
#        api=os.getenv("weather_api")
#        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api}&units=metric&q={city}"
#        response=requests.get(url=url)
#        ans=response.json()
#        return {
#             "city": city,
#             "temp": ans["main"]["temp"],
#             "humidity": ans["main"]["humidity"],
#             "condition": ans["weather"][0]["description"]
#         }

#     except:
#         return "ERROR to featch data."
@wrap_model_call
def logging(request,handlr):
    print("------------------")
    response=handlr(request)
    print("----------------")
      
    return response
      
@wrap_model_call
def limit_model_context(request, handlr):
    print("before model call................")

    if hasattr(request, "messages"):
        request = request.override(
            messages=request.messages[-5:]
        )

    response = handlr(request)
    print("activated.......")
    return response

    
llm=init_chat_model(
    model="qwen/qwen3-8b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_api"
    )
conversation=[]
agent=create_agent(
    model=llm,
    tools=[
           ],
    middleware=[
        limit_model_context,
        logging
    ],
    system_prompt="You are a helpful ai assistant that gives answer in few lines or if necessary only in one line , if not have answer returns 'ERROR'."
)


while True:
    prompt=input("ask.. :  ")
    if prompt=="exit":
        break
    conversation.append({"role": "user","content":prompt})
    reply=agent.invoke({"messages":conversation})
    
    ai_msg = reply["messages"][-1]
    print("(＾▽＾) ⬇️ ",ai_msg.content)
    conversation=reply["messages"]
