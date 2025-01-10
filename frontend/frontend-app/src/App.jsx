import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import { useEffect, useState } from 'react';
import SongSubmissionForm from './components/SubmissionForm';
import SubmissionsList from './components/SubmissionsList';
import HomePage from './components/HomePage';
import SongLevels from './components/SongLevels';
import PaymentPage from './components/PaymentPage';
import Navbar from './components/NavBar';
import BlogList from './components/blogfiles/BlogList';
import BlogDetails from './components/blogfiles/BlogDetails';
import BlogForm from './components/blogfiles/BlogForm';
import AOS from 'aos';
import { Helmet } from "react-helmet";
import 'aos/dist/aos.css';




function App() {
    useEffect(() => {
        AOS.init();
    }, []);
    

    return <div>
        <Helmet>
            <meta charSet="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Dan & Drum | Personalized Songs</title>
            <meta name="description" content="Dan & Drum crafts personalized songs tailored to your special moments. Explore custom music today." />
            <meta name="keywords" content="personalized songs, custom music, indie artists, gift ideas" />
        </Helmet>
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/personalized-songs" element={<HomePage />} />
                <Route path="/submissions" element={<SubmissionsList />} />
                <Route path="/personalized-song-order-form" element={<SongSubmissionForm />} />
                <Route path="/personalized-song-levels" element={<SongLevels />} />
                <Route path="/payment-page" element={<PaymentPage />} />
                <Route path="/personalized-songs-blogs" element={<BlogList />} />
                <Route path="/personalized-songs-blogs/:slug" element={<BlogDetails />} />
                <Route path="/admin/blogs/new" element={<BlogForm />} />
                <Route path="/admin/blogs/:id/edit" element={<BlogForm />} />
            </Routes>
        </Router>
    </div>;
}

export default App;
