"""
============================================================
 Maracana Football Arena Kano — Booking System
 Version 2.0 | Production-Grade
 Stack: Flask + SQLite | Nigeria-optimised
============================================================

 Architecture notes:
   - Single-file Flask app for simplicity; split into blueprints
     when adding 2nd arena or user auth system.
   - All DB calls use parameterised queries (SQL-injection safe).
   - Booking status machine:  PENDING → CONFIRMED | CANCELLED | FAILED | NO_SHOW
   - Payment status machine:  PENDING → VERIFIED | FAILED
   - Slots blocked by admin show status = 'BLOCKED' in bookings table
     with team_name = '__BLOCKED__' sentinel.
   - Paystack integration: initiate → redirect → webhook confirms.
     Set PAYSTACK_SECRET_KEY env var in production.
"""

import sqlite3
import re
import os
import uuid
import hashlib
import hmac
import json
import logging
from datetime import datetime, date, timedelta
from functools import wraps

import requests 
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, jsonify, session, abort, g
)

# ══════════════════════════════════════════════════════════
#  APP BOOTSTRAP
# ══════════════════════════════════════════════════════════

app = Flask(__name__)

# ── Secrets — override via environment variables in production ──────────
app.secret_key = os.environ.get("SECRET_KEY", "maracana-dev-secret-CHANGE-IN-PROD")
ADMIN_PASSWORD  = os.environ.get("ADMIN_PASSWORD", "admin1234")   # change before going live

# ── Arena config — one place to rebrand the entire app ─────────────────
ARENA_NAME     = os.environ.get("ARENA_NAME",    "Maracana Football Arena Kano")
ARENA_LOCATION = os.environ.get("ARENA_LOCATION", "Kano, Nigeria")
ARENA_PHONE    = os.environ.get("ARENA_PHONE",    "08099998888")
ARENA_EMAIL    = os.environ.get("ARENA_EMAIL",    "info@maracana.ng")

# ── Pricing (Naira) ─────────────────────────────────────────────────────
PRICE = {
    "5-aside": 15_000,
    "7-aside": 25_000,
}

# ── Paystack ─────────────────────────────────────────────────────────────
PAYSTACK_SECRET_KEY  = os.environ.get("PAYSTACK_SECRET_KEY", "")
PAYSTACK_PUBLIC_KEY  = os.environ.get("PAYSTACK_PUBLIC_KEY", "")
PAYSTACK_BASE_URL    = "https://api.paystack.co"
PAYMENT_SIMULATE     = not bool(PAYSTACK_SECRET_KEY)   # True → use simulated payment

# ── Database ─────────────────────────────────────────────────────────────
DATABASE = os.environ.get("DATABASE_PATH", "arena.db")

# ── Time slots — 1-hour blocks, 06:00–22:00 ─────────────────────────────
TIME_SLOTS = [
    "06:00 - 07:00", "07:00 - 08:00", "08:00 - 09:00",
    "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00",
    "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00",
    "15:00 - 16:00", "16:00 - 17:00", "17:00 - 18:00",
    "18:00 - 19:00", "19:00 - 20:00", "20:00 - 21:00",
    "21:00 - 22:00",
]

# ── Booking & payment state constants ────────────────────────────────────
class BookingStatus:
    PENDING    = "PENDING"
    CONFIRMED  = "CONFIRMED"
    CANCELLED  = "CANCELLED"
    FAILED     = "FAILED"
    NO_SHOW    = "NO_SHOW"
    BLOCKED    = "BLOCKED"      # admin-blocked slot
    PAY_VENUE  = "PAY_VENUE"   # pay at venue, confirmed without online payment

class PaymentStatus:
    PENDING  = "PENDING"
    VERIFIED = "VERIFIED"
    FAILED   = "FAILED"
    WAIVED   = "WAIVED"        # admin waived payment (pay at venue)

# ── Logging ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ══════════════════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════════════════

