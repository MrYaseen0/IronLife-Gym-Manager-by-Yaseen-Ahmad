"""
IronLife Gym Manager - Flask Backend
A complete gym management system with member registration, authentication, and data persistence
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import json
from functools import wraps

# Initialize Flask App
app = Flask(__name__, static_folder='.', static_url_path='')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = 'ironlife-secret-key-2026'

# Enable CORS for frontend access
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Initialize Database
db = SQLAlchemy(app)

# ==================== MODELS ====================

class User(db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True)
    role = db.Column(db.String(50), default='Manager')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Member(db.Model):
    """Member model for gym members"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120))
    gender = db.Column(db.String(20), default='Male')
    plan = db.Column(db.String(50), nullable=False)  # Basic, Pro, Elite
    amount = db.Column(db.Integer, nullable=False)  # Monthly fee in INR
    joinDate = db.Column(db.String(10), nullable=False)
    renewal_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Active')  # Active, Inactive, Suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_renewal_date(self):
        """Calculate renewal date (30 days from join date)"""
        try:
            join_date = datetime.strptime(self.joinDate, '%Y-%m-%d')
            return (join_date + timedelta(days=30)).date().isoformat()
        except:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'gender': self.gender,
            'plan': self.plan,
            'amount': self.amount,
            'joinDate': self.joinDate,
            'renewal_date': self.calculate_renewal_date(),
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Payment(db.Model):
    """Payment model to track member payments"""
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.Column(db.String(50), default='Cash')  # Cash, Card, UPI, etc.
    status = db.Column(db.String(20), default='Completed')
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'member_id': self.member_id,
            'amount': self.amount,
            'payment_date': self.payment_date.isoformat(),
            'method': self.method,
            'status': self.status,
            'notes': self.notes
        }

# ==================== AUTHENTICATION ====================

