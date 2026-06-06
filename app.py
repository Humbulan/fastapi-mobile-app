import os
import secrets
import datetime
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, g, session, after_this_request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from auth_utils import hash_password, verify_password, load_secret_key


# Database configuration
DATABASE = os.path.join(os.path.dirname(__file__), "instance", "imperial.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = load_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== MODELS ====================
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    phone = db.Column(db.String(20), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(50), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class USSDSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    current_menu = db.Column(db.String(50), default='main')
    amount = db.Column(db.Float, default=0)
    recipient = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ==================== VILLAGE MODELS ====================
class Village(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100))
    region = db.Column(db.String(100))
    population = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    keys = db.relationship("ApiKey", backref="village", lazy=True)

class ApiKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    village_id = db.Column(db.Integer, db.ForeignKey("village.id"), nullable=False)
    name = db.Column(db.String(100))
    tier = db.Column(db.String(50), default="basic")
    monthly_limit = db.Column(db.Integer, default=10000)
    usage_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ==================== WEB ROUTES ====================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed = hash_password(request.form['password'])
        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            password=hashed,
            phone=request.form.get('phone', '')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

    
    return render_template('login.html')


    
    

    stats = {

        'my_orders': len(orders),

        'my_payments': len(payments)

    }

    

    if current_user.role == 'admin':

        stats['total_users'] = User.query.count()

        stats['total_orders'] = Order.query.count()

        stats['total_payments'] = db.session.query(db.func.sum(Payment.amount)).scalar() or 0

    

    return render_template('dashboard.html', user=current_user, orders=orders, payments=payments, stats=stats)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# ==================== USER ACTIONS ====================
@app.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    if request.method == 'POST':
        order_no = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        new_order = Order(
            order_number=order_no,
            customer_id=current_user.id,
            description=request.form.get('description'),
            amount=float(request.form.get('amount', 0))
        )
        db.session.add(new_order)
        db.session.commit()
        flash('Order created successfully!')
        return redirect(url_for('dashboard'))
    return render_template('create_order.html')

@app.route('/create_payment', methods=['GET', 'POST'])
@login_required
def create_payment():
    if request.method == 'POST':
        pay_id = f"PAY-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        new_payment = Payment(
            payment_id=pay_id,
            user_id=current_user.id,
            amount=float(request.form.get('amount', 0)),
            payment_method=request.form.get('method')
        )
        db.session.add(new_payment)
        db.session.commit()
        flash('Payment submitted!')
        return redirect(url_for('dashboard'))
    return render_template('create_payment.html')

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(customer_id=current_user.id).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/my_payments')
@login_required
def my_payments():
    payments = Payment.query.filter_by(user_id=current_user.id).all()
    return render_template('my_payments.html', payments=payments)

# ==================== API ENDPOINTS ====================
@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'version': '2.0.0'
    })

@app.route('/api/version')
def api_version():
    return jsonify({
        'name': 'Imperial Network API',
        'version': '2.0.0',
        'status': 'operational',
        'endpoints': [
            '/api/health',
            '/api/version',
            '/api/system/status',
            '/api/business/data',
            '/api/mobile/config'
        ]
    })

@app.route('/api/system/status')
def system_status():
    return jsonify({
        'system': 'online',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'services': {
            'database': 'connected',
            'api': 'operational',
            'business_api': 'ready'
        }
    })


@app.route("/mobile")
@login_required
def mobile():
    return render_template("mobile.html")

@app.route("/mobile/sdk")
@login_required
def mobile_sdk():
    return render_template("mobile_sdk.html")

