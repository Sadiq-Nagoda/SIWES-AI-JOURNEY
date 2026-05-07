"""
Football Arena Booking System - MVP
Backend: Flask + SQLite
Nigeria 5-a-side / 7-a-side Pitch Booking
"""

import sqlite3
import re
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = "arena_secret_key_change_in_production"

DATABASE = "arena.db"

# ─────────────────────────────────────────
#  Available time slots for the arena
# ─────────────────────────────────────────
TIME_SLOTS = [
    "06:00 - 07:00",
    "07:00 - 08:00",
    "08:00 - 09:00",
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "12:00 - 13:00",
    "13:00 - 14:00",
    "14:00 - 15:00",
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00",
    "18:00 - 19:00",
    "19:00 - 20:00",
    "20:00 - 21:00",
    "21:00 - 22:00",
]

# ─────────────────────────────────────────
#  Database helpers
# ─────────────────────────────────────────

def get_db():
    """Return a database connection with row factory enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
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

    # Unique constraint: one booking per slot per date
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_slot_date
        ON bookings (time_slot, date)
    """)

    conn.commit()
    conn.close()
    print("✅  Database initialised: arena.db")


# ─────────────────────────────────────────
#  Validation helpers
# ─────────────────────────────────────────

def validate_phone(phone):
    """Accept Nigerian mobile numbers (08xx, 07xx, 09xx, +234xx)."""
    pattern = r"^(\+234|0)[789]\d{9}$"
    return re.match(pattern, phone.replace(" ", ""))


def validate_date(date_str):
    """Ensure date is today or in the future."""
    try:
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return booking_date >= date.today()
    except ValueError:
        return False


# ─────────────────────────────────────────
#  Routes
# ─────────────────────────────────────────

@app.route("/")
def index():
    """
    Home page — show all time slots for a selected date.
    Marks each slot as available or booked.
    """
    selected_date = request.args.get("date", date.today().isoformat())

    conn = get_db()
    booked_rows = conn.execute(
        "SELECT time_slot FROM bookings WHERE date = ? AND status != 'cancelled'",
        (selected_date,)
    ).fetchall()
    conn.close()

    booked_slots = {row["time_slot"] for row in booked_rows}

    slots = []
    for slot in TIME_SLOTS:
        slots.append({
            "time": slot,
            "booked": slot in booked_slots
        })

    return render_template("index.html",
                           slots=slots,
                           selected_date=selected_date,
                           today=date.today().isoformat())


@app.route("/book", methods=["GET", "POST"])
def book():
    """
    GET  → Render booking form with available slots pre-filled.
    POST → Validate input, check for double booking, save booking.
    """
    if request.method == "GET":
        selected_date = request.args.get("date", date.today().isoformat())
        preselect_slot = request.args.get("slot", "")

        # Only show available slots in the dropdown
        conn = get_db()
        booked_rows = conn.execute(
            "SELECT time_slot FROM bookings WHERE date = ? AND status != 'cancelled'",
            (selected_date,)
        ).fetchall()
        conn.close()

        booked_slots = {row["time_slot"] for row in booked_rows}
        available_slots = [s for s in TIME_SLOTS if s not in booked_slots]

        return render_template("book.html",
                               available_slots=available_slots,
                               selected_date=selected_date,
                               preselect_slot=preselect_slot,
                               today=date.today().isoformat())

    # ── POST: process the form ──────────────────────────────────────────
    team_name  = request.form.get("team_name", "").strip()
    phone      = request.form.get("phone", "").strip()
    time_slot  = request.form.get("time_slot", "").strip()
    book_date  = request.form.get("date", "").strip()
    pitch_type = request.form.get("pitch_type", "5-aside").strip()

    errors = []

    # Input validation
    if not team_name:
        errors.append("Team name is required.")
    if len(team_name) > 60:
        errors.append("Team name must be under 60 characters.")
    if not phone:
        errors.append("Phone number is required.")
    elif not validate_phone(phone):
        errors.append("Enter a valid Nigerian phone number (e.g. 08012345678).")
    if time_slot not in TIME_SLOTS:
        errors.append("Please select a valid time slot.")
    if not book_date:
        errors.append("Date is required.")
    elif not validate_date(book_date):
        errors.append("Please select today or a future date.")

    if errors:
        conn = get_db()
        booked_rows = conn.execute(
            "SELECT time_slot FROM bookings WHERE date = ? AND status != 'cancelled'",
            (book_date,)
        ).fetchall()
        conn.close()
        booked_slots = {row["time_slot"] for row in booked_rows}
        available_slots = [s for s in TIME_SLOTS if s not in booked_slots]

        return render_template("book.html",
                               errors=errors,
                               available_slots=available_slots,
                               selected_date=book_date,
                               preselect_slot=time_slot,
                               today=date.today().isoformat(),
                               form_data=request.form)

    # ── CRITICAL: Double-booking check ─────────────────────────────────
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM bookings WHERE time_slot = ? AND date = ? AND status != 'cancelled'",
        (time_slot, book_date)
    ).fetchone()

    if existing:
        conn.close()
        booked_rows_2 = get_db().execute(
            "SELECT time_slot FROM bookings WHERE date = ? AND status != 'cancelled'",
            (book_date,)
        ).fetchall()
        booked_slots = {row["time_slot"] for row in booked_rows_2}
        available_slots = [s for s in TIME_SLOTS if s not in booked_slots]

        return render_template("book.html",
                               errors=["❌ Sorry! That slot is already booked. Please choose another."],
                               available_slots=available_slots,
                               selected_date=book_date,
                               preselect_slot="",
                               today=date.today().isoformat(),
                               form_data=request.form)

    # ── Save booking ─────────────────────────────────────────────────────
    try:
        conn.execute(
            """INSERT INTO bookings (team_name, phone, time_slot, date, pitch_type, status)
               VALUES (?, ?, ?, ?, ?, 'confirmed')""",
            (team_name, phone, time_slot, book_date, pitch_type)
        )
        conn.commit()
        booking_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()

        flash({
            "type": "success",
            "booking_id": booking_id,
            "team": team_name,
            "slot": time_slot,
            "date": book_date,
            "pitch": pitch_type,
            "phone": phone
        })
        return redirect(url_for("confirmation"))

    except sqlite3.IntegrityError:
        # Catches race-condition double inserts at DB level
        conn.close()
        return render_template("book.html",
                               errors=["❌ That slot was just taken. Please pick another."],
                               available_slots=[s for s in TIME_SLOTS],
                               selected_date=book_date,
                               preselect_slot="",
                               today=date.today().isoformat())


