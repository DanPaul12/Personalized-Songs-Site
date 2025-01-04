import React, { useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

function SongSubmissionForm() {
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const selectedLevel = queryParams.get('level');

    const priceMapping = {
        basic: 250,
        premium: 500,
        deluxe: 650,
    };

    const selectedPrice = priceMapping[selectedLevel] || 0;

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        occasion: '',
        preferences: '',
        lyricsIdea: '',
        dateNeededBy: '',
        level: selectedLevel || 'basic',
        price: selectedPrice,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/api/song-submissions', formData);
            alert('Song submitted successfully: ' + response.data.message);

            // Redirect to the payment page with song details
            navigate(`/payment-page?email=${encodeURIComponent(formData.email)}&price=${formData.price}`);
        } catch (error) {
            console.error('Error submitting song:', error);
            alert('Failed to submit the song. Please try again.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h1>Order Form</h1>
            <p>Selected Level: {selectedLevel} (${selectedPrice})</p>
            <p>Please allow 2-3 weeks for delivery- more time often means more special!</p>
            <label>
                Name:
                <input type="text" name="name" value={formData.name} onChange={handleChange} required />
            </label>
            <br />
            <label>
                Email:
                <input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </label>
            <br />
            <label>
                Occasion:
                <input type="text" name="occasion" value={formData.occasion} onChange={handleChange} required />
            </label>
            <br />
            <label>
                Preferences:
                <input type="text" name="preferences" value={formData.preferences} onChange={handleChange} />
            </label>
            <br />
            <label>
                Lyrics Idea:
                <textarea name="lyricsIdea" value={formData.lyricsIdea} onChange={handleChange}></textarea>
            </label>
            <br />
            <label>
                Date Needed By:
                <input type="date" name="dateNeededBy" value={formData.dateNeededBy} onChange={handleChange} required />
            </label>
            <button type="submit">Submit Song</button>
        </form>
    );
}

export default SongSubmissionForm;