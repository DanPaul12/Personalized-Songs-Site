from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import stripe
import traceback
import json
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the keys
stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
stripe_webhook_endpoint = os.getenv("WEBHOOK_SECRET")
password = os.getenv("DB_PASSWORD")


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{password}@localhost/personalized_songs'
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == "True"
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEBUG'] = True

mail = Mail(app)
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

    

stripe.api_key = stripe_secret_key
WEBHOOK_SECRET = stripe_webhook_endpoint

#----------------------------------------------------------------

def handle_payment_success(payment_intent):
    payment = Payment.query.filter_by(payment_intent_id=payment_intent['id']).first()
    if payment:
        payment.status = "succeeded"
        db.session.commit()

        order = Order.query.filter_by(email=payment.email).order_by(Order.created_at.desc()).first()
        if order:
            send_confirmation_email(order.email, order.song_details)
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

def send_confirmation_email(to_email, song_details):
    try:
        msg = Message(
            subject="Your Custom Song Order Confirmation",
            sender=app.config['MAIL_USERNAME'],
            recipients=[to_email],
            body=f"Thank you for your order!\n\nYour song details:\n{song_details}"
        )
        mail.send(msg)
        print("Confirmation email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


#------------------------------------------------------------------------------------

@app.route('/test-email', methods=['GET'])
def test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_USERNAME'],
            recipients=["dan.paul.schechter@gmail.com"],
            body="This is a test email from the app."
        )
        mail.send(msg)
        return "Test email sent successfully!"
    except Exception as e:
        return f"Error sending test email: {e}", 500

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
    app.run(debug=True)