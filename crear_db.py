import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    balance INTEGER DEFAULT 0,
    apuestas INTEGER DEFAULT 0,
    referral_code TEXT
)
""")

c.execute("""
CREATE TABLE referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    referrer_id INTEGER,
    referred_username TEXT
)
""")

c.execute("""
CREATE TABLE apuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan INTEGER,
    status TEXT
)
""")

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente")
