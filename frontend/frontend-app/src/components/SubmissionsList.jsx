import React, { useEffect, useState } from 'react';
import axios from 'axios';

function SubmissionsList() {
    const [submissions, setSubmissions] = useState([]);

    useEffect(() => {
        axios.get('https://api.dananddrumpersonalizedsongs.com/api/song-submissions')
            .then(response => setSubmissions(response.data))
            .catch(error => console.error('Error fetching submissions:', error));
    }, []);

    return (
        <div>
            <h1>Song Submissions</h1>
            <ul>
                {submissions.map(submission => (
                    <li key={submission.id}>
                        <h3>Submission ID: {submission.id}</h3>
                        <p>Details: {submission.song_details}</p>
                        <p>Status: {submission.status}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default SubmissionsList;