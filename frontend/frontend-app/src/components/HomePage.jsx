import React from 'react';
import './HomePage.css'; 
import { useNavigate } from 'react-router-dom';
import Testimonials from './Testimonials';

const HomePage = () => {

    const navigate = useNavigate();

    const handleGetStarted = () => {
        navigate('/song-levels');
    };
    
    return (
        <div className="homepage">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content" data-aos="fade-up">
                    <h4>Dan & Drum's</h4>
                    <h1>Personalized Songs</h1>
                    <p>The Personal is Universal</p>
                    <button className="cta-button" onClick={handleGetStarted}>Get Started</button>
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
            <section className='testimonial-section'>
                <h2>The Reviews are in:</h2>
                <Testimonials/>
            </section>

            {/* Portfolio Section */}
            <section className="portfolio">
                <h2>Listen to the Music</h2>
                <div className="portfolio-grid">
                    <div className="spotify-player">
                        <iframe 
                            src="https://open.spotify.com/embed/track/173Q9olf7rOr0gQkGpK338?utm_source=generator" 
                            width="300" 
                            height="380" 
                            frameBorder="0" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                            loading="lazy">
                        </iframe>
                        <p>Our most-streamed track with over 5 million plays!</p>
                    </div>
                    <div className="spotify-player">
                        <iframe 
                            src="https://open.spotify.com/embed/track/6G1LvBcrEEB4RNimTqFmKm?utm_source=generator" 
                            width="300" 
                            height="380" 
                            frameBorder="0" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                            loading="lazy">
                        </iframe>
                        <p>A heartfelt ballad cherished for its universal message.</p>
                    </div>
                    <div className="spotify-player">
                        <iframe 
                            src="https://open.spotify.com/embed/track/3FfJkqLbBl5X2Hlg9YopgG?utm_source=generator" 
                            width="300" 
                            height="380" 
                            frameBorder="0" 
                            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
                            loading="lazy">
                        </iframe>
                        <p>Our newest release, showcasing fresh creativity.</p>
                    </div>
                </div>
                <button className="cta-button">Order Your Song</button>
            </section>

            {/* How It Works Section */}
            <section className="how-it-works">
                <h2>How It Works</h2>
                <div className="steps">
                    <div className="step" data-aos="fade-up">
                        <div className='text1'>
                                <h3>1. Tell Your Story</h3>
                                <p>Fill out a quick form with details about your song.</p>    
                        </div>
                        <div className='stepimg'>
                            <img src='src/images/firstsong1.png'></img>
                            <p className="caption">Share your unique experience with us.</p>
                        </div>
                    </div>
                    <div className="step" data-aos="fade-up">
                        <div className='stepimg'>
                            <img src='src/images/firstsongwedding.png'></img>
                            <p className="caption">Share your unique experience with us.</p>
                        </div>
                        <div className='text2'>
                            <h3>2. Collaborate</h3>
                            <p>I’ll create a one-of-a-kind song inspired by your input.</p>
                        </div>
                    </div>
                    <div className="step" data-aos="fade-up">
                        <div className='text3'>
                            <h3>3. Receive Your Song</h3>
                            <p>Get a professional-quality track delivered to you.</p>
                        </div>
                        <div className='stepimg'>
                            <img src='src/images/firstsong3.png'></img>
                            <p className="caption">Share your unique experience with us.</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Call-to-Action Section */}
            <section className="call-to-action">
                <h2>Ready to Create Something Truly Special?</h2>
                <button className="cta-button" onClick={handleGetStarted}>Order Your Song</button>
            </section>
        </div>
    );
};

export default HomePage;