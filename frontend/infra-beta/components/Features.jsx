import { FaTools, FaCloud, FaLock } from 'react-icons/fa';

const features = [
  {
    icon: FaTools,
    title: 'Automation',
    description: 'Streamline your workflows with powerful automation tools.'
  },
  {
    icon: FaCloud,
    title: 'Scalability',
    description: 'Scale seamlessly with cloud-native infrastructure.'
  },
  {
    icon: FaLock,
    title: 'Security',
    description: 'Protect your data with enterprise-grade security.'
  }
];

export default function Features() {
  return (
    <section className="py-20 bg-gray-950 text-white">
      <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-12 px-8">
        {features.map((feature) => {
          const Icon = feature.icon;
          return (
            <div key={feature.title} className="text-center">
              <Icon className="text-4xl mx-auto mb-4 text-purple-400" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
