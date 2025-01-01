import axios from 'axios';
import { useEffect, useState } from 'react';

function App() {
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/hello')
            .then(response => setMessage(response.data.message))
            .catch(error => console.error(error));
    }, []);

    return <div>{message}</div>;
}

export default App;
