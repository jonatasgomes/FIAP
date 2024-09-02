import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)

def get_connection():
    return conn

def check_database():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS culturas (id INTEGER PRIMARY KEY, cultura TEXT)')
    conn.commit()