def get_db():
    """
    Return a per-request SQLite connection stored on Flask's g object.
    Teardown closes it automatically at end of request.
    """
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA journal_mode=WAL")    # safe for concurrent reads
        g.db.execute("PRAGMA foreign_keys=ON")
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    """
    Create all tables and indexes.
    Safe to call multiple times — uses IF NOT EXISTS everywhere.
    """
    with app.app_context():
        db = get_db()

        # ── bookings ─────────────────────────────────────────────────────
        db.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_ref     TEXT    NOT NULL UNIQUE,   -- human-readable ref e.g. MRK-00042
                team_name       TEXT    NOT NULL,
                phone           TEXT    NOT NULL,
                email           TEXT,
                time_slot       TEXT    NOT NULL,
                date            TEXT    NOT NULL,
                pitch_type      TEXT    NOT NULL DEFAULT '5-aside',
                amount          INTEGER NOT NULL DEFAULT 0, -- Naira
                booking_status  TEXT    NOT NULL DEFAULT 'PENDING',
                payment_status  TEXT    NOT NULL DEFAULT 'PENDING',
                payment_ref     TEXT,                       -- Paystack reference
                notes           TEXT,                       -- admin notes
                created_by      TEXT    NOT NULL DEFAULT 'customer', -- 'customer'|'admin'
                created_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime')),
                updated_at      TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """)

        # ── CRITICAL: prevent double-booking at DB level ──────────────────
        # Only one CONFIRMED/PENDING/PAY_VENUE booking per slot per date.
        # CANCELLED, FAILED, NO_SHOW slots are freed automatically.
        db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_slot_date_active
            ON bookings (time_slot, date)
            WHERE booking_status NOT IN ('CANCELLED','FAILED','NO_SHOW')
        """)

        # Fast lookups
        db.execute("CREATE INDEX IF NOT EXISTS idx_date ON bookings(date)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_status ON bookings(booking_status)")
        db.execute("CREATE INDEX IF NOT EXISTS idx_payment_ref ON bookings(payment_ref)")

        # ── blocked_periods ───────────────────────────────────────────────
        db.execute("""
            CREATE TABLE IF NOT EXISTS blocked_periods (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL,
                time_slot   TEXT,               -- NULL means entire day blocked
                reason      TEXT    NOT NULL DEFAULT 'Maintenance',
                created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """)
        db.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_block_slot_date
            ON blocked_periods (date, time_slot)
        """)

        # ── audit_log ─────────────────────────────────────────────────────
        db.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                booking_ref TEXT,
                action      TEXT    NOT NULL,
                actor       TEXT    NOT NULL DEFAULT 'system',
                detail      TEXT,
                created_at  TEXT    NOT NULL DEFAULT (datetime('now','localtime'))
            )
        """)

        # ── sequence counter for human refs ──────────────────────────────
        db.execute("""
            CREATE TABLE IF NOT EXISTS counters (
                name    TEXT PRIMARY KEY,
                value   INTEGER NOT NULL DEFAULT 0
            )
        """)
        db.execute("""
            INSERT OR IGNORE INTO counters (name, value) VALUES ('booking_seq', 0)
        """)

        db.commit()
        logger.info("✅ Database initialised: %s", DATABASE)


# ══════════════════════════════════════════════════════════
#  HELPER UTILITIES
# ══════════════════════════════════════════════════════════

def next_booking_ref(db):
    """
    Generate sequential human-readable booking reference.
    Format: MRK-00042
    Thread-safe via SQLite's atomic UPDATE + RETURNING.
    """
    db.execute("UPDATE counters SET value = value + 1 WHERE name='booking_seq'")
    seq = db.execute("SELECT value FROM counters WHERE name='booking_seq'").fetchone()[0]
    return f"MRK-{seq:05d}"


def validate_nigerian_phone(phone: str) -> bool:
    """Accept 080x, 081x, 070x, 090x, 091x, +234x formats."""
    cleaned = phone.replace(" ", "").replace("-", "")
    return bool(re.match(r"^(\+234|0)[789]\d{9}$", cleaned))


def validate_future_date(date_str: str) -> bool:
    """Date must be today or in the future."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return d >= date.today()
    except ValueError:
        return False


def get_slot_map(db, target_date: str) -> dict:
    """
    Return a dict: time_slot → {status, booking_ref, team_name}
    Status values: 'available', 'booked', 'blocked', 'pending'
    """
    # Active bookings for this date
    rows = db.execute("""
        SELECT time_slot, booking_status, booking_ref, team_name
        FROM bookings
        WHERE date = ?
          AND booking_status NOT IN ('CANCELLED','FAILED','NO_SHOW')
    """, (target_date,)).fetchall()

    booked = {}
    for row in rows:
        booked[row["time_slot"]] = {
            "status":      "pending" if row["booking_status"] == BookingStatus.PENDING else "booked",
            "booking_ref": row["booking_ref"],
            "team_name":   row["team_name"],
            "bs":          row["booking_status"],
        }

    # Blocked periods
    blocks = db.execute("""
        SELECT time_slot FROM blocked_periods
        WHERE date = ? AND (time_slot IS NOT NULL)
    """, (target_date,)).fetchall()
    day_blocked = db.execute("""
        SELECT id FROM blocked_periods
        WHERE date = ? AND time_slot IS NULL
        LIMIT 1
    """, (target_date,)).fetchone()

    slot_map = {}
    for slot in TIME_SLOTS:
        if day_blocked:
            slot_map[slot] = {"status": "blocked", "booking_ref": None, "team_name": "Day Blocked"}
        elif slot in booked:
            slot_map[slot] = booked[slot]
        elif any(b["time_slot"] == slot for b in blocks):
            slot_map[slot] = {"status": "blocked", "booking_ref": None, "team_name": "Blocked"}
        else:
            slot_map[slot] = {"status": "available", "booking_ref": None, "team_name": None}

    return slot_map


def audit(db, booking_ref, action, actor="system", detail=None):
    """Write a line to the audit log."""
    db.execute(
        "INSERT INTO audit_log (booking_ref, action, actor, detail) VALUES (?,?,?,?)",
        (booking_ref, action, actor, detail)
    )


def arena_context():
    """Common template context injected into every render_template call."""
    return {
        "arena_name":     ARENA_NAME,
        "arena_location": ARENA_LOCATION,
        "arena_phone":    ARENA_PHONE,
        "arena_email":    ARENA_EMAIL,
        "payment_simulate": PAYMENT_SIMULATE,
        "today":          date.today().isoformat(),
        "TIME_SLOTS":     TIME_SLOTS,
    }


# ══════════════════════════════════════════════════════════
#  ADMIN AUTH DECORATOR
# ══════════════════════════════════════════════════════════

def admin_required(f):
    """Simple session-based admin guard."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the admin area.", "warning")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ══════════════════════════════════════════════════════════
