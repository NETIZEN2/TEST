import { useState } from 'react';
import Link from 'next/link';
import { search } from '../lib/api';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [type, setType] = useState('unknown');
  const [docs, setDocs] = useState<any[]>([]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const res = await search(query, type);
    setDocs(res.docs);
  }

  return (
    <main className="p-4 space-y-4" aria-labelledby="search-heading">
      <h1 id="search-heading" className="text-xl font-bold">Search</h1>
      <form onSubmit={onSubmit} className="flex flex-wrap gap-2" aria-label="search form">
        <input
          className="border p-2 flex-grow" value={query} onChange={e => setQuery(e.target.value)}
          aria-label="query" placeholder="Search query"/>
        <select
          className="border p-2" value={type} onChange={e => setType(e.target.value)} aria-label="type">
          <option value="person">Person</option>
          <option value="company">Company</option>
          <option value="group">Group</option>
          <option value="asset">Asset</option>
          <option value="unknown">Unknown</option>
        </select>
        <button type="submit" className="bg-blue-600 text-white px-3 py-2 rounded">Go</button>
      </form>
      <ul className="divide-y" aria-label="results">
        {docs.map(doc => (
          <li key={doc.id} className="py-2">
            <Link href={`/profile?id=${encodeURIComponent(doc.id)}&type=${encodeURIComponent(type)}&q=${encodeURIComponent(query)}`}>{doc.title || doc.url}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
