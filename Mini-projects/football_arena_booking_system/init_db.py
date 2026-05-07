"""
Database initialization script for Football Arena Booking System
Run this script to create and initialize the database with sample data
"""

from app import app, db, Booking
from datetime import datetime, timedelta
from decimal import Decimal

def init_database():
    """Initialize database with tables"""
    with app.app_context():
        # Drop all tables (for fresh start)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        print("✓ Database tables created successfully")
        
        # Add sample bookings for demonstration
        sample_bookings = [
            Booking(
                booking_id='MFA20260420001',
                team_name='Manchester United FC',
                phone='08012345678',
                date=datetime.now().date() + timedelta(days=1),
                time_slot='09:00-10:00',
                arena_name='Maracana Football Arena Kano',
                payment_status='PAID',
                payment_method='TRANSFER',
                payment_reference='TRF-001-20260420',
                amount=Decimal('5000.00'),
            ),
            Booking(
                booking_id='MFA20260420002',
                team_name='Liverpool FC Kano',
                phone='08098765432',
                date=datetime.now().date() + timedelta(days=2),
                time_slot='14:00-15:00',
                arena_name='Maracana Football Arena Kano',
                payment_status='PENDING',
                payment_method='TRANSFER',
                payment_reference='TRF-002-20260420',
                amount=Decimal('5000.00'),
            ),
            Booking(
                booking_id='MFA20260420003',
                team_name='Arsenal Kano',
                phone='08055555555',
                date=datetime.now().date() + timedelta(days=3),
                time_slot='17:00-18:00',
                arena_name='Maracana Football Arena Kano',
                payment_status='PAID',
                payment_method='CARD',
                payment_reference='PAYSTACK-MFA20260420003',
                amount=Decimal('5000.00'),
            ),
        ]
        
        for booking in sample_bookings:
            db.session.add(booking)
        
        db.session.commit()
        
        print(f"✓ Added {len(sample_bookings)} sample bookings")
        
        # Display database info
        total_bookings = Booking.query.count()
        print(f"\nDatabase Summary:")
        print(f"  Total Bookings: {total_bookings}")
        print(f"  Paid Bookings: {Booking.query.filter_by(payment_status='PAID').count()}")
        print(f"  Pending Bookings: {Booking.query.filter_by(payment_status='PENDING').count()}")
        
        print("\n✓ Database initialization complete!")
        print("\nAdmin Credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nNext steps:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000")
        print("  3. Admin panel: http://localhost:5000/admin/login")

if __name__ == '__main__':
    init_database()