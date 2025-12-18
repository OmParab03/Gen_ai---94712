from langchain.chat_models import init_chat_model
import os
import streamlit as st
st.title("history-Based Chat-Bot")
llm = init_chat_model(
    model = "llama-3.3-70b-versatile",
    model_provider = "openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("groq_api")
)
if "conversation" not in st.session_state:
    st.session_state.conversation=[]

with st.sidebar:
    value=st.slider("give value for history-apporach",2,5,3,1)
prompt=st.chat_input("ask anything.. : ")    
if prompt:
   st.session_state.conversation.append(
    {"role": "user","content":prompt}) 
   history=st.session_state.conversation[-value:]
   with st.spinner("getting reply.."):
        result=llm.stream(history)
        
        def stream_create(result):
            full_reply=""
            for chunk in result:
                if chunk.content:
                    full_reply+=chunk.content
                    yield chunk.content
                    st.session_state.conversation.append(
                    {"role": "assistant","content":full_reply})
            
        
                    
        st.write_stream(stream_create(result))        
                
        
   










    
