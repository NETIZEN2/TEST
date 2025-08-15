export default function ComparePage() {
  return (
    <main className="p-4 space-y-4" aria-labelledby="compare-heading">
      <h1 id="compare-heading" className="text-xl font-bold">Compare Entities</h1>
      <div className="grid md:grid-cols-2 gap-4" aria-label="comparison grid">
        <div className="border p-2" aria-label="entity A">Entity A placeholder</div>
        <div className="border p-2" aria-label="entity B">Entity B placeholder</div>
      </div>
    </main>
  );
}
