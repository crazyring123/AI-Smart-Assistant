# database.py

import sqlite3

def init_db():
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()

    # Email table: id, thread_id, sender, subject, body, timestamp
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            thread_id TEXT,
            sender TEXT,
            subject TEXT,
            body TEXT,
            timestamp TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

if __name__ == "__main__":
    init_db()
