from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import traceback
import json

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:thegoblet2@localhost/personalized_songs'
db = SQLAlchemy(app)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # Optional user_id field
    song_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=True)

@app.route('/api/song-submissions', methods=['POST'])
def submit_song():
    data = request.json
    try:
        # Parse data from the request
        #name = data['name']
        #email = data['email']
        song_details = json.dumps({
            "occasion": data['occasion'],
            "preferences": data['preferences'],
            "lyrics_idea": data['lyricsIdea']
        })

        new_order = Orders(song_details=song_details)
        db.session.add(new_order)
        db.session.commit()

        return jsonify({'message': 'Song submission received!'}), 201
    except Exception as e:
        print("Error occurred:", e)
        print(traceback.format_exc())  # Logs full traceback
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/song-submissions', methods=['GET'])
def get_submissions():
    try:
        submissions = Orders.query.all()
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