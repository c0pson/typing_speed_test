import sqlite3

def setup_database():
    conn = sqlite3.connect('typing_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TypingStats (
        stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        wpm REAL NOT NULL,
        cpm REAL NOT NULL,
        accuracy REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_stat(wpm, cpm, accuracy):
    conn = sqlite3.connect('typing_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO TypingStats (wpm, cpm, accuracy)
    VALUES (?, ?, ?)
    ''', (wpm, cpm, accuracy))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect('typing_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT time, wpm, cpm, accuracy
    FROM TypingStats
    ORDER BY time DESC
    ''')
    stats = cursor.fetchall()
    conn.close()
    return stats
