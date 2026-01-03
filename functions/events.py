from datetime import datetime
from functions.database import get_connection
from functions.notifications import send_event_created_email


# --------------------------------------------------
# FETCH EVENTS
# --------------------------------------------------
def get_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id,
            title,
            subject,
            description,
            start,
            end,
            timezone,
            created_by,
            is_private,
            recurrence,
            subject_color
        FROM events
        ORDER BY start
    """)

    rows = cur.fetchall()
    conn.close()

    events = []
    for r in rows:
        events.append({
            "id": r[0],
            "title": r[1],
            "subject": r[2],
            "description": r[3],
            "start": r[4],
            "end": r[5],
            "timezone": r[6],
            "created_by": r[7],
            "is_private": r[8],
            "recurrence": r[9],
            "subject_color": r[10],
        })

    return events


# --------------------------------------------------
# CREATE EVENT (SMS TRIGGER HERE)
# --------------------------------------------------
def create_event(event):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO events (
            title,
            subject,
            description,
            start,
            end,
            timezone,
            created_by,
            is_private,
            recurrence,
            subject_color
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["title"],
        event["subject"],
        event["description"],
        event["start"],
        event["end"],
        event["timezone"],
        event["created_by"],
        event["is_private"],
        event["recurrence"],
        event["subject_color"],
    ))

    conn.commit()
    conn.close()

    # 🔔 SMS notification (ONLY on creation)
    send_event_created_email(event)

# --------------------------------------------------
# UPDATE EVENT DATES (DRAG & DROP)
# --------------------------------------------------
def update_event_time(event_id, new_start, new_end, username, is_admin):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT created_by FROM events WHERE id=?", (event_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    creator = row[0]

    if creator != username and not is_admin:
        conn.close()
        return False

    cur.execute("""
        UPDATE events
        SET start=?, end=?
        WHERE id=?
    """, (new_start, new_end, event_id))

    conn.commit()
    conn.close()
    return True


# --------------------------------------------------
# EDIT EVENT (TITLE / DESC / DATES)
# --------------------------------------------------
def update_event(event_id, data, username, is_admin):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT created_by FROM events WHERE id=?", (event_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    creator = row[0]
    if creator != username and not is_admin:
        conn.close()
        return False

    cur.execute("""
        UPDATE events
        SET
            title=?,
            description=?,
            start=?,
            end=?
        WHERE id=?
    """, (
        data["title"],
        data["description"],
        data["start"],
        data["end"],
        event_id
    ))

    conn.commit()
    conn.close()
    return True


# --------------------------------------------------
# DELETE EVENT
# --------------------------------------------------
def delete_event(event_id, username, is_admin):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT created_by FROM events WHERE id=?", (event_id,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return False

    creator = row[0]

    if creator != username and not is_admin:
        conn.close()
        return False

    cur.execute("DELETE FROM events WHERE id=?", (event_id,))
    cur.execute("DELETE FROM attendance WHERE event_id=?", (event_id,))

    conn.commit()
    conn.close()
    return True