#  PUBLIC ROUTES
# ══════════════════════════════════════════════════════════

@app.route("/")
def index():
    """
    Home — slot availability grid for a selected date.
    Shows available / booked / blocked with team names for booked slots.
    """
    selected_date = request.args.get("date", date.today().isoformat())
    db = get_db()
    slot_map = get_slot_map(db, selected_date)

    # Summary counts
    counts = {"available": 0, "booked": 0, "blocked": 0, "pending": 0}
    for v in slot_map.values():
        counts[v["status"]] = counts.get(v["status"], 0) + 1

    ctx = arena_context()
    ctx.update({
        "slot_map":     slot_map,
        "TIME_SLOTS":   TIME_SLOTS,
        "selected_date": selected_date,
        "counts":       counts,
    })
    return render_template("index.html", **ctx)


@app.route("/book", methods=["GET", "POST"])
def book():
    """
    Booking flow:
      GET  → show form with available slots pre-populated
      POST → validate → create PENDING booking → redirect to payment
    """
    db = get_db()

    if request.method == "GET":
        selected_date  = request.args.get("date", date.today().isoformat())
        preselect_slot = request.args.get("slot", "")
        slot_map       = get_slot_map(db, selected_date)
        available      = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]

        ctx = arena_context()
        ctx.update({
            "available_slots": available,
            "selected_date":   selected_date,
            "preselect_slot":  preselect_slot,
            "PRICE":           PRICE,
        })
        return render_template("book.html", **ctx)

    # ── POST ─────────────────────────────────────────────────────────────
    team_name  = request.form.get("team_name",  "").strip()
    phone      = request.form.get("phone",      "").strip()
    email      = request.form.get("email",      "").strip().lower()
    time_slot  = request.form.get("time_slot",  "").strip()
    book_date  = request.form.get("date",       "").strip()
    pitch_type = request.form.get("pitch_type", "5-aside").strip()

    errors = []

    if not team_name:                       errors.append("Team name is required.")
    if len(team_name) > 80:                 errors.append("Team name must be under 80 characters.")
    if not phone:                           errors.append("Phone number is required.")
    elif not validate_nigerian_phone(phone):errors.append("Enter a valid Nigerian number (e.g. 08012345678).")
    if email and "@" not in email:          errors.append("Email address looks invalid.")
    if time_slot not in TIME_SLOTS:         errors.append("Please select a valid time slot.")
    if not book_date:                       errors.append("Date is required.")
    elif not validate_future_date(book_date):errors.append("Please select today or a future date.")
    if pitch_type not in PRICE:             errors.append("Please select a valid pitch type.")

    if errors:
        slot_map  = get_slot_map(db, book_date or date.today().isoformat())
        available = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]
        ctx = arena_context()
        ctx.update({
            "errors":          errors,
            "available_slots": available,
            "selected_date":   book_date,
            "preselect_slot":  time_slot,
            "form_data":       request.form,
            "PRICE":           PRICE,
        })
        return render_template("book.html", **ctx)

    # ── Double-booking guard (application level) ──────────────────────
    slot_map = get_slot_map(db, book_date)
    if slot_map.get(time_slot, {}).get("status") not in ("available",):
        slot_map  = get_slot_map(db, book_date)
        available = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]
        ctx = arena_context()
        ctx.update({
            "errors":          ["❌ That slot just became unavailable. Please choose another."],
            "available_slots": available,
            "selected_date":   book_date,
            "preselect_slot":  "",
            "form_data":       request.form,
            "PRICE":           PRICE,
        })
        return render_template("book.html", **ctx)

    # ── Create PENDING booking ─────────────────────────────────────────
    amount      = PRICE.get(pitch_type, 15_000)
    booking_ref = next_booking_ref(db)

    try:
        db.execute("""
            INSERT INTO bookings
              (booking_ref, team_name, phone, email, time_slot, date,
               pitch_type, amount, booking_status, payment_status, created_by)
            VALUES (?,?,?,?,?,?,?,?,'PENDING','PENDING','customer')
        """, (booking_ref, team_name, phone, email or None,
              time_slot, book_date, pitch_type, amount))
        db.commit()
        audit(db, booking_ref, "BOOKING_CREATED", "customer",
              f"{team_name} | {book_date} | {time_slot}")
        db.commit()

    except sqlite3.IntegrityError:
        # Race-condition: another request beat us to the UNIQUE index
        logger.warning("Race-condition double-booking attempt on %s %s", book_date, time_slot)
        slot_map  = get_slot_map(db, book_date)
        available = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]
        ctx = arena_context()
        ctx.update({
            "errors":          ["❌ That slot was just taken by another team. Please choose another."],
            "available_slots": available,
            "selected_date":   book_date,
            "preselect_slot":  "",
            "form_data":       request.form,
            "PRICE":           PRICE,
        })
        return render_template("book.html", **ctx)

    # ── Redirect to payment ───────────────────────────────────────────
    return redirect(url_for("payment_page", booking_ref=booking_ref))


