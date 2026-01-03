import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from functions.database import get_connection
from dotenv import load_dotenv
load_dotenv()


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_event_created_email(event):
    if not all([EMAIL_HOST, EMAIL_USER, EMAIL_PASS]):
        print("📴 Email notifications disabled (missing config)")
        return

    recipients = get_user_emails()
    if not recipients:
        return

    msg = EmailMessage()
    msg["Subject"] = f"📅 New event: {event['title']}"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join(recipients)

    start_date = event["start"][:10]
    end_date = event["end"][:10]

    msg.set_content(
        f"""
A new event has been created.

Title: {event['title']}
Subject: {event['subject']}
Date: {start_date} → {end_date}
Created by: {event['created_by']}

Description:
{event['description']}
Link:
https://calendarapp.streamlit.app/
"""
    )

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
    except Exception as e:
        print("⚠️ Email failed:", e)


def get_user_emails():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT email FROM users
        WHERE email IS NOT NULL AND email != ''
    """)

    emails = [row[0] for row in cur.fetchall()]
    conn.close()
    return emails
