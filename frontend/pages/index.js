import { useState, useEffect } from 'react';
import HistoryTable from '../components/HistoryTable';

export default function Home() {
    const [text, setText] = useState('');
    const [history, setHistory] = useState([]);

    const handleSubmit = async () => {
        try {
            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });
            const result = await response.json();
            if (response.ok) {
                setHistory([...history, result]);
                console.log(result);
            } else {
                console.error(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    useEffect(() => {
        const fetchHistory = async () => {
            const response = await fetch('/api/history');
            const data = await response.json();
            setHistory(data);
        };
        fetchHistory();
    }, []);

    return (
        <div>
            <h1>CRUD App</h1>
            <input 
                type="text" 
                value={text} 
                onChange={(e) => setText(e.target.value)} 
                placeholder="Enter text here"
            />
            <button onClick={handleSubmit}>Submit</button>
            <HistoryTable history={history} />
        </div>
    );
}
