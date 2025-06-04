'use client'
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) {
      router.replace('/login');
    } else {
      setUser(storedUser);
    }
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('user');
    router.push('/login');
  };

  if (!user) return null;

  return (
    <div className="p-4">
      <h1 className="text-2xl mb-4">Welcome, {user}!</h1>
      <button
        onClick={handleLogout}
        className="p-2 bg-red-500 text-white rounded"
      >
        Log Out
      </button>
    </div>
  );
}
