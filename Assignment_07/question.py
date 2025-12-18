from langchain_openai import ChatOpenAI
import pandas as pd
from langchain.chat_models import init_chat_model
import os
import pandasql as ps


      


conversation=[{"role" : "assistant","content":"You are SQLite expert developer with 10 years of experience."}]    
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)
csv=input("enter csv path... : ")
df=pd.read_csv(csv)
print("csv datatypes..")
print(df.dtypes)

while True:
    question=input("ask anything about csv file.")
    if question=="exit":
        break
    llm_input=f"""Table Name: data,
        Table Schema: {df.dtypes}
        Question: {question}
        Instruction:
            Write a SQL query for the above question. 
            Generate SQL query only in plain text format and nothing else.
            If you cannot generate the query, then output 'Error'."""
    result=llm.invoke(llm_input)
    
    query=f"{result.content}"
    print(query)
    ans=ps.sqldf(query,{"data": df})
    content="give me only summary of given data in english in 2,3 sentences, data="
    prompt=ans.to_string(index=False)
    url="http://127.0.0.1:1234/v1"
    
    llm= ChatOpenAI (
            base_url=url,
            model="google/gemma-3-12b",
            api_key="dummy_api"
        )
    prompt=content+prompt
    if prompt:
        response=llm.stream(prompt )
        def stream_generator():
           for chunk in response:
               if chunk.content:
                  yield chunk.content
        for chunk in stream_generator():
            print(chunk,end="",flush=True)
        print()
    
    
    
