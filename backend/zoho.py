from flask import Flask
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Load email config from environment variables
app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))  # Convert to int
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/test-email")
def send_test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config["MAIL_DEFAULT_SENDER"],
            recipients=["dan.paul.schechter@gmail.com"],
            body="This is a test email from your Flask app."
        )
        mail.send(msg)
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)