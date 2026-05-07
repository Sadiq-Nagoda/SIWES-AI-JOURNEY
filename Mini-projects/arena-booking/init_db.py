"""
init_db.py — Run this once to create the database.
Usage: python init_db.py
"""
import sqlite3

DATABASE = "arena.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name   TEXT    NOT NULL,
            phone       TEXT    NOT NULL,
            time_slot   TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            pitch_type  TEXT    NOT NULL DEFAULT '5-aside',
            status      TEXT    NOT NULL DEFAULT 'confirmed',
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    # This UNIQUE index is the core anti-double-booking constraint
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_slot_date
        ON bookings (time_slot, date)
    """)

    conn.commit()
    conn.close()
    print("✅  arena.db created and ready!")
    print("🏟️  Run: python app.py")

if __name__ == "__main__":
    init_db()