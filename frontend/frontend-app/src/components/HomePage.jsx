import React from 'react';
import './HomePage.css'; // Create and style this CSS file

const HomePage = () => {
    return (
        <div className="homepage">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <h4>Dan & Drum's</h4>
                    <h1>Personalized Songs</h1>
                    <p>The Personal is Universal</p>
                    <button className="cta-button">Get Started</button>
                </div>
            </section>

            {/* About Section */}
            <section className="about">
                <h2>About Dan & Drum</h2>
                <p>
                Dan & Drum is a nationally touring act that has accrued 10s of millions of streams across platforms, with Florence Pugh and Rob Thomas as noted fans. Order a personalized song from Dan, and he will craft a customized song specific to your experience, while making it universally relatable- just like a "real" song. Many of these unique, catchy songs are released and go on to earn millions of streams.
                </p>
            </section>

            {/* Testimonials Section */}
            <section className="testimonials">
                <h2>What People Are Saying</h2>
                <div className="testimonial">
                    <blockquote>
                        “Dan’s song brought my wedding to life—now it has 1M streams on Spotify!”
                    </blockquote>
                </div>
                <div className="testimonial">
                    <blockquote>
                        “The most unique gift I’ve ever given. Truly unforgettable.”
                    </blockquote>
                </div>
            </section>

            {/* Portfolio Section */}
            <section className="portfolio">
                <h2>Listen to the Music</h2>
                <div className="song-snippet">
                    <audio controls>
                        <source src="/path-to-song-snippet.mp3" type="audio/mpeg" />
                        Your browser does not support the audio element.
                    </audio>
                    <p>This custom song now has 2M+ Spotify streams!</p>
                </div>
                {/* Add more snippets as needed */}
            </section>

            {/* How It Works Section */}
            <section className="how-it-works">
                <h2>How It Works</h2>
                <div className="steps">
                    <div className="step">
                        <h3>1. Tell Your Story</h3>
                        <p>Fill out a quick form with details about your song.</p>
                    </div>
                    <div className="step">
                        <h3>2. Collaborate</h3>
                        <p>I’ll create a one-of-a-kind song inspired by your input.</p>
                    </div>
                    <div className="step">
                        <h3>3. Receive Your Song</h3>
                        <p>Get a professional-quality track delivered to you.</p>
                    </div>
                </div>
            </section>

            {/* Call-to-Action Section */}
            <section className="call-to-action">
                <h2>Ready to Create Something Truly Special?</h2>
                <button className="cta-button">Order Your Song</button>
            </section>
        </div>
    );
};

export default HomePage;