# ══════════════════════════════════════════════════════════
#  PAYMENT ROUTES
# ══════════════════════════════════════════════════════════

@app.route("/pay/<booking_ref>")
def payment_page(booking_ref):
    """
    Payment page — shows booking summary and launches payment.
    In simulate mode: provides a 'Simulate Pay' button.
    In live mode: initialises Paystack inline checkout.
    """
    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,)
    ).fetchone()

    if not booking:
        abort(404)

    # If already paid or confirmed, go straight to confirmation
    if booking["booking_status"] in (BookingStatus.CONFIRMED, BookingStatus.PAY_VENUE):
        return redirect(url_for("confirmation", booking_ref=booking_ref))

    # If cancelled or failed, show error
    if booking["booking_status"] in (BookingStatus.CANCELLED, BookingStatus.FAILED):
        flash("This booking has been cancelled or failed.", "error")
        return redirect(url_for("index"))

    ctx = arena_context()
    ctx.update({
        "booking":            dict(booking),
        "paystack_public_key": PAYSTACK_PUBLIC_KEY,
        "PRICE":              PRICE,
    })
    return render_template("payment.html", **ctx)


@app.route("/pay/<booking_ref>/initiate", methods=["POST"])
def initiate_payment(booking_ref):
    """
    Initiate Paystack transaction.
    In simulate mode → immediately mark as VERIFIED and confirm booking.
    In live mode → call Paystack API → redirect to their hosted page.
    """
    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,)
    ).fetchone()

    if not booking:
        abort(404)

    if booking["booking_status"] not in (BookingStatus.PENDING,):
        flash("This booking is no longer in a payable state.", "warning")
        return redirect(url_for("index"))

    # ── SIMULATE MODE ────────────────────────────────────────────────
    if PAYMENT_SIMULATE:
        sim_ref = f"SIM-{uuid.uuid4().hex[:12].upper()}"
        db.execute("""
            UPDATE bookings
            SET booking_status = ?,
                payment_status = ?,
                payment_ref    = ?,
                updated_at     = datetime('now','localtime')
            WHERE booking_ref = ?
        """, (BookingStatus.CONFIRMED, PaymentStatus.VERIFIED, sim_ref, booking_ref))
        db.commit()
        audit(db, booking_ref, "PAYMENT_SIMULATED", "system", sim_ref)
        db.commit()
        logger.info("Simulated payment for %s → %s", booking_ref, sim_ref)
        return redirect(url_for("confirmation", booking_ref=booking_ref))

    # ── LIVE PAYSTACK MODE ───────────────────────────────────────────
    email = booking["email"] or f"{booking['phone']}@maracana.ng"
    callback_url = url_for("payment_callback", _external=True)

    payload = {
        "email":        email,
        "amount":       booking["amount"] * 100,   # Paystack uses kobo
        "reference":    booking_ref,               # use booking_ref as Paystack ref
        "callback_url": callback_url,
        "metadata": {
            "booking_ref": booking_ref,
            "team_name":   booking["team_name"],
            "arena":       ARENA_NAME,
        }
    }
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type":  "application/json",
    }
    try:
        resp = requests.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            json=payload, headers=headers, timeout=10
        )
        data = resp.json()
        if data.get("status"):
            auth_url = data["data"]["authorization_url"]
            logger.info("Paystack init OK for %s → %s", booking_ref, auth_url)
            return redirect(auth_url)
        else:
            logger.error("Paystack init FAILED: %s", data)
            flash("Payment gateway error. Please try again.", "error")
            return redirect(url_for("payment_page", booking_ref=booking_ref))
    except requests.RequestException as e:
        logger.error("Paystack request error: %s", e)
        flash("Network error contacting payment gateway. Please try again.", "error")
        return redirect(url_for("payment_page", booking_ref=booking_ref))


