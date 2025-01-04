from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import stripe
import traceback
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the keys
stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")

print(f"Publishable Key: {stripe_publishable_key}")
print(f"Secret Key: {stripe_secret_key}")

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:thegoblet2@localhost/personalized_songs'
db = SQLAlchemy(app)


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

    # Relationship with Payment table
    #payments = db.relationship('Payment', backref='order', lazy=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_payment_id = db.Column(db.String(100), nullable=False, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

stripe.api_key = stripe_secret_key

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data.get('amount', 0)
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={"enabled": True},
        )
        return jsonify({'clientSecret': intent['client_secret']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/record-payment', methods=['POST'])
def record_payment():
    data = request.json
    try:
        # Retrieve the associated order by order_id
        order_id = data['order_id']
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Create a new Payment record
        new_payment = Payment(
            stripe_payment_id=data['stripe_payment_id'],
            order_id=order_id,
            email=data['email'],
            amount=data['amount'],
            currency=data['currency'],
            status=data['status'],
            receipt_url=data.get('receipt_url')  # Optional field
        )
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({'message': 'Payment recorded successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@app.route('/payments/<int:order_id>', methods=['GET'])
def get_payments_for_order(order_id):
    try:
        # Query all payments associated with the given order_id
        payments = Payment.query.filter_by(order_id=order_id).all()
        payment_list = [{
            'id': payment.id,
            'stripe_payment_id': payment.stripe_payment_id,
            'email': payment.email,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'receipt_url': payment.receipt_url,
            'created_at': payment.created_at
        } for payment in payments]

        return jsonify(payment_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/song-submissions', methods=['POST'])
def submit_song():
    data = request.json
    try:
        # Parse data from the request
        name = data['name']
        email = data['email']
        date_needed_by=datetime.strptime(data['dateNeededBy'], '%Y-%m-%d').date()
        level = data['level']
        price = data['price']
        song_details = json.dumps({
            "occasion": data['occasion'],
            "preferences": data['preferences'],
            "lyrics_idea": data['lyricsIdea']
        })

        # Create a new order
        new_order = Order(
            name=name,
            email=email,
            song_details=song_details,
            level=level,
            price=price,
            date_needed_by=date_needed_by
        )
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Song submission received!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/song-submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = Order.query.all()
        result = [
            {
                "id": submission.id,
                "song_details": submission.song_details,
                "status": submission.status,
                "created_at": submission.created_at
            } for submission in submissions
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)