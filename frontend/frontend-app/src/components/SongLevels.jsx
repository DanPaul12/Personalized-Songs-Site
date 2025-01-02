import React from 'react';
import { useNavigate } from 'react-router-dom';

function SongLevels() {
    const navigate = useNavigate();

    const handleSelection = (level) => {
        navigate(`/order-form?level=${level}`); // Navigate to form with level as a query parameter
    };

    return (
        <div className="song-levels">
            <h1>Select Your Song Level</h1>
            <div className="levels-container">
                <div className="level-card" onClick={() => handleSelection('basic')}>
                    <h2>Basic Song</h2>
                    <p>A simple and heartfelt melody perfect for any occasion.</p>
                </div>
                <div className="level-card" onClick={() => handleSelection('premium')}>
                    <h2>Premium Song</h2>
                    <p>A more elaborate composition with professional mixing and mastering.</p>
                </div>
                <div className="level-card" onClick={() => handleSelection('custom')}>
                    <h2>Custom Song</h2>
                    <p>Fully tailored, unique production with your input throughout.</p>
                </div>
            </div>
        </div>
    );
}

export default SongLevels;