@app.route("/confirmation")
def confirmation():
    """Show booking confirmation receipt."""
    booking = dict(request.args) if request.args else None
    messages = []
    for cat in ["_flashes"]:
        pass

    # Read flash message
    from flask import get_flashed_messages
    raw = get_flashed_messages()
    data = raw[0] if raw else None

    return render_template("confirmation.html", booking=data)


@app.route("/admin")
def admin():
    """Admin dashboard — view all bookings, filter by date."""
    filter_date = request.args.get("date", "")
    filter_status = request.args.get("status", "")

    conn = get_db()
    query = "SELECT * FROM bookings WHERE 1=1"
    params = []

    if filter_date:
        query += " AND date = ?"
        params.append(filter_date)
    if filter_status:
        query += " AND status = ?"
        params.append(filter_status)

    query += " ORDER BY date ASC, time_slot ASC"

    bookings = conn.execute(query, params).fetchall()

    # Stats
    total     = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    confirmed = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='confirmed'").fetchone()[0]
    cancelled = conn.execute("SELECT COUNT(*) FROM bookings WHERE status='cancelled'").fetchone()[0]
    today_ct  = conn.execute(
        "SELECT COUNT(*) FROM bookings WHERE date=? AND status='confirmed'",
        (date.today().isoformat(),)
    ).fetchone()[0]
    conn.close()

    return render_template("admin.html",
                           bookings=bookings,
                           total=total,
                           confirmed=confirmed,
                           cancelled=cancelled,
                           today_count=today_ct,
                           filter_date=filter_date,
                           filter_status=filter_status)


@app.route("/admin/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    """Cancel a booking by ID."""
    conn = get_db()
    conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    flash("Booking cancelled successfully.")
    return redirect(url_for("admin"))


# ── API endpoint for AJAX slot availability check ──────────────────────
@app.route("/api/slots")
def api_slots():
    """Return available slots for a date as JSON (for dynamic frontend)."""
    req_date = request.args.get("date", date.today().isoformat())
    conn = get_db()
    booked_rows = conn.execute(
        "SELECT time_slot FROM bookings WHERE date = ? AND status != 'cancelled'",
        (req_date,)
    ).fetchall()
    conn.close()
    booked = {r["time_slot"] for r in booked_rows}
    result = [{"slot": s, "available": s not in booked} for s in TIME_SLOTS]
    return jsonify(result)


# ─────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("🏟️  Football Arena Booking System is running!")
    print("👉  Open: http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)