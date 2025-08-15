import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { getProfile } from '../lib/api';

interface Profile {
  query: string;
  type: string;
  canonical_name?: string;
  description?: string;
  confidence: number;
  signals: {
    emails?: string[];
    domains?: string[];
    usernames?: string[];
    phones?: string[];
    locations?: string[];
  };
  sources: any[];
}

export default function ProfilePage() {
  const router = useRouter();
  const { q = '', type = 'unknown' } = router.query;
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    if (typeof q === 'string' && typeof type === 'string') {
      getProfile(q, type).then(setProfile);
    }
  }, [q, type]);

  if (!profile) {
    return <main className="p-4">Loading…</main>;
  }

  return (
    <main className="p-4 space-y-6" aria-labelledby="profile-heading">
      <header className="space-y-2">
        <h1 id="profile-heading" className="text-2xl font-bold">{profile.canonical_name || profile.query}</h1>
        <p className="text-sm text-gray-600">{profile.description}</p>
        <span className="inline-block bg-gray-200 px-2 py-1 rounded text-xs">{profile.type}</span>
        <span className="inline-block bg-blue-200 px-2 py-1 rounded text-xs">Confidence: {profile.confidence.toFixed(2)}</span>
      </header>

      <section aria-labelledby="signals-heading">
        <h2 id="signals-heading" className="font-semibold">Signals</h2>
        <ul className="grid grid-cols-2 gap-2" aria-label="signal list">
          {Object.entries(profile.signals || {}).map(([k, v]) => (
            <li key={k} className="border p-2" aria-label={k}>
              <strong>{k}</strong>
              <div className="text-sm">{Array.isArray(v) ? v.join(', ') : ''}</div>
            </li>
          ))}
        </ul>
      </section>

      <section aria-labelledby="timeline-heading">
        <h2 id="timeline-heading" className="font-semibold">Timeline</h2>
        <p className="text-sm">Timeline visualisation placeholder</p>
      </section>

      <section aria-labelledby="relationships-heading">
        <h2 id="relationships-heading" className="font-semibold">Relationships</h2>
        <p className="text-sm">Mini-graph placeholder</p>
      </section>

      <section aria-labelledby="sources-heading">
        <h2 id="sources-heading" className="font-semibold">Sources</h2>
        <ul className="space-y-1" aria-label="sources list">
          {profile.sources.map((s, i) => (
            <li key={i} className="text-sm">
              <a href={s.url} className="text-blue-700 underline" target="_blank" rel="noopener noreferrer">{s.url}</a>
              <span className="ml-2 text-gray-500">{s.fetched_at}</span>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
