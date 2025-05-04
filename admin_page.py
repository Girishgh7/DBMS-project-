import streamlit as st
import sqlite3
import hashlib
import pandas as pd

# --- DB Setup --- #
conn = sqlite3.connect('bus_booking.db', check_same_thread=False)
c = conn.cursor()

# --- Create Tables if Not Exist --- #
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT UNIQUE NOT NULL,
             password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS bookings (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT NOT NULL,
             bus_type TEXT NOT NULL,
             source TEXT NOT NULL,
             destination TEXT NOT NULL,
             travel_date TEXT NOT NULL,
             seat_no TEXT NOT NULL,
             passenger_name TEXT NOT NULL,
             passenger_id TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# --- Utility Functions --- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
              (username, hash_password(password)))
    return c.fetchone()

# --- Ensure admin account exists --- #
admin_username = "girish"
admin_password = hash_password("1234")
c.execute("SELECT * FROM users WHERE username = ?", (admin_username,))
if not c.fetchone():
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (admin_username, admin_password))
    conn.commit()

# --- Session State --- #
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "user" not in st.session_state:
    st.session_state.user = None

# --- Sidebar Navigation ---
st.sidebar.title("🚌 Blue Bus ADMIN Page")
st.sidebar.markdown("Made by GIRISH, ANN, DAMINI")
page = st.sidebar.radio("Navigate", ["Login",  "Admin Dashboard"])

# --- Login Page --- #
if page == "Login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_login(username, password)
        if user:
            st.session_state.user = user
            st.success("Login successful")
            if username == "girish":
                st.session_state.page = "Admin Dashboard"
            else:
                st.session_state.page = "Book Ticket"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# --- Register Page --- #
elif page == "Register":
    st.title("📝 Register")
    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")
    if st.button("Register"):
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (new_user, hash_password(new_pass)))
            conn.commit()
            st.success("User registered. Please login.")
        except sqlite3.IntegrityError:
            st.error("Username already exists.")

# --- Admin Dashboard --- #
elif page == "Admin Dashboard":
    if not st.session_state.user or st.session_state.user[1] != "girish":
        st.warning("⛔ Access denied. Admins only.")
    else:
        st.title("📋 Admin Dashboard")
        st.subheader("All Bookings")
        c.execute("SELECT * FROM bookings ORDER BY timestamp DESC")
        rows = c.fetchall()
        if not rows:
            st.info("No bookings yet.")
        else:
            df = pd.DataFrame(rows, columns=[col[0] for col in c.description])
            st.dataframe(df, use_container_width=True)


