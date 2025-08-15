const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function search(query: string, type: string) {
  const url = `${API_BASE}/search?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('search failed');
    return await res.json();
  } catch {
    return { query, type, count: 0, docs: [] };
  }
}

export async function getProfile(query: string, type: string) {
  const url = `${API_BASE}/profile?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('profile failed');
    return await res.json();
  } catch {
    return null;
  }
}
