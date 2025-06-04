'use client';

import { useState } from 'react';
import { sendFileAndQuery } from '../lib/api';

export default function Home() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setError(null);
    try {
      const data = await sendFileAndQuery({ file, query });
      setResponse(data.response);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="p-4">
      <form onSubmit={handleSubmit} className="space-y-2">
        <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />
        <input
          type="text"
          className="border p-1"
          placeholder="Ask a question"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="px-3 py-1 bg-blue-500 text-white">
          Send
        </button>
      </form>
      {response && <p className="mt-4">{response}</p>}
      {error && <p className="mt-4 text-red-500">{error}</p>}
    </div>
  );
}
