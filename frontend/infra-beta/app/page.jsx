import dynamic from 'next/dynamic';

const Hero = dynamic(() => import('../components/Hero'));
const Features = dynamic(() => import('../components/Features'));

export default function Home() {
  return (
    <div className="bg-black min-h-screen">
      <Hero />
      <Features />
    </div>
  );
}