@app.route("/pay/callback")
def payment_callback():
    """
    Paystack redirects here after customer completes payment on their page.
    We verify the transaction immediately.
    """
    reference = request.args.get("reference", "")
    if not reference:
        flash("Invalid payment callback.", "error")
        return redirect(url_for("index"))

    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref = ?", (reference,)
    ).fetchone()

    if not booking:
        flash("Booking not found for this payment.", "error")
        return redirect(url_for("index"))

    # Verify with Paystack
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    try:
        resp = requests.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers=headers, timeout=10
        )
        data = resp.json()
    except requests.RequestException as e:
        logger.error("Paystack verify error: %s", e)
        flash("Could not verify payment. Please contact the arena.", "error")
        return redirect(url_for("payment_page", booking_ref=reference))

    if data.get("status") and data["data"]["status"] == "success":
        db.execute("""
            UPDATE bookings
            SET booking_status = ?,
                payment_status = ?,
                payment_ref    = ?,
                updated_at     = datetime('now','localtime')
            WHERE booking_ref = ?
        """, (BookingStatus.CONFIRMED, PaymentStatus.VERIFIED,
              data["data"]["reference"], reference))
        db.commit()
        audit(db, reference, "PAYMENT_VERIFIED", "paystack",
              f"Paystack ref: {data['data']['reference']}")
        db.commit()
        logger.info("Payment VERIFIED for %s", reference)
        return redirect(url_for("confirmation", booking_ref=reference))
    else:
        db.execute("""
            UPDATE bookings
            SET booking_status = ?,
                payment_status = ?,
                updated_at     = datetime('now','localtime')
            WHERE booking_ref = ?
        """, (BookingStatus.FAILED, PaymentStatus.FAILED, reference))
        db.commit()
        audit(db, reference, "PAYMENT_FAILED", "paystack", str(data))
        db.commit()
        logger.warning("Payment FAILED for %s", reference)
        flash("Payment was not successful. Your slot has been released.", "error")
        return redirect(url_for("index"))
@app.route("/pay/webhook", methods=["POST"])
def paystack_webhook():
    """
    Paystack server-to-server webhook.
    Provides a second confirmation layer even if the callback redirect fails.
    Validates HMAC signature to reject forgeries.
    """
    signature = request.headers.get("X-Paystack-Signature", "")
    body      = request.get_data()

    # Validate signature
    expected = hmac.new(
        PAYSTACK_SECRET_KEY.encode(), body, hashlib.sha512
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        logger.warning("Webhook: invalid signature rejected")
        abort(400)

    event = json.loads(body)
    if event.get("event") == "charge.success":
        ref   = event["data"]["reference"]
        db    = get_db()
        existing = db.execute(
            "SELECT booking_status FROM bookings WHERE booking_ref=?", (ref,)
        ).fetchone()
        if existing and existing["booking_status"] != BookingStatus.CONFIRMED:
            db.execute("""
                UPDATE bookings
                SET booking_status=?, payment_status=?, updated_at=datetime('now','localtime')
                WHERE booking_ref=?
            """, (BookingStatus.CONFIRMED, PaymentStatus.VERIFIED, ref))
            db.commit()
            audit(db, ref, "WEBHOOK_CONFIRMED", "paystack_webhook")
            db.commit()
            logger.info("Webhook confirmed booking %s", ref)

    return jsonify({"status": "ok"})


@app.route("/confirmation/<booking_ref>")
def confirmation(booking_ref):
    """Show booking receipt after successful payment."""
    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref = ?", (booking_ref,)
    ).fetchone()

    if not booking:
        abort(404)

    ctx = arena_context()
    ctx["booking"] = dict(booking)
    return render_template("confirmation.html", **ctx)


# ══════════════════════════════════════════════════════════
#  ADMIN ROUTES
# ══════════════════════════════════════════════════════════

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            session.permanent = False
            audit(get_db(), None, "ADMIN_LOGIN", "admin", request.remote_addr)
            get_db().commit()
            return redirect(url_for("admin_dashboard"))
        flash("Incorrect password.", "error")
    ctx = arena_context()
    return render_template("admin_login.html", **ctx)


