import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import pandas as pd

# --- PAGE SETUP --- #
st.set_page_config(page_title="Blue Bus", layout="wide")

# --- DATABASE SETUP --- #
conn = sqlite3.connect("bus_booking.db", check_same_thread=False)
c = conn.cursor()

# --Create user table-- #
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Create bookings table
c.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    email TEXT,
    phone TEXT,
    source TEXT,
    destination TEXT,
    journey_date TEXT,
    bus_name TEXT,
    bus_type TEXT,
    seats TEXT,
    total_fare INTEGER,
    timestamp TEXT
)
''')
conn.commit()

# --- UTILITY FUNCTIONS --- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    if username == "girish" and password == "1234":
        return ("girish", "admin")
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
              (username, hash_password(password)))
    return c.fetchone()

def register_user(username, password):
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def generate_seats(rows, cols):
    return [{'seat': f"{chr(65 + r)}{c+1}", 'booked': False} for r in range(rows) for c in range(cols)]

# --- SESSION STATE DEFAULTS ---
for key in ['stage', 'selected_bus', 'selected_seats', 'passenger_details', 'journey_info', 'user', 'page']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'stage' else 'search'

# --- SIDEBAR NAVIGATION --- ##
st.sidebar.title("🧭 Navigation")
page = st.sidebar.selectbox("Choose Page", ["Login", "Register", "Book Ticket", "Admin Dashboard", "Logout"])
st.caption("Made by: Girish , Damini , Ann")
st.session_state.page = page

# --- LOGIN PAGE ---
if page == "Login":
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = check_login(username, password)
        if user:
            st.session_state.user = user
            st.success("Login successful")
            if user[1] == "admin":
                st.session_state.page = "Admin Dashboard"
            else:
                st.session_state.page = "Book Ticket"
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

# --- REGISTER PAGE ---
elif page == "Register":
    st.title("📝 Register")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Register"):
        if username.lower() == "admin" or username.lower() == "girish":
            st.error("Username is reserved.")
        elif register_user(username, password):
            st.success("User registered successfully. Please login.")
        else:
            st.error("Username already exists.")

# --- LOGOUT --- #
elif page == "Logout":
    st.session_state.user = None
    for key in ['stage', 'selected_bus', 'selected_seats', 'journey_info']:
        st.session_state[key] = None if key != 'stage' else 'search'
    st.success("You have been logged out.")
    st.session_state.page = "Login"
    st.rerun()

# --- ADMIN DASHBOARD --- #
elif page == "Admin Dashboard":
    if not st.session_state.user or st.session_state.user[0] != "girish":
        st.warning("⛔ Access denied. Admins only.")
    else:
        st.title("📋 Admin Dashboard")
        c.execute("SELECT * FROM bookings ORDER BY timestamp DESC")
        rows = c.fetchall()
        if not rows:
            st.info("No bookings yet.")
        else:
            df = pd.DataFrame(rows, columns=[col[0] for col in c.description])
            st.dataframe(df, use_container_width=True)

# --- BOOKING FLOW --- #
elif page == "Book Ticket":
    if not st.session_state.user or st.session_state.user[1] == "admin":
        st.warning("Please log in with a user account to book tickets.")
    else:
        locations = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad']
        buses_data = [
            {'Bus Name': 'Royal Express', 'Type': 'AC Sleeper', 'Rows': 5, 'Cols': 6, 'Fare': 1200},
            {'Bus Name': 'Urban Connect', 'Type': 'Non-AC Seater', 'Rows': 3, 'Cols': 7, 'Fare': 700},
            {'Bus Name': 'Elite Ride', 'Type': 'AC Volvo', 'Rows': 2, 'Cols': 8, 'Fare': 1600},
        ]

        if st.session_state.stage == 'search':
            st.title("🚌 Book Your Bus 💺")
            col1, col2, col3 = st.columns(3)
            with col1:
                source = st.selectbox("From", locations)
            with col2:
                destination = st.selectbox("To", [loc for loc in locations if loc != source])
            with col3:
                journey_date = st.date_input("Journey Date", min_value=datetime.today())
            if st.button("🔍 Search Buses"):
                st.session_state.journey_info = {
                    'from': source,
                    'to': destination,
                    'date': str(journey_date)
                }
                st.session_state.stage = 'select_bus'
                st.rerun()

        elif st.session_state.stage == 'select_bus':
            st.header("Select a Bus")
            for idx, bus in enumerate(buses_data):
                with st.container():
                    col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
                    col1.markdown(f"**{bus['Bus Name']}** ({bus['Type']})")
                    col2.markdown(f"Seats: {bus['Rows']} x {bus['Cols']} = {bus['Rows'] * bus['Cols']}")
                    col3.markdown(f"Fare: ₹{bus['Fare']}")
                    if col4.button("Select", key=f"bus_select_{idx}"):
                        bus['SeatsLayout'] = generate_seats(bus['Rows'], bus['Cols'])
                        st.session_state.selected_bus = bus
                        st.session_state.selected_seats = []
                        st.session_state.stage = 'select_seats'
                        st.rerun()

        elif st.session_state.stage == 'select_seats':
            st.header("Choose Seats 💺")
            bus = st.session_state.selected_bus
            seats = bus['SeatsLayout']
            cols = st.columns(bus['Cols'])

            for seat in seats:
                idx = int(seat['seat'][1:]) - 1
                col = cols[idx % bus['Cols']]
                selected = seat['seat'] in st.session_state.selected_seats
                if col.button(f"{seat['seat']} {'✅' if selected else ''}", key=f"seat_{seat['seat']}"):
                    if selected:
                        st.session_state.selected_seats.remove(seat['seat'])
                    else:
                        st.session_state.selected_seats.append(seat['seat'])

            st.markdown(f"Selected Seats: **{', '.join(st.session_state.selected_seats)}**")
            if st.button("➡ Proceed to Payment"):
                if not st.session_state.selected_seats:
                    st.warning("Select at least one seat")
                else:
                    st.session_state.stage = 'payment'
                    st.rerun()

        elif st.session_state.stage == 'payment':
            st.header("Payment & Passenger Details")
            bus = st.session_state.selected_bus
            seats = st.session_state.selected_seats
            total = bus['Fare'] * len(seats)

            st.markdown(f"**Bus:** {bus['Bus Name']} ({bus['Type']})")
            st.markdown(f"**Total Fare:** ₹{total}")

            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

            if st.button("✅ Confirm Booking"):
                if not (name and email and phone):
                    st.error("Please fill all details")
                else:
                    c.execute('''
                        INSERT INTO bookings 
                        (user_id, name, email, phone, source, destination, journey_date, bus_name, bus_type, seats, total_fare, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        st.session_state.user[0], name, email, phone,
                        st.session_state.journey_info['from'],
                        st.session_state.journey_info['to'],
                        st.session_state.journey_info['date'],
                        bus['Bus Name'], bus['Type'],
                        ','.join(seats), total,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    conn.commit()
                    st.success("🎉 Booking Confirmed!")
                    st.balloons()
                    st.session_state.stage = 'search'
                    st.session_state.selected_seats = []