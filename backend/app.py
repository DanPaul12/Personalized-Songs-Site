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
stripe_webhook_endpoint = os.getenv("WEBHOOK_SECRET")


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
    __tablename__ = 'payments' 
    id = db.Column(db.Integer, primary_key=True)
    payment_intent_id = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Integer, nullable=False)  # Amount in cents
    status = db.Column(db.String(50), nullable=False, default="pending")  # e.g., pending, succeeded, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

stripe.api_key = stripe_secret_key
WEBHOOK_SECRET = stripe_webhook_endpoint

def handle_payment_success(payment_intent):
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "succeeded"
        db.session.commit()

def handle_payment_failure(payment_intent):
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "failed"
        db.session.commit()

def handle_payment_canceled(payment_intent):
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "canceled"
        db.session.commit()

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        # Invalid payload
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return "Invalid signature", 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_payment_success(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_payment_failure(payment_intent)
    elif event['type'] == 'payment_intent.canceled':
        payment_intent = event['data']['object']
        handle_payment_canceled(payment_intent)

    return "Success", 200


@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data.get('amount', 0)
        email = data.get('email')
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={"enabled": True},
        )

        payment = Payment(
            payment_intent_id=intent['id'],
            email=email,
            amount=amount,
            status="pending"
        )
        db.session.add(payment)
        db.session.commit()

        return jsonify({'clientSecret': intent['client_secret']})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/update-payment-status', methods=['POST'])
def update_payment_status():
    data = request.get_json()
    payment_intent_id = data['paymentIntentId']
    status = data['status']

    try:
        # Find the payment record
        payment = Payment.query.filter_by(payment_intent_id=payment_intent_id).first()
        if payment:
            payment.status = status
            db.session.commit()
            return jsonify({"message": "Payment status updated successfully."})
        else:
            return jsonify({"error": "Payment not found."}), 404
    except Exception as e:
        return jsonify(error=str(e)), 400

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