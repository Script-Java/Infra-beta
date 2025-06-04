"use client";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/summary", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setSummary(data.ai_summary);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="file:mr-4"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          Submit
        </button>
      </form>

      {loading && (
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 border-2 border-t-transparent border-gray-900 rounded-full animate-spin" />
          <span>Processing...</span>
        </div>
      )}

      {summary && (
        <pre className="whitespace-pre-wrap bg-gray-100 p-4 rounded">
          {summary}
        </pre>
      )}
    </div>
  );
}
