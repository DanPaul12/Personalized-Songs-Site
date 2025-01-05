import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import { useEffect, useState } from 'react';
import SongSubmissionForm from './components/SubmissionForm';
import SubmissionsList from './components/SubmissionsList';
import HomePage from './components/HomePage';
import SongLevels from './components/SongLevels';
import PaymentPage from './components/PaymentPage';
import Navbar from './components/NavBar';
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
            </Routes>
        </Router>
    </div>;
}

export default App;
