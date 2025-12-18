from langchain_openai import ChatOpenAI
import streamlit as st 


st.title("Model-chatbot")        
url="http://127.0.0.1:1234/v1"
    
llm= ChatOpenAI (
        base_url=url,
        model="Phi 4 Mini Reasoning",
        api_key="dummy_api"
    )
prompt=st.chat_input("ask anything...")

if prompt:
    with st.spinner("getting reply..."):
        response=llm.stream(prompt)
        def stream_generator():
           for chunk in response:
               if chunk.content:
                  yield chunk.content
    
     
        st.write_stream(stream_generator())
    




   