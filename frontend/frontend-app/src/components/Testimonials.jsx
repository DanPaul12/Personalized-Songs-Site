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
            quote: "“This may very well be the best email I've ever received. I absolutely love the song and the lyrics and I know Ben will too” - Adeline Carter",
            image: 'src/images/chazandlouise.png',
        },
        {
            quote: "“I listened to this song for the first time about 2 hours ago, and have listened to it like 10 times since. I LOVE it so much.” - Johnny Nava",
            image: 'src/images/johnnynava.png',
        },
        {
            quote: "“Holy SHIT that is good, oh my god, thank you so much idek what to say, thank you so so much i love it i know she will too” - Dylan Brown",
            image: 'src/images/adeline.jpg',
        },
        // Add more testimonials as needed
    ];

    return (
        <section className="testimonial-section">
            
            <Swiper
                modules={[Pagination, Navigation]}
                pagination={false} // Disables the dots
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