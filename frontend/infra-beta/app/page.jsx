import dynamic from 'next/dynamic';
import { useMemo } from 'react';

const LineChart = dynamic(() => import('../components/LineChart'), { ssr: false });

export default function Home() {
  const data = useMemo(
    () => ({
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
      datasets: [
        {
          label: 'Users',
          data: [12, 19, 3, 5, 2],
          borderColor: '#14b8a6',
          backgroundColor: 'rgba(20,184,166,0.2)',
          tension: 0.4,
        },
      ],
    }),
    []
  );

  const options = useMemo(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
    }),
    []
  );

  return (
    <div className="px-4">
      <section className="text-center py-20" id="home">
        <h2 className="text-4xl font-bold mb-4 text-teal-400">Welcome to Infra Beta</h2>
        <p className="max-w-xl mx-auto text-gray-400">
          Futuristic analytics dashboard powered by AI.
        </p>
      </section>
      <section id="graphs" className="grid place-items-center h-72">
        <LineChart data={data} options={options} />
      </section>
    </div>
  );
}
