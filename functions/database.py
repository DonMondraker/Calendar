import sqlite3
import os
import bcrypt

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # ---------------- USERS ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            timezone TEXT NOT NULL,
            email TEXT 
        )
    """)

    # ---------------- EVENTS ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT,
            start TEXT NOT NULL,
            end TEXT NOT NULL,
            timezone TEXT NOT NULL,
            created_by TEXT NOT NULL,
            is_private INTEGER DEFAULT 0,
            recurrence TEXT,
            subject_color TEXT NOT NULL
        )
    """)

    # ---------------- ATTENDANCE ----------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            event_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            status TEXT NOT NULL,
            PRIMARY KEY (event_id, username)
        )
    """)

    conn.commit()

    # ---------------- PRE-CREATE USERS ----------------
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        def insert_user(username, password, role, timezone, email):
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            c.execute(
                "INSERT INTO users (username, password_hash, role, timezone, email) VALUES (?, ?, ?, ?, ?)",
                (username, pw_hash, role, timezone, email),
            )

        insert_user("Admin", "Admin395", "admin", "Europe/Stockholm", "mrvicke@live.se")
        insert_user("Johanna", "Johanna123", "user", "Europe/Stockholm", "johanna.borgstrom98@gmail.com")
        insert_user("Veronika", "Veronika123", "user", "Europe/Stockholm", "veronikaborgstrom@gmail.com")
        insert_user("Jessica", "Jessica123", "user", "Europe/Stockholm", "jessica.borgstrom@ockero.se")
        insert_user("Claes", "Claes123", "user", "Europe/Stockholm", "claes.borgstrom@bergpropulsion.com")
        insert_user("Viktor", "Viktor123", "user", "Europe/Stockholm", "mrvicke@live.se")
        # insert_user("Niclas", "Niclas123", "user", "Europe/Stockholm", "mrvicke@live.se")
        # insert_user("Jonathan", "Jonathan123", "user", "Europe/Stockholm", "mrvicke@live.se")

        conn.commit()

    conn.close()
