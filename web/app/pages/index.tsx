import Link from 'next/link';

export default function Home() {
  return (
    <main className="p-4" aria-labelledby="home-heading">
      <h1 id="home-heading" className="text-2xl font-bold">OSINT Pro</h1>
      <p className="mt-2">Analyst toolkit for lawful open source intelligence.</p>
      <Link href="/search" className="text-blue-700 underline">Start searching</Link>
    </main>
  );
}