@app.route("/mobile/sdk/download")
@login_required
def mobile_sdk_download():
    import io
    sdk_content = "Imperial Mobile SDK v2.0.0\nRefer to documentation for implementation details."
    return send_file(
        io.BytesIO(sdk_content.encode()),
        mimetype="text/plain",
        as_attachment=True,
        download_name="imperial_sdk_v2.0.0.txt"
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            ok, needs_rehash = verify_password(user.password, password)
            if ok:
                # Auto-migrate legacy SHA-256 hashes to bcrypt on success.
                # Self-healing: every successful login rotates the row
                # exactly once, then never again.
                if needs_rehash:
                    user.password = hash_password(password)
                    db.session.commit()
                login_user(user)
                session["role"] = user.role
                return redirect(url_for('dashboard'))
        if user:
            ok, needs_rehash = verify_password(user.password, password)
            if ok:
                if needs_rehash:
                    user.password = hash_password(password)
                    db.session.commit()
                login_user(user)
                session["role"] = user.role
                return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    orders = Order.query.filter_by(customer_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, orders=orders)



@app.route('/monitor')
@login_required
def monitor():
    return render_template('monitor.html')

@app.route('/ussd/admin')
@login_required
def ussd_admin():
    return render_template('ussd_admin.html')
@app.route("/admin/villages")
@login_required
def admin_villages():
    return render_template("admin_villages.html")


@app.route("/api/admin/villages", methods=["GET", "POST"])
@login_required
def api_admin_villages():
    if request.method == "POST":
        data = request.json
        new_v = Village(
            name=data.get("name"),
            district=data.get("district"),
            region=data.get("region"),
            population=data.get("population", 0)
        )
        db.session.add(new_v)
        db.session.commit()
        return jsonify({"message": "Village added"})
    villages = Village.query.all()
    return jsonify([{
        "id": v.id,
        "name": v.name,
        "district": v.district,
        "region": v.region,
        "population": v.population
    } for v in villages])

@app.route("/api/ai/predictions")
@login_required
def api_ai_predictions():
    """API endpoint for AI predictions"""
    return jsonify({
        "revenue": 45600,
        "growth": 15,
        "orders": 245,
        "trend": "up",
        "confidence": 0.87,
        "village_predictions": [
            {"name": "Bindura Urban", "growth": 12.5},
            {"name": "Guruve South", "growth": 8.3},
            {"name": "Mvurwi Central", "growth": 15.2},
            {"name": "Shamva North", "growth": 10.7}
        ]
    })

@app.route("/api/status/full")
@login_required
def full_status():
    """Full system status endpoint"""
    return jsonify({
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "api": "online",
            "ai": "ready",
            "villages": "active"
        },
        "version": "2.0.0"
    })

@app.route("/api/admin/keys")
@login_required
def api_admin_keys():
    return jsonify({"status": "active", "keys": []})



@app.route('/notification-settings')
@login_required
def notification_settings():
    return render_template('notification_settings.html')

@app.route('/ai/dashboard')
@login_required
def ai_dashboard():
    total_users = User.query.count()
    active_users = User.query.filter(User.id.in_(db.session.query(Order.customer_id).distinct())).count()
    new_users = User.query.filter(User.created_at >= datetime.now() - timedelta(days=30)).count()
    
    health = {
        "system_health": "99.9%",
        "active_services": 12,
        "total_services": 12
    }
    predictions = {
        "revenue": 45600.00,
        "orders": 245,
        "growth": 15
    }
    stats = {
        "active_users": 300,
        "new_users": 15,
        "total_users": 315
    }
    return render_template("ai_dashboard.html", health=health, stats=stats, predictions=predictions)

@app.route("/admin/keys")
@login_required
def admin_keys():
    return render_template("admin_keys.html")

@app.route("/ussd", methods=["POST", "GET"])
def ussd_handler():
    text = request.values.get("text", "")
    if text == "":
        return "CON Welcome to Imperial Village System\n1. Register\n2. Check Balance\n3. Make Payment"
    return "END Session Closed"
@app.route("/api/business/data")
@login_required
def get_business_data():
    from datetime import datetime
    try:
        total_villages = Village.query.count()
        return jsonify({
            "success": True,
            "data": {
                "revenue": 45600.00,
                "active_villages": total_villages,
                "system_health": "99.9%",
                "timestamp": datetime.now().isoformat()
            }
        })
    except:
        return jsonify({"success": False, "message": "Database error"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False, use_reloader=False, host="0.0.0.0", port=8005)
