import sqlite3

def create_database():

    conn = sqlite3.connect("health.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        heart_rate INTEGER,
        spo2 INTEGER,
        temperature REAL,
        symptoms TEXT
    )
    """)

    conn.commit()
    conn.close()
