import streamlit as st
import httpx
import os
import bcrypt
import json
from dotenv import load_dotenv

load_dotenv()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def get_github_login_url():
    return f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&scope=user:email"

def get_github_user(code):
    token_res = httpx.post(
        "https://github.com/login/oauth/access_token",
        data={"client_id": GITHUB_CLIENT_ID, "client_secret": GITHUB_CLIENT_SECRET, "code": code},
        headers={"Accept": "application/json"}
    )
    token = token_res.json().get("access_token")
    if not token:
        return None
    user_res = httpx.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}
    )
    return user_res.json()

def login_page():
    st.title("📄 AI PDF Chat")
    st.markdown("*Smart document analysis powered by AI*")
    st.divider()

    params = st.query_params
    if "code" in params:
        with st.spinner("Logging in with GitHub..."):
            github_user = get_github_user(params["code"])
            if github_user and "login" in github_user:
                st.session_state.logged_in = True
                st.session_state.username = github_user["login"]
                st.session_state.avatar = github_user.get("avatar_url", "")
                st.query_params.clear()
                st.rerun()
            else:
                st.error("❌ GitHub login failed!")
                st.query_params.clear()

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        st.subheader("Welcome Back!")
        github_url = get_github_login_url()
        st.link_button("🐙 Continue with GitHub", github_url, use_container_width=True)
        st.markdown("**── or use username/password ──**")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True, type="primary"):
            users = load_users()
            if username in users and check_password(password, users[username]["password"]):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.avatar = ""
                st.rerun()
            else:
                st.error("❌ Wrong username or password!")

    with tab2:
        st.subheader("Create Account")
        new_username = st.text_input("Username", key="reg_user")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        if st.button("Register", use_container_width=True, type="primary"):
            if not new_username or not new_password:
                st.error("❌ Please fill all fields!")
            elif new_password != confirm_password:
                st.error("❌ Passwords don't match!")
            elif len(new_password) < 6:
                st.error("❌ Password must be at least 6 characters!")
            else:
                users = load_users()
                if new_username in users:
                    st.error("❌ Username already exists!")
                else:
                    users[new_username] = {"password": hash_password(new_password), "email": new_email}
                    save_users(users)
                    st.success("✅ Account created! Please login.")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.avatar = ""
    st.session_state.messages = []
    st.session_state.chain = None
    st.session_state.pdf_names = []
    st.rerun()
