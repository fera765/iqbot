import { notFound } from 'next/navigation';
import Link from 'next/link';
import RunClient from './RunClient';

async function fetchFunnel(slug: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/published/${slug}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

async function fetchProjectId(slug: string) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL ?? ''}/api/published/${slug}?meta=1`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json();
}

export default async function RunPage({ params }: { params: { slug: string } }) {
  const funnel = await fetchFunnel(params.slug);
  if (!funnel) return notFound();
  const meta = await fetchProjectId(params.slug);
  const projectId = meta?.projectId ?? '';
  return (
    <main className="mx-auto max-w-3xl px-6 py-10 space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">{funnel.name}</h1>
        <p className="text-slate-600 mt-2">Execução básica do funil.</p>
      </div>
      <RunClient funnel={funnel} projectId={projectId} />
      <Link href="/" className="mt-6 inline-block underline">Voltar</Link>
    </main>
  );
}