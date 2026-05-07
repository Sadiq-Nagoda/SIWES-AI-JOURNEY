"""
Quick-start script. Run this instead of app.py directly.
Usage: python run.py
"""
from app import app, init_db, ARENA_NAME, ADMIN_PASSWORD, PAYMENT_SIMULATE
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    init_db()
    print(f"\n{'='*55}")
    print(f"  🏟️  {ARENA_NAME}")
    print(f"{'='*55}")
    print(f"  🌍  Public site:  http://127.0.0.1:5000")
    print(f"  🔐  Admin panel:  http://127.0.0.1:5000/admin")
    print(f"  🔑  Password:     {ADMIN_PASSWORD}")
    print(f"  💳  Payments:     {'SIMULATE (no real money)' if PAYMENT_SIMULATE else 'LIVE - Paystack'}")
    print(f"{'='*55}\n")
    app.run(debug=True, host="0.0.0.0", port=5000)