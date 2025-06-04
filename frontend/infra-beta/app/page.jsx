'use client'
import Image from "next/image";
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) {
      setUser(stored);
    }
  }, []);

  const goToDashboard = () => {
    if (user) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  };

  return (
    <div className="p-4">
      <main className="space-y-4">
        <p>Hello world</p>
        <button
          onClick={goToDashboard}
          className="p-2 bg-green-500 text-white rounded"
        >
          {user ? 'Go to Dashboard' : 'Login'}
        </button>
      </main>
    </div>
  );
}
