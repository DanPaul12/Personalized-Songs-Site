from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'  # Match the new table name in MySQL
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    song_details = db.Column(db.Text, nullable=False)
    date_needed_by = db.Column(db.Date, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=True)


class Payment(db.Model):
    __tablename__ = 'payments' 
    id = db.Column(db.Integer, primary_key=True)
    payment_intent_id = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # Amount in cents
    status = db.Column(db.String(50), nullable=False, default="pending")  # e.g., pending, succeeded, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.JSON, default=[])
    author = db.Column(db.String(255), nullable=False, default='Anonymous')  # New
    imageUrl = db.Column(db.String(2083))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    published = db.Column(db.Boolean, default=False)