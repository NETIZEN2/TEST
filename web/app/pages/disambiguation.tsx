import Link from 'next/link';

const mock = [
  { id: '1', title: 'Example One' },
  { id: '2', title: 'Example Two' },
];

export default function DisambiguationPage() {
  return (
    <main className="p-4 space-y-4" aria-labelledby="disambiguation-heading">
      <h1 id="disambiguation-heading" className="text-xl font-bold">Disambiguation</h1>
      <p>Select the intended entity:</p>
      <ul className="list-disc pl-5">
        {mock.map(m => (
          <li key={m.id}>
            <Link href={`/profile?id=${m.id}`}>{m.title}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
