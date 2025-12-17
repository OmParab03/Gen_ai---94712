import streamlit as st
import chat_bot as cb
import chat_bot_local as cbl

if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_messages():
    st.session_state.messages = []

choices = ["llama-3.1-8b-instant", "Phi 4 Mini Reasoning"]
with st.sidebar:
    st.title("Options")
    choice = st.selectbox("Choose Model", choices)
    if st.button("➕ New Chat"):
        clear_messages()

st.title("Multi-Model Chat Bot")
prompt = st.chat_input("Ask anything...")


if prompt is not None and prompt.strip() != "":
    prompt_text = prompt.strip()

   
    st.session_state.messages.append({
        "role": "user",
        "content": prompt_text
    })

    
    if choice == "Phi 4 Mini Reasoning":
        reply = cbl.local_chat_bot(prompt=prompt_text, history=st.session_state.messages)
    else:
        reply = cb.chat_bot(prompt_text)

    
    if reply is None or reply.strip() == "":
        reply = "❌ Model returned no response"

   
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

for msg in st.session_state.messages:
    if not isinstance(msg, dict) or "role" not in msg or "content" not in msg:
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