@app.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    """
    Main admin dashboard:
    - Today's schedule (all slots with status)
    - Summary stats
    - Recent bookings
    """
    db       = get_db()
    today_s  = date.today().isoformat()
    slot_map = get_slot_map(db, today_s)

    # Aggregate stats
    total     = db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    confirmed = db.execute("SELECT COUNT(*) FROM bookings WHERE booking_status='CONFIRMED'").fetchone()[0]
    pending   = db.execute("SELECT COUNT(*) FROM bookings WHERE booking_status='PENDING'").fetchone()[0]
    cancelled = db.execute("SELECT COUNT(*) FROM bookings WHERE booking_status='CANCELLED'").fetchone()[0]
    no_show   = db.execute("SELECT COUNT(*) FROM bookings WHERE booking_status='NO_SHOW'").fetchone()[0]
    revenue   = db.execute(
        "SELECT COALESCE(SUM(amount),0) FROM bookings WHERE payment_status='VERIFIED'"
    ).fetchone()[0]
    today_rev = db.execute(
        "SELECT COALESCE(SUM(amount),0) FROM bookings WHERE date=? AND payment_status='VERIFIED'",
        (today_s,)
    ).fetchone()[0]

    # Last 10 bookings
    recent = db.execute("""
        SELECT * FROM bookings
        ORDER BY created_at DESC LIMIT 10
    """).fetchall()

    ctx = arena_context()
    ctx.update({
        "slot_map":    slot_map,
        "TIME_SLOTS":  TIME_SLOTS,
        "today":       today_s,
        "stats": {
            "total": total, "confirmed": confirmed, "pending": pending,
            "cancelled": cancelled, "no_show": no_show,
            "revenue": revenue, "today_rev": today_rev,
        },
        "recent":      [dict(r) for r in recent],
    })
    return render_template("admin_dashboard.html", **ctx)


