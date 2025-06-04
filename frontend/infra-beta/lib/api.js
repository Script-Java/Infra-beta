const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export async function sendFileAndQuery({ file, query }) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('query', query);

  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || 'Request failed');
  }
  return res.json();
}
