from flask import Flask
import os
import requests

app = Flask(__name__)


def send_simple_message():
  	return requests.post(
  		"https://api.mailgun.net/v3/dananddrumpersonalizedsongs.com/messages",
  		auth=("api", os.getenv('MAILGUN_API_KEY')),
  		data={"from": "Dan & Drum <postmaster@dananddrumpersonalizedsongs.com>",
			"to": "Daniel Paul Schechter <dan.paul.schechter@gmail.com>",
  			"subject": "Hello Daniel Paul Schechter",
  			"text": "Congratulations Daniel Paul Schechter, you just sent an email with Mailgun! You are truly awesome!"})
        

response = send_simple_message()
print("Status Code:", response.status_code)
print("Response Text:", response.text)

if __name__ == "__main__":
    app.run(debug=True)