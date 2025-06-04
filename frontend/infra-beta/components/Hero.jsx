import { FaRocket } from 'react-icons/fa';

export default function Hero() {
  return (
    <section className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-br from-gray-900 via-purple-900 to-black text-center text-white p-8">
      <FaRocket className="text-6xl mb-6 animate-bounce" />
      <h1 className="text-5xl font-extrabold mb-4">Welcome to Infra-Beta</h1>
      <p className="max-w-xl text-lg text-gray-300">
        Explore the future of infrastructure management with cutting edge tools and seamless integrations.
      </p>
    </section>
  );
}
