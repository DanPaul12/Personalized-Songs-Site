import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import { useEffect, useState } from 'react';
import SongSubmissionForm from './components/SubmissionForm';
import SubmissionsList from './components/SubmissionsList';
import HomePage from './components/HomePage';
import SongLevels from './components/SongLevels';
import PaymentPage from './components/PaymentPage';



function App() {
    

    return <div>
        <Router>
            <Routes>
                <Route path="/" element={<SongSubmissionForm />} />
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
