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
    <div className="mt-10">
      <h1 className="text-3xl font-bold mb-6 text-center">Chat with your PDF</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="file"
            className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none bg-gray-50 p-2"
            onChange={(e) => setFile(e.target.files?.[0])}
          />
          <input
            type="text"
            className="w-full border border-gray-300 p-2 rounded focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ask a question"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Send
          </button>
        </form>
        {response && (
          <p className="mt-4 text-gray-700 whitespace-pre-line">{response}</p>
        )}
        {error && <p className="mt-4 text-red-500">{error}</p>}
      </div>
    </div>
  );
}
