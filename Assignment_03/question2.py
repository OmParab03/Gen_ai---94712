import time
import streamlit as st
import groq


if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "project_chats" not in st.session_state:
    st.session_state.project_chats = []

if "active_project_chat" not in st.session_state:
    st.session_state.active_project_chat = None

if "page" not in st.session_state:
    st.session_state.page = "chat"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def log_in():
    st.session_state.logged_in = True
    st.session_state.page = "chat"
    st.rerun()

def log_out():
    st.session_state.logged_in = False
    st.session_state.page = "login"
    st.rerun()


def back_to_chat():
    st.session_state.page = "chat"
    st.rerun()

def clear_history():
    st.session_state.chat_history = []
    st.success("Chat history cleared!")

def open_profile():
    st.header("Your Profile")
    st.snow()

    st.markdown(
        """
        <div style="background-color:#0F172A;padding:20px;border-radius:12px;">
            <div style="height:200px;width:100%;background-color:#f0f2f6;
                        border-radius:10px;padding:20px;">
                <div style="height:100px;width:100px;border-radius:50%;
                            background-color:#9ca3af;margin-bottom:10px;"></div>
                <b>Name:</b> User <br>
                <b>Status:</b> Active
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("⬅️ Back to Chat", use_container_width=True):
        back_to_chat()

    if st.button("🗑️ Delete Chat History", use_container_width=True):
        clear_history()
        st.rerun()
    if st.button("🚪 Log Out", use_container_width=True):
       log_out()

        

def open_project():
    st.header("📂 Project Page")
    with st.spinner("Saving project chat..."):
        time.sleep(1)
    st.success("Project saved successfully!")
    st.session_state.page = "chat"
    st.rerun()


with st.sidebar:
    

    if st.button("➕ New chat", use_container_width=True):
        if st.session_state.messages:
            st.session_state.chat_history.append(
                st.session_state.messages.copy()
            )
        st.session_state.messages = []
        st.session_state.page = "chat"
        st.rerun()

    if st.button("🔍 Search chat", use_container_width=True):
        st.info("Coming soon")

    if st.button("📔 Project chat", use_container_width=True):
        st.session_state.page = "project_chat"
        st.rerun()

    if st.button("📂 Project", use_container_width=True):
        if st.session_state.messages:
            st.session_state.project_chats.append(
                st.session_state.messages.copy()
            )
            st.session_state.messages = []
        st.session_state.page = "project"
        st.rerun()

    st.divider()
    st.subheader("🕘 Previous Chats")

    if not st.session_state.chat_history:
        st.caption("No previous chats")
    else:
        for i, chat in enumerate(st.session_state.chat_history):
            if st.button(f"Chat {i+1}", key=f"history_{i}"):
                st.session_state.messages = chat.copy()
                st.session_state.page = "chat"
                st.rerun()
    
    if st.button("🙍 PROFILE", use_container_width=True):
        st.session_state.page = "profile"
        st.rerun()


st.markdown(
    "<h2 style='padding-left:20px;'>Chat Bot</h2>",
    unsafe_allow_html=True
)

if st.session_state.page == "login":

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            log_in()
        else:
            st.error("Please enter credentials")

    st.stop() 
if not st.session_state.logged_in:
    st.session_state.page = "login"
    st.rerun()
 

if st.session_state.page == "chat":

    for idx, message in enumerate(st.session_state.messages):
        role = "human" if idx % 2 == 0 else "ai"
        with st.chat_message(role):
            st.write(message)

    msg = st.chat_input("Type your message here...")
    uploaded_file = st.file_uploader("Upload your file (optional)", type=None)

    if msg:
        final_prompt = msg

        if uploaded_file:
            try:
                file_text = uploaded_file.read().decode("utf-8", errors="ignore")
                final_prompt += f"\n\n[File Content]\n{file_text}"
            except:
                st.warning("Could not read file")

        st.session_state.messages.append(final_prompt)

        reply = groq.get_groq_response(final_prompt)
        st.session_state.messages.append(reply)

        st.rerun()


elif st.session_state.page == "project_chat":
    st.header("📔 Project Chats")

    if not st.session_state.project_chats:
        st.info("No project chats yet")
    else:
        for i, chat in enumerate(st.session_state.project_chats):
            if st.button(f"Open Project Chat {i+1}", key=f"project_{i}"):
                st.session_state.messages = chat.copy()
                st.session_state.active_project_chat = i
                st.session_state.page = "chat"
                st.rerun()

    if st.button("⬅️ Back", use_container_width=True):
        back_to_chat()


elif st.session_state.page == "profile":
    open_profile()


elif st.session_state.page == "project":
    open_project()
