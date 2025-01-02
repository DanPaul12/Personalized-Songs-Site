import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import { useEffect, useState } from 'react';
import SongSubmissionForm from './components/SubmissionForm';
import SubmissionsList from './components/SubmissionsList';
import HomePage from './components/HomePage';


function App() {
    

    return <div>
        <Router>
            <Routes>
                <Route path="/" element={<SongSubmissionForm />} />
                <Route path="/home" element={<HomePage />} />
                <Route path="/submissions" element={<SubmissionsList />} />
            </Routes>
        </Router>
    </div>;
}

export default App;
