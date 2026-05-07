"""
Football Arena Booking System - Flask Application
Production-ready MVP for Maracana Football Arena Kano
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from functools import wraps
import os
import secrets
import string
from decimal import Decimal

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Booking(db.Model):
    """Booking model for storing arena reservations"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    team_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(10), nullable=False)
    arena_name = db.Column(db.String(100), nullable=False, default='Maracana Football Arena Kano')
    payment_status = db.Column(db.String(20), nullable=False, default='PENDING')  # PENDING, PAID, FAILED
    payment_method = db.Column(db.String(20), nullable=False)  # TRANSFER, CARD
    payment_reference = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=5000.00)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint on date and time_slot to prevent double booking
    __table_args__ = (
        db.UniqueConstraint('date', 'time_slot', name='unique_booking_slot'),
    )
    
    def to_dict(self):
        """Convert booking to dictionary"""
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'team_name': self.team_name,
            'phone': self.phone,
            'date': self.date.strftime('%Y-%m-%d'),
            'time_slot': self.time_slot,
            'arena_name': self.arena_name,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'amount': float(self.amount),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

ARENA_NAME = 'Maracana Football Arena Kano'
BOOKING_AMOUNT = Decimal('5000.00')
BOOKING_CURRENCY = 'NGN'

# Available time slots
TIME_SLOTS = [
    '09:00-10:00',
    '10:00-11:00',
    '11:00-12:00',
    '14:00-15:00',
    '15:00-16:00',
    '16:00-17:00',
    '17:00-18:00',
    '18:00-19:00',
]

# Bank details for transfer payments
BANK_DETAILS = {
    'bank_name': 'Zenith Bank',
    'account_number': '1234567890',
    'account_name': 'Maracana Football Arena Kano',
    'amount': float(BOOKING_AMOUNT),
}

# Admin credentials (in production, use proper authentication)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # Change in production

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_booking_id():
    """Generate unique booking ID"""
    prefix = 'MFA'
    timestamp = datetime.now().strftime('%Y%m%d')
    random_suffix = ''.join(secrets.choice(string.digits) for _ in range(4))
    return f"{prefix}{timestamp}{random_suffix}"

def is_slot_available(date, time_slot):
    """Check if a time slot is available"""
    booking = Booking.query.filter_by(date=date, time_slot=time_slot).first()
    return booking is None

def get_available_slots(date):
    """Get available slots for a given date"""
    booked_slots = Booking.query.filter_by(date=date).with_entities(Booking.time_slot).all()
    booked_slot_list = [slot[0] for slot in booked_slots]
    return [slot for slot in TIME_SLOTS if slot not in booked_slot_list]

def validate_booking_input(team_name, phone, date_str, time_slot):
    """Validate booking input"""
    errors = []
    
    if not team_name or len(team_name.strip()) < 2:
        errors.append('Team name must be at least 2 characters')
    
    if not phone or len(phone) < 10:
        errors.append('Phone number must be at least 10 digits')
    
    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if booking_date < datetime.now().date():
            errors.append('Cannot book for past dates')
    except ValueError:
        errors.append('Invalid date format')
        booking_date = None
    
    if time_slot not in TIME_SLOTS:
        errors.append('Invalid time slot')
    
    if booking_date and not is_slot_available(booking_date, time_slot):
        errors.append('This time slot is already booked')
    
    return errors, booking_date if not errors else None

def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please log in to access admin panel', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# ROUTES - PUBLIC PAGES
# ============================================================================

@app.route('/')
def index():
    """Homepage with available slots"""
    today = datetime.now().date()
    next_30_days = [today + timedelta(days=i) for i in range(30)]
    
    return render_template('index.html', 
                         arena_name=ARENA_NAME,
                         next_30_days=next_30_days,
                         time_slots=TIME_SLOTS)

@app.route('/api/available-slots')
def api_available_slots():
    """API endpoint to get available slots for a date"""
    date_str = request.args.get('date')
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date < datetime.now().date():
            return jsonify({'error': 'Cannot book for past dates'}), 400
        
        available_slots = get_available_slots(date)
        return jsonify({'available_slots': available_slots})
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

