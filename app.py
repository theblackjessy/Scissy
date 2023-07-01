from datetime import datetime
# import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for, send_file, abort
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import qrcode
import os
from io import BytesIO
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import re
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import sqlite3
import psycopg2
from psycopg2 import sql
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from cutty import limiter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config

app = Flask(__name__)

limiter = Limiter(app, default_limits=["1/day"])
# limiter = Limiter(app)
base_dir = os.path.dirname(os.path.realpath(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(base_dir, 'cutty.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("DATABASE_URL")

app.secret_key = '2e1ef6c2cd1efb6c3147'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login configuration
login_manager = LoginManager(app)
login_manager.login_view = 'login'

DB_NAME = 'Linksnip'


# class UrlAnalytics(db.Model):
#     __tablename__ = 'urlanalytics'
#     id = db.Column(db.Integer, primary_key=True)
#     shortened_url = db.Column(db.String(255))
#     timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
#     ip_address = db.Column(db.String(255))
#     user_agent = db.Column(db.String(255))
#     referral_source = db.Column(db.String(255))

    # def __init__(self, shortened_url, ip_address, user_agent, referral_source):
    #     self.shortened_url = shortened_url
    #     self.ip_address = ip_address
    #     self.user_agent = user_agent
    #     self.referral_source = referral_source


class ShortUrls(db.Model):
    __tablename__ = 'shorturls'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_id = db.Column(db.String(16), nullable=False, unique=True)
    click_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    clicks = db.relationship('Click', backref='url', lazy=True)

    def __init__(self, original_url, short_id, click_count, created_at):
        self.original_url = original_url
        self.short_id = short_id
        self.click_count = click_count
        self.created_at = datetime.now()


class Click(db.Model):
    __tablename__ = 'clicks'
    id = db.Column(db.Integer, primary_key=True)
    shorturl_id = db.Column(db.Integer, db.ForeignKey('shorturls.id'), nullable=False)
    location = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    company_size = db.Column(db.String(50))
    primary_use_case = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    # password = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(150))
    created_at = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Log analytics data for a shortened URL
# def log_analytics(short_url, ip_address, user_agent, referral_source):
#     analytics = UrlAnalytics(shortened_url=short_url, ip_address=ip_address,
#                              user_agent=user_agent, referral_source=referral_source)
#     db.session.add(analytics)
#     db.session.commit()


# Retrieve analytics data for a shortened URL
# def get_analytics(short_url):
#     conn = psycopg2.connect(
#         host='localhost',
#         port=5432,
#         dbname='Linksnip.db'
#     )
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT ua.timestamp, ua.ip_address, ua.user_agent, ua.referral_source, c.location, c.created_at
#         FROM urlanalytics AS ua
#         INNER JOIN shorturls AS su ON ua.shortened_url = su.short_id
#         LEFT JOIN clicks AS c ON su.id = c.shorturl_id
#         WHERE ua.shortened_url = %s
#     ''', (short_url,))
#     data = cursor.fetchall()
#     conn.close()
#     return data


# Generate analytics report using Plotly
# def generate_analytics_report(data):
#     timestamps = [row[0] for row in data]
#     ip_addresses = [row[1] for row in data]
#     user_agents = [row[2] for row in data]
#     referral_sources = [row[3] for row in data]
#     click_locations = [row[4] for row in data]
#     click_timestamps = [row[5] for row in data]
#
#     fig = make_subplots(rows=2, cols=2, subplot_titles=("IP Addresses", "User Agents", "Referral Sources", "Clicks"))
#
#     fig.add_trace(go.Scatter(x=timestamps, y=ip_addresses, mode='lines', name='IP Addresses'), row=1, col=1)
#     fig.add_trace(go.Scatter(x=timestamps, y=user_agents, mode='lines', name='User Agents'), row=1, col=2)
#     fig.add_trace(go.Bar(x=timestamps, y=referral_sources, name='Referral Sources'), row=2, col=1)
#
#     # Plot click details
#     fig.add_trace(go.Scatter(x=click_timestamps, y=click_locations, mode='markers', name='Clicks'), row=2, col=2)
#
#     fig.update_layout(title='URL Analytics Report', xaxis_title='Timestamp', yaxis_title='Count')
#
#     return fig


# @app.route('/analytics', methods=['GET', 'POST'])
# def analytics():
#     if request.method == 'POST':
#         short_url = request.form.get('short_url')
#
#         # Retrieve analytics data for the shortened URL
#         data = get_analytics(short_url)
#
#         if data:
#             # Generate analytics report
#             fig = generate_analytics_report(data)
#             plot = fig.to_html(full_html=False)
#             return render_template('dashboard.html', plot=plot)
#         else:
#             return 'No analytics data available'
#
#     return render_template('dashboard.html', plot=None)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Custom filter for base64 encoding
@app.template_filter('b64encode')
def base64_encode(value):
    return base64.b64encode(value).decode('utf-8')


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(num_of_chars))

def validate_email(email):
        # Validate email format using regular expression
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_phone(phone):
        # Validate phone number format using regular expression
    pattern = r'^\d{11}$'
    return re.match(pattern, phone)


@app.route('/', methods=['GET', 'POST'])
def index():
    qr_image_data = b'My QR Code Data'
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Create a new contact instance
        new_contact = Contact(name=name, email=email, message=message)

        # Save the contact to the database
        db.session.add(new_contact)
        db.session.commit()

        # Redirect or render a success page
        return render_template('contact_success.html')

    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/shortenit')
def shortenit():
    return render_template('shortenit.html')


@app.route('/shortenedURL')
def shortenedURL():
    return render_template('shortenedURL.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # Redirect to the homepage or another route
        return redirect(url_for('index'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        company_name = request.form.get('company_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        job_title = request.form.get('job_title')
        company_size = request.form.get('company_size')
        primary_use_case = request.form.get('primary_use_case')
        country = request.form.get('country')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate email
        if not validate_email(email):
            flash(f'Invalid email address.')
            return redirect(url_for('register'))

        # Validate phone number
        if not validate_phone(phone):
            flash(f'Invalid phone number.')
            return redirect(url_for('register'))

        # Check if the user already exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f'Email address already registered.')
            return redirect(url_for('register'))

        # Check if the passwords match
        if password != confirm_password:
            flash(f'Passwords do not match.')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            company_name=company_name,
            email=email,
            phone=phone,
            job_title=job_title,
            company_size=company_size,
            primary_use_case=primary_use_case,
            country=country
        )
        new_user.set_password(password)

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash(f'Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect to the homepage or another route
        return redirect(url_for('shortenit'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user by email address
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Log in the user
            login_user(user)

            # Redirect to the homepage or another route
            return redirect(url_for('shortenit'))

        flash(f'Invalid email or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


# The URL shortening route and function...
@app.route('/shorten', methods=['GET', 'POST'])
@limiter.limit("1/day", key_func=get_remote_address)
@login_required
def shorten():
    qr_image_data = b''
    short_url = ''  # Initialize the variable with a default value
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first():
            flash(f'Please enter a different custom ID!')
            return redirect(url_for('shortenit'))

        if not url:
            flash(f'The URL is required!')
            return redirect(url_for('shortenit'))

        if not short_id:
            short_id = generate_short_id(8)

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=5, border=4)
        qr.add_data(url)
        qr.make(fit=True)

        qr_stream = BytesIO()
        qr.make_image(fill_color='black', back_color='white').save(qr_stream, 'PNG')
        qr_stream.seek(0)

        # Log analytics data for the shortened URL
        # log_analytics(short_url, request.remote_addr, request.user_agent.string, request.referrer)

        new_link = ShortUrls(
            original_url=url,
            short_id=short_id,
            # qr_image_data=qr_stream.getvalue(),
            click_count=0,
            created_at=datetime.now()
        )
        db.session.add(new_link)
        db.session.commit()

        short_url = request.host_url + short_id
        if qr_image_data is not None:
            return render_template('shortenedURL.html', short_url=short_url, qr_image_data=qr_stream.getvalue())
        else:
            flash(f'No image generated')
    return render_template('shortenedURL.html', qr_image_data=qr_image_data)


# The redirection route and function
@app.route('/<short_id>')
@login_required
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()

    if link:
        link.click_count += 1
        db.session.commit()
        return redirect(link.original_url)
    else:
        flash(f'Invalid URL')
        return redirect(url_for('shortenit'))


@app.route('/download_qr')
def download_qr():
    # Retrieve the QR code image stream from the query parameter
    qr_stream = request.args.get('qr_image_data')

    if qr_stream:
        # Return the QR code image as a downloadable file
        return send_file(BytesIO(qr_stream), attachment_filename='qr_code.png', as_attachment=True)
    else:
        abort(404, message='QR code image not found')


@app.route('/history')
def history():
    url_activities = ShortUrls.query.all()
    return render_template('history.html', url_activities=url_activities)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)