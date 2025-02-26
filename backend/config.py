import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

class Config:
    stripe_publishable_key = os.getenv("STRIPE_PUBLISHABLE_KEY")
    stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
    stripe_webhook_endpoint = os.getenv("WEBHOOK_SECRET")
    password = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

def init_app(app):
    app.config.from_object(Config)

def init_stripe():
    import stripe
    stripe.api_key = Config.stripe_secret_key