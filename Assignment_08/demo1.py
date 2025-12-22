from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

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
        return result
    except:
        return "Error can't solve expression."
    
    
llm=init_chat_model(
    model="qwen/qwen3-8b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy_api"
    )
conversation=[]
agent=create_agent(
    model=llm,
    tools=[calculator],
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
    print("result",reply["messages"])
    conversation=reply["messages"]
    
