import React from 'react';

export default function HistoryTable({ history }) {
    return (
        <table className="history-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Original Text</th>
                    <th>Processed Text</th>
                </tr>
            </thead>
            <tbody>
                {history.map((item) => (
                    <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.original}</td>
                        <td>{item.processed}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
}