@app.route('/book', methods=['GET', 'POST'])
def book():
    """Booking page"""
    if request.method == 'POST':
        team_name = request.form.get('team_name', '').strip()
        phone = request.form.get('phone', '').strip()
        date_str = request.form.get('date', '')
        time_slot = request.form.get('time_slot', '')
        payment_method = request.form.get('payment_method', 'TRANSFER')
        
        # Validate input
        errors, booking_date = validate_booking_input(team_name, phone, date_str, time_slot)
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('book'))
        
        try:
            # Create booking
            booking_id = generate_booking_id()
            booking = Booking(
                booking_id=booking_id,
                team_name=team_name,
                phone=phone,
                date=booking_date,
                time_slot=time_slot,
                arena_name=ARENA_NAME,
                payment_method=payment_method,
                amount=BOOKING_AMOUNT,
                payment_status='PENDING'
            )
            
            db.session.add(booking)
            db.session.commit()
            
            # Store booking ID in session for receipt
            session['booking_id'] = booking_id
            
            flash(f'Booking created successfully! Booking ID: {booking_id}', 'success')
            return redirect(url_for('payment', booking_id=booking_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating booking: {str(e)}', 'error')
            return redirect(url_for('book'))
    
    today = datetime.now().date()
    next_30_days = [today + timedelta(days=i) for i in range(30)]
    
    return render_template('book.html',
                         arena_name=ARENA_NAME,
                         next_30_days=next_30_days,
                         time_slots=TIME_SLOTS,
                         bank_details=BANK_DETAILS,
                         booking_amount=float(BOOKING_AMOUNT))

@app.route('/payment/<booking_id>', methods=['GET', 'POST'])
def payment(booking_id):
    """Payment page"""
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method', 'TRANSFER')
        payment_reference = request.form.get('payment_reference', '').strip()
        
        if payment_method == 'TRANSFER':
            if not payment_reference:
                flash('Please provide payment reference', 'error')
                return redirect(url_for('payment', booking_id=booking_id))
            
            booking.payment_reference = payment_reference
            booking.payment_status = 'PENDING'
            booking.payment_method = 'TRANSFER'
        
        elif payment_method == 'CARD':
            # In production, integrate with Paystack
            booking.payment_status = 'PAID'
            booking.payment_method = 'CARD'
            booking.payment_reference = f'PAYSTACK-{booking_id}'
        
        db.session.commit()
        flash('Payment recorded. Your booking is confirmed!', 'success')
        return redirect(url_for('receipt', booking_id=booking_id))
    
    return render_template('payment.html',
                         booking=booking,
                         bank_details=BANK_DETAILS,
                         arena_name=ARENA_NAME)

@app.route('/receipt/<booking_id>')
def receipt(booking_id):
    """Receipt page"""
    booking = Booking.query.filter_by(booking_id=booking_id).first()
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('index'))
    
    return render_template('receipt.html',
                         booking=booking,
                         arena_name=ARENA_NAME,
                         currency=BOOKING_CURRENCY)

# ============================================================================
# ROUTES - ADMIN PAGES
# ============================================================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Logged in successfully', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    page = request.args.get('page', 1, type=int)
    payment_status = request.args.get('status', '', type=str)
    
    query = Booking.query
    
    if payment_status and payment_status in ['PENDING', 'PAID', 'FAILED']:
        query = query.filter_by(payment_status=payment_status)
    
    # Paginate results
    bookings = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=20)
    
    # Statistics
    total_bookings = Booking.query.count()
    pending_payments = Booking.query.filter_by(payment_status='PENDING').count()
    paid_bookings = Booking.query.filter_by(payment_status='PAID').count()
    total_revenue = db.session.query(db.func.sum(Booking.amount)).filter_by(payment_status='PAID').scalar() or 0
    
    stats = {
        'total_bookings': total_bookings,
        'pending_payments': pending_payments,
        'paid_bookings': paid_bookings,
        'total_revenue': float(total_revenue),
    }
    
    return render_template('admin_dashboard.html',
                         bookings=bookings,
                         stats=stats,
                         current_status=payment_status,
                         arena_name=ARENA_NAME)

@app.route('/admin/booking/<int:booking_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(booking_id):
    """Confirm transfer payment"""
    booking = Booking.query.get(booking_id)
    
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    
    booking.payment_status = 'PAID'
    db.session.commit()
    
    flash(f'Payment confirmed for booking {booking.booking_id}', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/booking/<int:booking_id>/delete', methods=['POST'])
@login_required
def delete_booking(booking_id):
    """Delete booking"""
    booking = Booking.query.get(booking_id)
    
    if not booking:
        flash('Booking not found', 'error')
        return redirect(url_for('admin_dashboard'))
    
    booking_ref = booking.booking_id
    db.session.delete(booking)
    db.session.commit()
    
    flash(f'Booking {booking_ref} deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/api/bookings')
@login_required
def api_bookings():
    """API endpoint for bookings data (JSON export)"""
    bookings = Booking.query.all()
    return jsonify([booking.to_dict() for booking in bookings])

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# ============================================================================
# CONTEXT PROCESSORS
# ============================================================================

@app.context_processor
def inject_config():
    """Inject configuration into templates"""
    return {
        'arena_name': ARENA_NAME,
        'booking_amount': float(BOOKING_AMOUNT),
        'currency': BOOKING_CURRENCY,
    }

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)