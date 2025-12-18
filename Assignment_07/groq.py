import os
import streamlit as st 
from langchain.chat_models import init_chat_model

st.title("Chat-Bot")
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)

prompt=st.chat_input("ask anything... ")
if prompt:
    response=llm.stream(prompt)
    st.write_stream([chunk.content for chunk in response])
    
