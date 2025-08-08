import { NextResponse } from 'next/server';
import { prisma } from '@/src/lib/prisma';

export async function GET(_: Request, { params }: { params: { slug: string } }) {
  const pub = await prisma.published.findUnique({ where: { slug: params.slug }, include: { project: true } });
  if (!pub?.project) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  const project = await prisma.project.findUnique({
    where: { id: pub.projectId },
    include: { nodes: true, edges: true },
  });
  if (!project) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  if (new URL(_.url).searchParams.get('meta')) {
    return NextResponse.json({ projectId: project.id });
  }
  const funnel = {
    version: 1 as const,
    name: project.name,
    description: project.description ?? undefined,
    nodes: project.nodes.map((n) => ({
      id: n.id,
      type: n.type,
      label: n.label,
      position: { x: n.positionX, y: n.positionY },
      data: n.data as any,
    })),
    edges: project.edges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label ?? undefined,
      data: (e.data as any) ?? undefined,
    })),
  };
  return NextResponse.json(funnel);
}