@app.route("/admin/bookings")
@admin_required
def admin_bookings():
    """Full bookings list with filters."""
    db            = get_db()
    filter_date   = request.args.get("date",   "")
    filter_status = request.args.get("status", "")
    filter_search = request.args.get("q",      "").strip()
    page          = max(1, int(request.args.get("page", 1)))
    per_page      = 25

    query  = "SELECT * FROM bookings WHERE 1=1"
    params = []

    if filter_date:
        query  += " AND date=?"
        params.append(filter_date)
    if filter_status:
        query  += " AND booking_status=?"
        params.append(filter_status)
    if filter_search:
        query  += " AND (team_name LIKE ? OR phone LIKE ? OR booking_ref LIKE ?)"
        like = f"%{filter_search}%"
        params.extend([like, like, like])

    total_count = db.execute(
        query.replace("SELECT *", "SELECT COUNT(*)"), params
    ).fetchone()[0]

    query  += f" ORDER BY date DESC, time_slot ASC LIMIT {per_page} OFFSET {(page-1)*per_page}"
    bookings = db.execute(query, params).fetchall()

    ctx = arena_context()
    ctx.update({
        "bookings":      [dict(b) for b in bookings],
        "filter_date":   filter_date,
        "filter_status": filter_status,
        "filter_search": filter_search,
        "page":          page,
        "per_page":      per_page,
        "total_count":   total_count,
        "total_pages":   max(1, -(-total_count // per_page)),
        "statuses":      [BookingStatus.PENDING, BookingStatus.CONFIRMED,
                          BookingStatus.CANCELLED, BookingStatus.FAILED,
                          BookingStatus.NO_SHOW, BookingStatus.PAY_VENUE],
    })
    return render_template("admin_bookings.html", **ctx)


@app.route("/admin/booking/<booking_ref>")
@admin_required
def admin_booking_detail(booking_ref):
    """Single booking detail view with full audit log."""
    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref=?", (booking_ref,)
    ).fetchone()
    if not booking:
        abort(404)

    logs = db.execute(
        "SELECT * FROM audit_log WHERE booking_ref=? ORDER BY created_at ASC",
        (booking_ref,)
    ).fetchall()

    ctx = arena_context()
    ctx.update({
        "booking": dict(booking),
        "logs":    [dict(l) for l in logs],
        "PRICE":   PRICE,
        "statuses": [BookingStatus.PENDING, BookingStatus.CONFIRMED,
                     BookingStatus.CANCELLED, BookingStatus.FAILED,
                     BookingStatus.NO_SHOW, BookingStatus.PAY_VENUE],
        "pstatuses": [PaymentStatus.PENDING, PaymentStatus.VERIFIED,
                      PaymentStatus.FAILED, PaymentStatus.WAIVED],
    })
    return render_template("admin_booking_detail.html", **ctx)


@app.route("/admin/booking/<booking_ref>/update", methods=["POST"])
@admin_required
def admin_update_booking(booking_ref):
    """Admin can update booking status, payment status, and notes."""
    db = get_db()
    booking = db.execute(
        "SELECT * FROM bookings WHERE booking_ref=?", (booking_ref,)
    ).fetchone()
    if not booking:
        abort(404)

    new_bs  = request.form.get("booking_status", booking["booking_status"])
    new_ps  = request.form.get("payment_status", booking["payment_status"])
    notes   = request.form.get("notes", booking["notes"] or "").strip()

    db.execute("""
        UPDATE bookings
        SET booking_status=?, payment_status=?, notes=?,
            updated_at=datetime('now','localtime')
        WHERE booking_ref=?
    """, (new_bs, new_ps, notes, booking_ref))
    db.commit()
    audit(db, booking_ref, "ADMIN_UPDATE", "admin",
          f"bs:{new_bs} ps:{new_ps}")
    db.commit()
    flash(f"Booking {booking_ref} updated.", "success")
    return redirect(url_for("admin_booking_detail", booking_ref=booking_ref))


@app.route("/admin/booking/create", methods=["GET", "POST"])
@admin_required
def admin_create_booking():
    """
    Admin manually creates a booking (walk-in, phone call, etc.)
    Can set status to PAY_VENUE to bypass online payment.
    """
    db = get_db()

    if request.method == "GET":
        selected_date = request.args.get("date", date.today().isoformat())
        slot_map      = get_slot_map(db, selected_date)
        available     = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]
        ctx = arena_context()
        ctx.update({
            "available_slots": available,
            "selected_date":   selected_date,
            "PRICE":           PRICE,
            "all_slots":       TIME_SLOTS,
        })
        return render_template("admin_create_booking.html", **ctx)

    # POST
    team_name  = request.form.get("team_name",  "").strip()
    phone      = request.form.get("phone",      "").strip()
    email      = request.form.get("email",      "").strip()
    time_slot  = request.form.get("time_slot",  "").strip()
    book_date  = request.form.get("date",       "").strip()
    pitch_type = request.form.get("pitch_type", "5-aside").strip()
    pay_venue  = request.form.get("pay_venue")  # checkbox
    notes      = request.form.get("notes", "").strip()

    errors = []
    if not team_name: errors.append("Team name required.")
    if not phone:     errors.append("Phone required.")
    if time_slot not in TIME_SLOTS: errors.append("Select a valid time slot.")
    if not book_date: errors.append("Date required.")

    if errors:
        slot_map  = get_slot_map(db, book_date or date.today().isoformat())
        available = [s for s in TIME_SLOTS if slot_map[s]["status"] == "available"]
        ctx = arena_context()
        ctx.update({
            "errors":          errors,
            "available_slots": available,
            "selected_date":   book_date,
            "form_data":       request.form,
            "PRICE":           PRICE,
            "all_slots":       TIME_SLOTS,
        })
        return render_template("admin_create_booking.html", **ctx)

    amount      = PRICE.get(pitch_type, 15_000)
    booking_ref = next_booking_ref(db)
    bs          = BookingStatus.PAY_VENUE if pay_venue else BookingStatus.CONFIRMED
    ps          = PaymentStatus.WAIVED    if pay_venue else PaymentStatus.VERIFIED

    try:
        db.execute("""
            INSERT INTO bookings
              (booking_ref, team_name, phone, email, time_slot, date,
               pitch_type, amount, booking_status, payment_status, notes, created_by)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,'admin')
        """, (booking_ref, team_name, phone, email or None,
              time_slot, book_date, pitch_type, amount, bs, ps, notes or None))
        db.commit()
        audit(db, booking_ref, "ADMIN_CREATED", "admin",
              f"{team_name} | {book_date} | {time_slot} | {bs}")
        db.commit()
        flash(f"Booking {booking_ref} created successfully.", "success")
        return redirect(url_for("admin_booking_detail", booking_ref=booking_ref))

    except sqlite3.IntegrityError:
        ctx = arena_context()
        ctx.update({
            "errors":          ["That slot is already taken for this date."],
            "available_slots": [],
            "selected_date":   book_date,
            "form_data":       request.form,
            "PRICE":           PRICE,
            "all_slots":       TIME_SLOTS,
        })
        return render_template("admin_create_booking.html", **ctx)


@app.route("/admin/booking/<booking_ref>/delete", methods=["POST"])
@admin_required
def admin_delete_booking(booking_ref):
    """Hard-delete a booking (use sparingly; prefer CANCELLED status)."""
    db = get_db()
    db.execute("DELETE FROM bookings WHERE booking_ref=?", (booking_ref,))
    db.commit()
    audit(db, booking_ref, "ADMIN_DELETED", "admin")
    db.commit()
    flash(f"Booking {booking_ref} permanently deleted.", "warning")
    return redirect(url_for("admin_bookings"))


