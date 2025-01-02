import React, { useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

function SongSubmissionForm() {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const selectedLevel = queryParams.get('level');

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        occasion: '',
        preferences: '',
        lyricsIdea: ''
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
        } catch (error) {
            console.error('Error submitting song:', error);
            alert('Failed to submit the song. Please try again.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
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
            <button type="submit">Submit Song</button>
        </form>
    );
}

export default SongSubmissionForm;