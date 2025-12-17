import time
import json
import streamlit as st
import groqqq as groq
import os
import csv

USERS_FILE = "users.csv"

# ---------- FILE SETUP ----------
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "chat", "project_chats"])

# ---------- USERS CSV ----------
def load_users():
    users = {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # safe load chat & project_chats
            chat = json.loads(row["chat"]) if "chat" in row and row["chat"] else []
            project_chats = json.loads(row["project_chats"]) if "project_chats" in row and row["project_chats"] else []
            users[row["username"]] = {
                "password": row["password"],
                "chat": chat,
                "project_chats": project_chats
            }
    return users

def save_users(users):
    # ensure CSV has all columns
    with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password", "chat", "project_chats"])
        for u, data in users.items():
            chat = json.dumps(data.get("chat", []))
            project_chats = json.dumps(data.get("project_chats", []))
            writer.writerow([u, data["password"], chat, project_chats])

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "users" not in st.session_state:
    st.session_state.users = load_users()
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "active_project_chat" not in st.session_state:
    st.session_state.active_project_chat = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "project_chats" not in st.session_state:
    st.session_state.project_chats = []

# ---------- AUTH ----------
def register():
    with st.form("registration_form"):
        new_username = st.text_input("Choose a username")
        new_password = st.text_input("Choose a password", type="password")
        confirm_password = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            users = load_users()
            if new_username in users:
                st.error("Username already exists.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif not new_username or not new_password:
                st.error("Fields cannot be empty.")
            else:
                users[new_username] = {"password": new_password, "chat": [], "project_chats": []}
                save_users(users)
                st.session_state.users = users
                st.success("Registration successful! Please login.")
                st.session_state.page = "login"
                st.rerun()

def log_in(username):
    st.session_state.current_user = username
    st.session_state.logged_in = True
    st.session_state.messages = st.session_state.users[username].get("chat", [])
    st.session_state.project_chats = st.session_state.users[username].get("project_chats", [])
    st.session_state.chat_history = []  # previous session snapshots (optional)
    st.session_state.page = "chat"
    st.rerun()

def log_out():
    users = st.session_state.users
    users[st.session_state.current_user]["chat"] = st.session_state.messages
    users[st.session_state.current_user]["project_chats"] = st.session_state.project_chats
    save_users(users)
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.project_chats = []
    st.session_state.page = "login"
    st.rerun()

def delete_account():
    users = st.session_state.users
    if st.session_state.current_user in users:
        del users[st.session_state.current_user]
        save_users(users)
    log_out()

def back_to_chat():
    st.session_state.page = "chat"
    st.rerun()

def clear_history():
    st.session_state.messages.clear()
    users = st.session_state.users
    users[st.session_state.current_user]["chat"] = []
    save_users(users)
    st.success("Chat history cleared!")

# ---------- PROFILE ----------
def open_profile():
    st.header("Your Profile")
    st.markdown(
        f"""
        <div style="background-color:#0F172A;padding:20px;border-radius:12px;">
            <div style="background-color:#f0f2f6;border-radius:10px;padding:20px;">
                <b>Name:</b> {st.session_state.current_user}<br>
                <b>Status:</b> Active
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("⬅️ Back to Chat", use_container_width=True):
        back_to_chat()
    if st.button("🗑️ Delete Chat History", use_container_width=True):
        clear_history()
    if st.button("🚪 Log Out", use_container_width=True):
        log_out()
    if st.button("🗑️ Delete Account", use_container_width=True):
        delete_account()

def open_project():
    st.header("📂 Project Page")
    with st.spinner("Saving project chat..."):
        time.sleep(1)
    st.success("Project saved successfully!")
    back_to_chat()

# ---------- SIDEBAR ----------
if st.session_state.logged_in:
    with st.sidebar:
        if st.button("➕ New chat", use_container_width=True):
            if st.session_state.messages:
                st.session_state.chat_history.append(st.session_state.messages.copy())
            st.session_state.messages.clear()
            back_to_chat()
        st.button("🔍 Search chat", use_container_width=True)
        if st.button("📔 Project chat", use_container_width=True):
            st.session_state.page = "project_chat"
            st.rerun()
        if st.button("📂 Project", use_container_width=True):
            if st.session_state.messages:
                st.session_state.project_chats.append(st.session_state.messages.copy())
                st.session_state.messages.clear()
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
                    back_to_chat()
        if st.button("🙍 PROFILE", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

# ---------- UI ----------
st.markdown("<h2 style='padding-left:20px;'>Chat Bot</h2>", unsafe_allow_html=True)

if st.session_state.page == "login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username]["password"] == password:
            st.session_state.users = users
            log_in(username)
        else:
            st.error("Invalid username or password")
    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()
    st.stop()

if st.session_state.page == "register":
    st.title("📝 Register")
    register()
    st.stop()

if st.session_state.page == "chat":
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message("human" if i % 2 == 0 else "ai"):
            st.write(msg)
    user_msg = st.chat_input("Type your message here...")
    file = st.file_uploader("Upload your file (optional)")
    if user_msg:
        prompt = user_msg
        if file:
            prompt += "\n\n" + file.read().decode(errors="ignore")
        st.session_state.messages.append(prompt)
        reply = groq.get_groq_response(prompt)
        st.session_state.messages.append(reply)
        # save chat to CSV
        users = st.session_state.users
        users[st.session_state.current_user]["chat"] = st.session_state.messages
        save_users(users)
        st.rerun()

elif st.session_state.page == "project_chat":
    st.header("📔 Project Chats")
    if not st.session_state.project_chats:
        st.info("No project chats yet")
    else:
        for i, chat in enumerate(st.session_state.project_chats):
            if st.button(f"Open Project Chat {i+1}"):
                st.session_state.messages = chat.copy()
                back_to_chat()
elif st.session_state.page == "profile":
    open_profile()
elif st.session_state.page == "project":
    open_project()
