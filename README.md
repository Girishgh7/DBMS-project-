# 🚌 Blue Bus Booking App

A Streamlit-based multi-page web application that enables users to register, log in, and book bus tickets, while allowing an admin to monitor all bookings. The app uses an SQLite3 database to store user and booking data, and employs secure password hashing.

---

## 📦 Features

- 🔐 **User Authentication**: Register, login, and secure password handling using SHA-256 hashing.
- 🎟️ **Ticket Booking**: Select source, destination, date, bus type, and seats.
- 🗃️ **Admin Dashboard**: View all bookings with date, passenger, and bus details.
- 🧠 **Session Management**: Dynamic page control using Streamlit's `session_state`.
- 💾 **Persistent Storage**: Uses `SQLite3` to store user credentials and bookings.

---

## 🧰 Tech Stack

| Component    | Technology         |
|--------------|--------------------|
| UI Framework | [Streamlit](https://streamlit.io) |
| Database     | SQLite3            |
| Language     | Python 3           |
| Security     | `hashlib` for password hashing |
| Data Display | `pandas` for admin dashboard |

---

## 🛠️ How to Run

1. **Clone or Download** the repository.

2. **Install dependencies**:
   ```bash
   pip install streamlit pandas
   ```

3. **Run the application**:
   ```bash
   streamlit run bus_app.py
   ```

> Make sure the file `bus_booking.db` is in the same directory as `bus_app.py`.

---

## 📂 Project Structure

```
.
├── bus_app.py          # Main Streamlit app with login, booking, and admin views
├── admin_page.py       # (Optional) Admin dashboard module
├── bus_booking.db      # SQLite database storing users and bookings
└── README.md           # Documentation
```

---

## 🔍 Functional Overview

### 🔐 User Management

* **Registration**: Creates a new user with a hashed password.
* **Login**: Authenticates using SHA-256 hash comparison.
* **Logout**: Clears session state.

### 🧾 Booking Workflow

1. **Search**: Select source, destination, and travel date.
2. **Bus Selection**: Choose from predefined bus types (AC, Sleeper, Deluxe).
3. **Seat Selection**: Dynamically rendered seat map (e.g., A1–E4).
4. **Booking**: Confirms and stores the booking in the database.

### 🛡️ Admin Panel

* Accessible only to the hardcoded admin user (`girish`).
* Displays all booking records in a `pandas` dataframe.
* Offers visibility into user bookings, dates, and buses.

---

## 🧠 Code Structure Summary

### `bus_app.py`

| Section              | Description                                                           |
| -------------------- | --------------------------------------------------------------------- |
| `st.set_page_config` | Sets the title and layout of the Streamlit app                        |
| `sqlite3.connect`    | Connects to the `bus_booking.db` file                                 |
| `CREATE TABLE`       | Ensures `users` and `bookings` tables exist                           |
| `hash_password()`    | Hashes user passwords for secure storage                              |
| `check_login()`      | Validates username/password against DB                                |
| `register_user()`    | Adds new users to DB if not already registered                        |
| `generate_seats()`   | Creates a list like A1, A2, ..., E4 for seat selection                |
| `st.session_state`   | Maintains session state (e.g., logged-in user, current page)          |
| Navigation Sidebar   | Selects between Login, Register, Book Ticket, Admin Dashboard, Logout |
| Booking Workflow     | Controlled via `st.session_state.stage` logic                         |
| Admin Dashboard      | Shows all bookings to authorized admin                                |

---

## 🧱 Database Schema

### `users` Table

| Column   | Type                  |
| -------- | --------------------- |
| id       | INTEGER (Primary Key) |
| username | TEXT (Unique)         |
| password | TEXT (SHA-256 hash)   |

### `bookings` Table

| Column      | Type                     |
| ----------- | ------------------------ |
| id          | INTEGER (Primary Key)    |
| username    | TEXT                     |
| source      | TEXT                     |
| destination | TEXT                     |
| date        | TEXT (ISO format)        |
| bus_type    | TEXT (e.g., AC, Sleeper) |
| seat        | TEXT (e.g., A1, B2)      |

---

## ⚙️ Future Improvements

- ✅ Implement dynamic seat availability check
- ✅ Integrate email confirmations for bookings
- 🚫 Admin credentials are currently hardcoded — move to DB
- 🔜 Add payment gateway integration
- 🔒 Role-based access control (RBAC)

---

## 👥 Contributors

| Name   | Role                          |
| ------ | ----------------------------- |
| Girish | Developer / Admin login logic |
| Damini | UI / Booking System           |
| Ann    | Database Design / Integration |

---

## 📜 License

This project is for educational and demonstration purposes only. No commercial rights granted.
