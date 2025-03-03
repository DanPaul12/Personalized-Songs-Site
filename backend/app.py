from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import stripe
import traceback
import json
from dotenv import load_dotenv
import os
from config import init_app, init_stripe
from models import db, Order, Payment, Blog
import logging
import sys


app = Flask(__name__)
init_app(app)
init_stripe()
CORS(app, resources={r"/*": {"origins": "https://dananddrumpersonalizedsongs.com"}})
#CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

print("MAIL_SERVER:", app.config["MAIL_SERVER"])
print("MAIL_PORT:", app.config["MAIL_PORT"])
print("MAIL_USE_TLS:", app.config["MAIL_USE_TLS"])
print("MAIL_USERNAME:", app.config["MAIL_USERNAME"])
print("MAIL_PASSWORD:", "******" if app.config["MAIL_PASSWORD"] else "Not Set")
print("MAIL_DEFAULT_SENDER:", app.config["MAIL_DEFAULT_SENDER"])
print(os.getenv("MAIL_USERNAME"))

db.init_app(app)


@app.route("/test-log", methods=["GET"])
def test_log():
    print("Testing print log", flush=True)
    app.logger.debug("Testing app.logger log")
    return "Logged!"

@app.route('/init-db', methods=['GET'])
def init_db():
    try:
        db.create_all()
        return jsonify({"message": "Database initialized successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/check-tables')
def check_tables():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify({"tables": tables})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(f"frontend/frontend-app/build/{path}"):
        return send_from_directory('frontend/frontend-app/build', path)
    else:
        return send_from_directory('frontend/frontend-app/build', 'index.html')
    
#----------------------------------------------------------------

@app.route("/send_confirmation", methods=["POST"])
def send_confirmation():
    try:
        data = request.get_json()
        email = data.get("email")
        song_details = data.get("song_details")

        # Print debug logs
        print("Received request:", data)
        print("Extracted email:", email)
        print("Extracted song details:", song_details)

        if not email or not song_details:
            return jsonify({"error": "Missing email or song details"}), 400

        msg = Message(
            subject="Payment Confirmation",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=[email],
            body=f"Thank you for your payment! Your song details: {song_details}"
        )

        print("Attempting to send email...")
        mail.send(msg)
        print("✅ Email sent successfully!")

        return jsonify({"message": "Confirmation email sent successfully"}), 200
    except Exception as e:
        print(f"❌ Error while sending email: {e}")  # Log the error to the console
        return jsonify({"error": str(e)}), 500

#----------------------------------------------------------------

#WEBHOOK_SECRET = "whsec_48645bd88705d0e4e25d927a5ea01644ae4ed29bd0e88d143de295ad6f426733"
WEBHOOK_SECRET = "whsec_48645bd88705d0e4e25d927a5ea01644ae4ed29bd0e88d143de295ad6f426733"

def handle_payment_success(payment_intent):
    """Handles successful payments from Stripe webhooks."""
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "succeeded"
        db.session.commit()

        # Find the most recent order linked to the payment email
        order = Order.query.filter_by(email=payment.email).order_by(Order.created_at.desc()).first()
        if order:
            print(f"Confirmation email sent to {order.email} for order ID {order.id}.")
            # Send confirmation email (uncomment when email function is ready)
            # send_confirmation_email(order.email, order.song_details)


def handle_payment_failure(payment_intent):
    """Handles failed payments."""
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "failed"
        db.session.commit()


def handle_payment_canceled(payment_intent):
    """Handles canceled payments."""
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "canceled"
        db.session.commit()
'''
def handle_payment_success(payment_intent):
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "succeeded"
        db.session.commit()

        order = Order.query.filter_by(email=payment.email).order_by(Order.created_at.desc()).first()
        if order:
            #send_confirmation_email(order.email, order.song_details)
            print(f"Confirmation email sent to {order.email} for order ID {order.id}.")

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
'''
@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature')

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        app.logger.debug("⚠️ Invalid payload")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        app.logger.debug("⚠️ Invalid signature")
        return jsonify({'error': 'Invalid signature'}), 400

    print(f"🔹 Event received: {event['type']}")

    # Handle successful payments
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        app.logger.debug(f"💰 Payment succeeded for {payment_intent['amount']} cents")
        email = payment_intent["receipt_email"]
        song_details = "Your personalized song details here"
        send_email(email, song_details)

        # Find and update payment in database
        payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()

        if payment:
            payment.status = "succeeded"
            db.session.commit()
            app.logger.debug("✅ Payment updated in database")
        else:
            app.logger.debug("⚠️ No matching payment record found in database")

    return jsonify({'status': 'success'}), 200

def send_email(recipient_email, song_details):
    try:
        msg = Message(
            "Your Personalized Song Order Confirmation",
            recipients=[recipient_email]
        )
        msg.body = f"Thank you for your order! 🎶\n\nSong Details:\n{song_details}"
        mail.send(msg)
        app.logger.debug("✅ Confirmation email sent!")
    except Exception as e:
        app.logger.debug(f"❌ Error sending email: {e}")

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    
    email = data.get("email")
    amount = data.get("amount")  # Amount should be in cents

    if not email or not amount:
        return jsonify({"error": "Missing email or amount"}), 400

    try:
        # Create a PaymentIntent on Stripe
        intent = stripe.PaymentIntent.create(
            amount=amount,  # Amount in cents
            currency="usd",
            receipt_email=email,
        )

        # Store payment in database
        new_payment = Payment(
            payment_intent_id=intent.id,
            email=email,
            amount=amount,
            status="pending",  # Initially set to pending
            created_at=datetime.utcnow()
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify({
            "clientSecret": intent.client_secret,
            "paymentIntentId": intent.id,
            "message": "Payment initiated successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
'''
@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        data = request.json
        amount = data.get('amount', 0)
        email = data.get('email')
        song_details = data.get('song_details', 'No details provided')
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
'''
#------------------------------------------------------------------------------------

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

        return jsonify({'message': 'Song submission received!', "order_id": new_order.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/song-submissions/<int:order_id>', methods=['GET'])
def get_song_submission(order_id):
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({"error": "Order not found"}), 404

        return jsonify({
            "id": order.id,
            "song_details": order.song_details,
            "status": order.status,
            "created_at": order.created_at
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
    

#------------------------------------------------------------------------------------

@app.route('/api/blogs', methods=['POST'])
def create_blog():
    data = request.json
    try:
        blog = Blog(
            title=data['title'],
            slug=data['slug'],
            content=data['content'],
            category=data['category'],
            tags=data.get('tags', []),
            author=data.get('author', 'Admin'),
            published=data.get('published', False)
        )
        db.session.add(blog)
        db.session.commit()
        return jsonify({'message': 'Blog post created!', 'id': blog.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    try:
        blogs = Blog.query.all()
        result = [
            {
                "id": blog.id,
                "title": blog.title,
                "slug": blog.slug,
                "category": blog.category,
                "tags": blog.tags,
                "author": blog.author,
                "created_at": blog.created_at,
                "published": blog.published,
                "imageURL": blog.imageUrl
            } for blog in blogs
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/blogs/<slug>', methods=['GET'])
def get_blog_by_slug(slug):
    blog = Blog.query.filter_by(slug=slug).first()
    if not blog:
        return jsonify({"error": "Blog not found"}), 404
    
    # Directly construct the response as a dictionary
    response = {
        "id": blog.id,
        "title": blog.title,
        "slug": blog.slug,
        "content": blog.content,
        "category": blog.category,
        "tags": blog.tags,  # Assuming tags are stored as JSON
        "published": blog.published,
        "created_at": blog.created_at,
    }
    
    return jsonify(response)
    
@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.json
    try:
        blog = Blog.query.get(blog_id)
        if not blog:
            return jsonify({'error': 'Blog not found'}), 404
        
        blog.title = data.get('title', blog.title)
        blog.slug = data.get('slug', blog.slug)
        blog.content = data.get('content', blog.content)
        blog.category = data.get('category', blog.category)
        blog.tags = data.get('tags', blog.tags)
        blog.author = data.get('author', blog.author)
        blog.published = data.get('published', blog.published)
        
        db.session.commit()
        return jsonify({'message': 'Blog post updated!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    try:
        blog = Blog.query.get(blog_id)
        if not blog:
            return jsonify({'error': 'Blog not found'}), 404
        
        db.session.delete(blog)
        db.session.commit()
        return jsonify({'message': 'Blog post deleted!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # or logging.INFO for less verbosity
    app.run(debug=True)