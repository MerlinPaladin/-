import sqlite3

def create_connection():
    conn = sqlite3.connect('events.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_event(name, date, location):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (name, date, location)
        VALUES (?, ?, ?)
    ''', (name, date, location))
    conn.commit()
    conn.close()

def get_events():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events')
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_event(event_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()