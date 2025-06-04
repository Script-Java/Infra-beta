import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-gray-900 text-white p-4 flex justify-between items-center shadow-md">
      <h1 className="text-lg font-bold">Infra Beta</h1>
      <div className="space-x-4">
        <Link href="#graphs" className="hover:text-teal-400">Dashboard</Link>
        <Link href="#about" className="hover:text-teal-400">About</Link>
      </div>
    </nav>
  );
}
