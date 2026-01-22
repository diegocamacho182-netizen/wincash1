import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance INTEGER,
    referral_code INTEGER,
    bets INTEGER
)
""")

conn.commit()
conn.close()

print("BD actualizada")
