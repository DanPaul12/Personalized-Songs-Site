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
            image: basic, 
            description: 'A custom song with acoustic guitar and vocals, 1 minute and 30 seconds long.',
        },
        {
            level: 'premium',
            title: 'Premium',
            image: premium, 
            description: 'A custom song with full instrumentation, 3 minutes or longer',
        },
        {
            level: 'deluxe',
            title: 'Deluxe',
            image: deluxe, 
            description: 'Fully produced and mastered, ready for professional release',
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