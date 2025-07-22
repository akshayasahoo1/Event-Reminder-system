import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        description TEXT,
        reminder_sent BOOLEAN DEFAULT 0
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_event', methods=['POST'])
def add_event():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    description = request.form.get('description', '')
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO events (name, date, time, description) VALUES (?, ?, ?, ?)',
              (name, date, time, description))
    conn.commit()
    conn.close()
    
    return redirect(url_for('events'))

@app.route('/events')
def events():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE date >= date("now") ORDER BY date, time')
    events = c.fetchall()
    conn.close()
    return render_template('events.html', events=events)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, use_reloader=False)
