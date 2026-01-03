from functions.database import get_connection

def set_attendance(event_id, username, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO attendance
        (event_id, username, status)
        VALUES (?, ?, ?)
    """, (event_id, username, status))
    conn.commit()
    conn.close()

def get_attendance(event_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT username, status FROM attendance WHERE event_id=?",
        (event_id,)
    )
    rows = c.fetchall()
    conn.close()
    return rows
