import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import './Testimonials.css';

import { Pagination, Navigation } from 'swiper/modules';

const Testimonials = () => {
    const testimonials = [
        {
            quote: "Dan’s song brought my wedding to life—now it has 1M streams on Spotify!",
            image: 'src/images/chazandlouise.png',
        },
        {
            quote: "The most unique gift I’ve ever given. Truly unforgettable.",
            image: 'src/images/johnnynava.png',
        },
        {
            quote: "The most unique gift I’ve ever given. Truly unforgettable.",
            image: 'src/images/adeline.jpg',
        },
        // Add more testimonials as needed
    ];

    return (
        <section className="testimonial-section">
            
            <Swiper
                modules={[Pagination, Navigation]}
                pagination={{ clickable: true }}
                navigation
                spaceBetween={30}
                slidesPerView={1}
                className="testimonial-slider"
            >
                {testimonials.map((testimonial, index) => (
                    <SwiperSlide key={index}>
                        <div className="testimonial-card">
                            <img
                                src={testimonial.image}
                                alt={`Testimonial ${index + 1}`}
                                className="testimonial-image"
                            />
                            <blockquote>{testimonial.quote}</blockquote>
                        </div>
                    </SwiperSlide>
                ))}
            </Swiper>
        </section>
    );
};

export default Testimonials;