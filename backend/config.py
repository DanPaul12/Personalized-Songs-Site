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
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true" 
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def init_app(app):
    app.config.from_object(Config)

def init_stripe():
    import stripe
    stripe.api_key = Config.stripe_secret_key