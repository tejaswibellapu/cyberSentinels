import sqlite3
from datetime import datetime

DB_PATH = "database/threats.db"


# ---------------- CREATE DATABASE ---------------- #

def init_db():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS threats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attacker_ip TEXT,
        attack_type TEXT,
        risk_score INTEGER,
        attempts INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("✓ Database initialized")


# ---------------- INSERT THREAT ---------------- #

def insert_threat(attacker_ip, attack_type, risk_score, attempts):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO threats(attacker_ip, attack_type, risk_score, attempts, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (attacker_ip, attack_type, risk_score, attempts, timestamp))

    conn.commit()
    conn.close()

    print("✓ Threat stored in database")


# ---------------- GET ALL THREATS ---------------- #

def get_all_threats():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM threats ORDER BY id DESC")

    rows = cursor.fetchall()

    conn.close()

    return rows


# ---------------- INSERT 10 FAKE THREATS ---------------- #

def seed_fake_data():

    fake_data = [

            ("67.211.54.31", "DDos", 45, 7),
    ("190.45.32.78", "DDoS", 92, 40),
    ("10.143.123.61", "Packet Flood", 51, 1)
    ]

    for threat in fake_data:
        insert_threat(*threat)

    print("✓ 10 fake threats inserted")


# ---------------- RUN SEED (only once) ---------------- #

if __name__ == "__main__":

    init_db()
    seed_fake_data()