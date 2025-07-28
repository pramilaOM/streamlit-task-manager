# Enhanced Streamlit Task Manager with Priority, PDF/Excel Export, and Reminders
import streamlit as st
import os
import datetime
import hashlib
import json
import pandas as pd
from fpdf import FPDF

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="Task Manager", layout="centered")

# ------------------- THEME TOGGLE -------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

theme = st.sidebar.checkbox("🌗 Dark Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = theme

if theme:
    st.markdown("""
        <style>
        /* Base background and font */
        body, .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #16191f !important;
        }

        /* Headings and text */
        h1, h2, h3, h4, h5, h6, label, p, span, div {
            color: #e0e0e0 !important;
        }

        /* Inputs */
        input, textarea, select {
            background-color: #1c1e26 !important;
            color: #ffffff !important;
            border: 1px solid #444 !important;
        }

        /* Buttons */
        button {
            background-color: #333 !important;
            color: #ffffff !important;
            border: 1px solid #555 !important;
            padding: 0.5em 1em;
            border-radius: 6px;
        }

        button:disabled {
            background-color: #444 !important;
            color: #888 !important;
        }

        button:hover {
            background-color: #555 !important;
            color: #ffffff !important;
        }

        /* Radio & selectbox container */
        div[data-baseweb="radio"], div[data-baseweb="select"] {
            background-color: #1c1e26 !important;
            color: #fff !important;
        }

        /* Metrics */
        .stMetric {
            background-color: #1a1d23 !important;
            color: #fafafa !important;
            border-radius: 8px;
            padding: 10px;
        }

        /* Alert messages */
        .stAlert {
            background-color: #1a1d23 !important;
            border-left: 5px solid #4caf50;
            color: #eeeeee !important;
        }

        /* Form layout spacing */
        .stForm {
            background-color: #181a20;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #333;
        }

        /* Export buttons */
        .stButton>button {
            margin-top: 8px;
            background-color: #2c2f36 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------------- PASSWORD HASHING -------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------- USER PROFILE FILE -------------------
def get_profile_file(username):
    return f"{username}_profile.txt"

# ------------------- JSON TASK FILE -------------------
def get_task_file(username):
    return f"{username}_tasks.json"

def load_tasks(username):
    file = get_task_file(username)
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_tasks(username, tasks):
    file = get_task_file(username)
    with open(file, "w") as f:
        json.dump(tasks, f, indent=4)

# ------------------- EXPORT TO PDF -------------------
def export_to_pdf(username, tasks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Task Report for {username}", ln=True, align="C")
    pdf.ln(10)
    for i, t in enumerate(tasks, 1):
        pdf.cell(200, 10, txt=f"{i}. {t['desc']} | Due: {t['deadline']} | Status: {t['status']} | Priority: {t['priority']} | Tag: {t['tag']}", ln=True)
    pdf.output(f"{username}_tasks.pdf")
    return f"{username}_tasks.pdf"

# ------------------- EXPORT TO EXCEL -------------------
def export_to_excel(username, tasks):
    df = pd.DataFrame(tasks)
    file_path = f"{username}_tasks.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

# ------------------- LOGOUT -------------------
if "username" in st.session_state:
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

# ------------------- HEADER -------------------
st.title("📝 Personalized Task Manager")

# ------------------- MENU -------------------
menu = ["Login", "Sign Up"]
if "username" not in st.session_state:
    choice = st.sidebar.selectbox("Menu", menu)
else:
    choice = None

# ------------------- SIGN UP -------------------
if choice == "Sign Up":
    st.subheader("Create Account")
    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type="password")

    if st.button("Sign Up"):
        if new_user and new_pass:
            with open(get_profile_file(new_user), "w") as f:
                f.write(hash_password(new_pass) + "\n")
            st.success("Account created! You can now log in.")
        else:
            st.warning("Please enter both username and password.")

# ------------------- LOGIN -------------------
if choice == "Login":
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            with open(get_profile_file(username), "r") as f:
                saved_password = f.readline().strip()
                if hash_password(password) == saved_password:
                    st.success(f"Welcome {username}!")
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Incorrect password.")
        except FileNotFoundError:
            st.warning("Username not found. Please sign up first.")

# ------------------- TASK MANAGEMENT -------------------
if "username" in st.session_state:
    st.subheader("📋 Task Management")
    task_tab = st.radio("Choose option", ["Add Task", "View Tasks", "Update Task", "Delete Task", "Export Tasks"])

    tasks = load_tasks(st.session_state["username"])

    # ------------------- TASK SUMMARY -------------------
    if tasks:
        st.markdown("### 📊 Task Summary")
        total = len(tasks)
        completed = sum(1 for t in tasks if t["status"] == "Completed")
        ongoing = sum(1 for t in tasks if t["status"] == "Ongoing")
        not_started = total - completed - ongoing

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total", total)
        col2.metric("✅ Completed", completed)
        col3.metric("🚧 Ongoing", ongoing)
        col4.metric("🕓 Not Started", not_started)

    # ------------------- ADD TASK -------------------
    if task_tab == "Add Task":
        with st.form("add_task_form", clear_on_submit=True):
            desc = st.text_input("Task description")
            deadline = st.date_input("Deadline", min_value=datetime.date.today())
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            tag = st.text_input("Tag/Category (optional)")
            submitted = st.form_submit_button("Add Task")

            if submitted:
                if desc:
                    tasks.append({
                        "desc": desc,
                        "deadline": str(deadline),
                        "status": "Not Started",
                        "priority": priority,
                        "tag": tag
                    })
                    save_tasks(st.session_state["username"], tasks)
                    st.success("Task added!")
                else:
                    st.warning("Task description cannot be empty.")

    # ------------------- VIEW TASKS -------------------
    elif task_tab == "View Tasks":
        st.subheader("📄 Your Tasks")
        today = datetime.date.today()
        if tasks:
            for i, t in enumerate(tasks):
                deadline = datetime.date.fromisoformat(t["deadline"])
                overdue = deadline < today and t["status"] != "Completed"
                st.markdown(f"**{i+1}. {t['desc']}** - Due: {t['deadline']} - Status: `{t['status']}` - Priority: `{t['priority']}` - Tag: `{t['tag']}`")
                if overdue:
                    st.warning("⏰ This task is overdue!")
        else:
            st.info("No tasks yet.")

    # ------------------- UPDATE TASK -------------------
    elif task_tab == "Update Task":
        if tasks:
            task_index = st.selectbox("Select task to update", range(len(tasks)), format_func=lambda i: tasks[i]["desc"])
            new_status = st.selectbox("New status", ["Not Started", "Ongoing", "Completed"])
            if st.button("Update Status"):
                tasks[task_index]["status"] = new_status
                save_tasks(st.session_state["username"], tasks)
                st.success("Task status updated.")
        else:
            st.warning("No tasks to update.")

    # ------------------- DELETE TASK -------------------
    elif task_tab == "Delete Task":
        if tasks:
            task_index = st.selectbox("Select task to delete", range(len(tasks)), format_func=lambda i: tasks[i]["desc"])
            if st.button("Delete Task"):
                deleted = tasks.pop(task_index)
                save_tasks(st.session_state["username"], tasks)
                st.success(f"Deleted: {deleted['desc']}")
        else:
            st.warning("No tasks to delete.")

    # ------------------- EXPORT TASKS -------------------
    elif task_tab == "Export Tasks":
        st.subheader("📁 Export Options")
        if tasks:
            if st.button("Export to PDF"):
                pdf_path = export_to_pdf(st.session_state["username"], tasks)
                st.success(f"PDF exported successfully: {pdf_path}")

            if st.button("Export to Excel"):
                excel_path = export_to_excel(st.session_state["username"], tasks)
                st.success(f"Excel exported successfully: {excel_path}")
        else:
            st.info("No tasks to export.")
