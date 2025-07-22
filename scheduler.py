import sqlite3
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(event):
    msg = MIMEText(f"Reminder: {event[1]} is happening on {event[2]} at {event[3]}!\nDescription: {event[4]}")
    msg['Subject'] = f'Event Reminder: {event[1]}'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

def check_reminders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    now = datetime.now()
    reminder_time = now + timedelta(minutes=30)
    c.execute('SELECT * FROM events WHERE reminder_sent = 0')
    events = c.fetchall()
    
    for event in events:
        event_datetime = datetime.strptime(f"{event[2]} {event[3]}", '%Y-%m-%d %H:%M')
        if now <= event_datetime <= reminder_time:
            send_email(event)
            c.execute('UPDATE events SET reminder_sent = 1 WHERE id = ?', (event[0],))
            conn.commit()
    conn.close()

schedule.every(1).minutes.do(check_reminders)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(60)