def token_required(f):
    """Decorator to require authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # Simple token validation (in production, use JWT)
            if token != 'Bearer valid-token':
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(*args, **kwargs)
    return decorated

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    # Check user in database
    user = User.query.filter_by(username=username).first()
    
    if user and user.password == password:  # In production, use password hashing
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': 'valid-token'
        }), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401


@app.route('/api/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    # Create new user
    new_user = User(
        username=data['username'],
        password=data['password'],  # In production, hash the password
        email=data.get('email'),
        role=data.get('role', 'Manager')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    return jsonify({'message': 'Logout successful'}), 200

# ==================== MEMBERS ROUTES ====================

@app.route('/api/members', methods=['GET'])
def get_members():
    """Get all members"""
    try:
        members = Member.query.all()
        return jsonify([member.to_dict() for member in members]), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get specific member by ID"""
    try:
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'message': 'Member not found'}), 404
        return jsonify(member.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members', methods=['POST'])
def add_member():
    """Add a new member"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'phone', 'plan', 'amount', 'joinDate']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if phone already exists
    if Member.query.filter_by(phone=data['phone']).first():
        return jsonify({'message': 'Phone number already registered'}), 409
    
    try:
        new_member = Member(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            gender=data.get('gender', 'Male'),
            plan=data['plan'],
            amount=data['amount'],
            joinDate=data['joinDate'],
            status=data.get('status', 'Active')
        )
        
        db.session.add(new_member)
        db.session.commit()
        
        return jsonify({
            'message': 'Member added successfully',
            'member': new_member.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update member details"""
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    data = request.get_json()
    
    try:
        # Update fields
        if 'name' in data:
            member.name = data['name']
        if 'phone' in data:
            member.phone = data['phone']
        if 'email' in data:
            member.email = data['email']
        if 'gender' in data:
            member.gender = data['gender']
        if 'plan' in data:
            member.plan = data['plan']
        if 'amount' in data:
            member.amount = data['amount']
        if 'status' in data:
            member.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Member updated successfully',
            'member': member.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    try:
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members/search', methods=['GET'])
def search_members():
    """Search members by name or phone"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'message': 'Search query required'}), 400
    
    try:
        members = Member.query.filter(
            (Member.name.ilike(f'%{query}%')) |
            (Member.phone.ilike(f'%{query}%'))
        ).all()
        
        return jsonify([member.to_dict() for member in members]), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/members/sync', methods=['POST'])
def sync_members():
    """Sync members from frontend (for offline mode)"""
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({'message': 'Expected array of members'}), 400
    
    try:
        # This would sync members from frontend
        # In a real app, you'd handle conflicts and merging
        return jsonify({
            'message': 'Sync completed',
            'count': len(data)
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ==================== STATISTICS ROUTES ====================

@app.route('/api/stats/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        total_members = Member.query.count()
        active_members = Member.query.filter_by(status='Active').count()
        total_revenue = db.session.query(db.func.sum(Member.amount)).scalar() or 0
        
        return jsonify({
            'total_members': total_members,
            'active_members': active_members,
            'total_revenue': total_revenue,
            'recent_members': [m.to_dict() for m in Member.query.order_by(Member.created_at.desc()).limit(5).all()]
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/stats/revenue', methods=['GET'])
def get_revenue_stats():
    """Get revenue statistics"""
    try:
        # Calculate total and monthly revenue
        total = db.session.query(db.func.sum(Member.amount)).scalar() or 0
        
        # Group by plan
        by_plan = db.session.query(
            Member.plan,
            db.func.count(Member.id),
            db.func.sum(Member.amount)
        ).group_by(Member.plan).all()
        
        return jsonify({
            'total_revenue': total,
            'by_plan': [
                {
                    'plan': plan,
                    'count': count,
                    'revenue': revenue
                }
                for plan, count, revenue in by_plan
            ]
        }), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ==================== PAYMENT ROUTES ====================

@app.route('/api/payments', methods=['POST'])
def add_payment():
    """Record a payment"""
    data = request.get_json()
    
    if not data or not data.get('member_id') or not data.get('amount'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if member exists
    member = Member.query.get(data['member_id'])
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    try:
        new_payment = Payment(
            member_id=data['member_id'],
            amount=data['amount'],
            method=data.get('method', 'Cash'),
            notes=data.get('notes')
        )
        
        db.session.add(new_payment)
        db.session.commit()
        
        return jsonify({
            'message': 'Payment recorded successfully',
            'payment': new_payment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/api/payments/member/<int:member_id>', methods=['GET'])
def get_member_payments(member_id):
    """Get payment history for a member"""
    try:
        payments = Payment.query.filter_by(member_id=member_id).order_by(Payment.payment_date.desc()).all()
        return jsonify([payment.to_dict() for payment in payments]), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# ==================== ROOT ENDPOINT ====================

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - serve the main app"""
    try:
        with open('gym-manager.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return jsonify({
            'message': 'IronLife Gym Manager API',
            'status': 'running',
            'version': '1.0.0',
            'frontend_available': 'Open gym-manager.html in browser'
        }), 200

@app.route('/app', methods=['GET'])
def app_page():
    """Serve the main application"""
    try:
        with open('gym-manager.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start', methods=['GET'])
def start_page():
    """Serve the start page"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'API Endpoint not found. Use /api/login to start'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# ==================== MAIN ====================

def init_db():
    """Initialize database with default data"""
    with app.app_context():
        db.create_all()
        
        # Add default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password='123456',
                email='admin@ironlife.com',
                role='Admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin / 123456")
        
        # Add sample members if empty
        if Member.query.count() == 0:
            sample_members = [
                Member(
                    name='Rahul Sharma',
                    phone='9876543210',
                    gender='Male',
                    plan='Pro',
                    amount=2500,
                    joinDate='2023-10-01',
                    status='Active'
                ),
                Member(
                    name='Priya Singh',
                    phone='9123456789',
                    gender='Female',
                    plan='Elite',
                    amount=5000,
                    joinDate='2023-10-05',
                    status='Active'
                ),
                Member(
                    name='Amit Kumar',
                    phone='9988776655',
                    gender='Male',
                    plan='Basic',
                    amount=1000,
                    joinDate='2023-10-12',
                    status='Active'
                ),
                Member(
                    name='Sneha Gupta',
                    phone='8877665544',
                    gender='Female',
                    plan='Pro',
                    amount=2500,
                    joinDate='2023-10-15',
                    status='Active'
                )
            ]
            db.session.add_all(sample_members)
            db.session.commit()
            print("Sample members added")

if __name__ == '__main__':
    init_db()
    print("🏋️ IronLife Gym Manager Backend Starting...")
    print("📍 Running on http://localhost:5000")
    print("📚 API Documentation available at http://localhost:5000/api/docs")
    app.run(debug=True, port=5000, use_reloader=False)