@app.route("/admin/booking/<booking_ref>/no-show", methods=["POST"])
@admin_required
def admin_mark_no_show(booking_ref):
    db = get_db()
    db.execute("""
        UPDATE bookings SET booking_status='NO_SHOW',
        updated_at=datetime('now','localtime') WHERE booking_ref=?
    """, (booking_ref,))
    db.commit()
    audit(db, booking_ref, "MARKED_NO_SHOW", "admin")
    db.commit()
    flash(f"{booking_ref} marked as No-Show.", "warning")
    return redirect(request.referrer or url_for("admin_dashboard"))


# ── Schedule / blocking ────────────────────────────────────────────────

@app.route("/admin/schedule")
@admin_required
def admin_schedule():
    """Admin view: full week schedule with block/unblock controls."""
    db = get_db()

    # Build 7-day view from today
    start  = date.today()
    days   = [(start + timedelta(days=i)).isoformat() for i in range(7)]
    week   = {}
    for d in days:
        week[d] = get_slot_map(db, d)

    # Blocked periods
    blocks = db.execute(
        "SELECT * FROM blocked_periods ORDER BY date, time_slot"
    ).fetchall()

    ctx = arena_context()
    ctx.update({
        "week":      week,
        "days":      days,
        "TIME_SLOTS": TIME_SLOTS,
        "blocks":    [dict(b) for b in blocks],
    })
    return render_template("admin_schedule.html", **ctx)


@app.route("/admin/block", methods=["POST"])
@admin_required
def admin_block_slot():
    """Block a specific slot or entire day."""
    db        = get_db()
    block_date = request.form.get("date", "").strip()
    time_slot  = request.form.get("time_slot", "").strip() or None  # None = full day
    reason     = request.form.get("reason", "Maintenance").strip()

    if not block_date:
        flash("Date is required.", "error")
        return redirect(url_for("admin_schedule"))

    try:
        db.execute(
            "INSERT OR IGNORE INTO blocked_periods (date, time_slot, reason) VALUES (?,?,?)",
            (block_date, time_slot, reason)
        )
        db.commit()
        label = time_slot or "FULL DAY"
        audit(db, None, "SLOT_BLOCKED", "admin", f"{block_date} {label} — {reason}")
        db.commit()
        flash(f"{'Full day' if not time_slot else time_slot} on {block_date} blocked.", "success")
    except sqlite3.IntegrityError:
        flash("That slot/day is already blocked.", "warning")

    return redirect(url_for("admin_schedule"))


@app.route("/admin/unblock/<int:block_id>", methods=["POST"])
@admin_required
def admin_unblock_slot(block_id):
    db = get_db()
    db.execute("DELETE FROM blocked_periods WHERE id=?", (block_id,))
    db.commit()
    audit(db, None, "SLOT_UNBLOCKED", "admin", f"block_id={block_id}")
    db.commit()
    flash("Block removed.", "success")
    return redirect(url_for("admin_schedule"))


# ══════════════════════════════════════════════════════════
#  JSON API (for AJAX calls)
# ══════════════════════════════════════════════════════════

@app.route("/api/slots")
def api_slots():
    """Return slot availability for a date as JSON."""
    req_date = request.args.get("date", date.today().isoformat())
    db       = get_db()
    slot_map = get_slot_map(db, req_date)
    result   = [
        {
            "slot":      s,
            "status":    slot_map[s]["status"],
            "available": slot_map[s]["status"] == "available",
        }
        for s in TIME_SLOTS
    ]
    return jsonify(result)


@app.route("/api/booking/<booking_ref>")
def api_booking_status(booking_ref):
    """Polling endpoint — lets the payment page check if booking is confirmed."""
    db = get_db()
    b  = db.execute(
        "SELECT booking_status, payment_status FROM bookings WHERE booking_ref=?",
        (booking_ref,)
    ).fetchone()
    if not b:
        return jsonify({"error": "not found"}), 404
    return jsonify({"booking_status": b["booking_status"], "payment_status": b["payment_status"]})


# ══════════════════════════════════════════════════════════
#  ERROR HANDLERS
# ══════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(e):
    ctx = arena_context()
    return render_template("404.html", **ctx), 404


@app.errorhandler(500)
def server_error(e):
    logger.exception("Internal server error")
    ctx = arena_context()
    return render_template("500.html", **ctx), 500


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    init_db()
    logger.info("🏟️  %s Booking System starting...", ARENA_NAME)
    logger.info("👉  http://127.0.0.1:5000")
    logger.info("🔑  Admin: http://127.0.0.1:5000/admin  (password: %s)", ADMIN_PASSWORD)
    logger.info("💳  Payment mode: %s", "SIMULATE" if PAYMENT_SIMULATE else "LIVE (Paystack)")
    app.run(debug=True, host="0.0.0.0", port=5000)