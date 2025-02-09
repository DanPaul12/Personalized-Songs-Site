import React from 'react';
import { useNavigate } from 'react-router-dom';
import basic from '/src/images/basic.jpg'
import premium from '/src/images/premium.jpg'
import deluxe from '/src/images/deluxe.jpg'
import './SongLevels.css';


function SongLevels() {
    const navigate = useNavigate();

    const songLevels = [
        {
            level: 'basic',
            title: 'Basic',
            image: basic, // Replace with your image paths
            description: 'A simple yet heartfelt custom song.',
        },
        {
            level: 'premium',
            title: 'Premium',
            image: premium, // Replace with your image paths
            description: 'Enhanced production and creative lyrics.',
        },
        {
            level: 'deluxe',
            title: 'Deluxe',
            image: deluxe, // Replace with your image paths
            description: 'Top-notch production and a personal touch.',
        },
    ];

    const handleCardClick = (level) => {
        navigate(`/personalized-song-order-form?level=${level}`);
    };

    return (
        <div className="song-levels">
            <h1>Select Your Song Level</h1>
            <div className="levels-container">
                {songLevels.map((level) => (
                    <div
                        key={level.level}
                        className="level-card"
                        onClick={() => handleCardClick(level.level)}
                    >
                        <img src={level.image} alt={level.title} className="level-image" loading="lazy"/>
                        <h2>{level.title}</h2>
                        <p>{level.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default SongLevels;