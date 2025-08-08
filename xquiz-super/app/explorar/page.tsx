import Link from 'next/link';

async function fetchProjects() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/projects`, { cache: 'no-store' });
  if (!res.ok) return [] as any[];
  return res.json();
}

export default async function ExplorePage() {
  const projects = await fetchProjects();
  return (
    <main className="mx-auto max-w-5xl px-6 py-10">
      <h1 className="text-2xl font-semibold mb-6">Projetos</h1>
      <ul className="space-y-3">
        {projects.map((p: any) => (
          <li key={p.id} className="border rounded p-4">
            <div className="font-medium">{p.name}</div>
            <div className="text-xs text-slate-500">{p.id}</div>
            <div className="mt-3 flex gap-3">
              <form action={`/api/publish/${p.id}`} method="post">
                <button className="text-sm underline" type="submit">Publicar</button>
              </form>
              <Link className="text-sm underline" href={`/api/projects/${p.id}`}>Exportar JSON</Link>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}