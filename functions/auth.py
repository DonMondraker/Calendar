import sqlite3
import bcrypt
from functions.database import get_connection

def create_user(username, password, role="user", timezone="UTC"):
    conn = get_connection()
    c = conn.cursor()

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        c.execute(
            "INSERT INTO users (username, password_hash, role, timezone) VALUES (?, ?, ?, ?)",
            (username, pw_hash, role, timezone),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

import bcrypt
from functions.database import get_connection


def authenticate_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT username, password_hash, role, timezone FROM users WHERE username=?",
        (username,),
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return None

    if bcrypt.checkpw(password.encode(), row[1].encode()):
        return {
            "username": row[0],
            "role": row[2],
            "timezone": row[3],
        }

    return None

