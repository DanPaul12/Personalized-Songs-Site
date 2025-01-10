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
import 'aos/dist/aos.css';




function App() {
    useEffect(() => {
        AOS.init();
    }, []);
    

    return <div>
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/submissions" element={<SubmissionsList />} />
                <Route path="/order-form" element={<SongSubmissionForm />} />
                <Route path="/song-levels" element={<SongLevels />} />
                <Route path="/payment-page" element={<PaymentPage />} />
                <Route path="/blogs" element={<BlogList />} />
                <Route path="/blogs/:slug" element={<BlogDetails />} />
                <Route path="/admin/blogs/new" element={<BlogForm />} />
                <Route path="/admin/blogs/:id/edit" element={<BlogForm />} />
            </Routes>
        </Router>
    </div>;
}

export default App;
