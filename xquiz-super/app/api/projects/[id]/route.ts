import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/src/lib/prisma';
import { FunnelSchema } from '@/src/lib/validate';

export async function GET(_: NextRequest, { params }: { params: { id: string } }) {
  const project = await prisma.project.findUnique({
    where: { id: params.id },
    include: { nodes: true, edges: true, published: true },
  });
  if (!project) return NextResponse.json({ error: 'Not found' }, { status: 404 });
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

export async function PUT(req: NextRequest, { params }: { params: { id: string } }) {
  const body = await req.json();
  const parsed = FunnelSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const funnel = parsed.data;
  try {
    const updated = await prisma.$transaction(async (tx) => {
      await tx.project.update({ where: { id: params.id }, data: { name: funnel.name, description: funnel.description ?? null } });
      await tx.node.deleteMany({ where: { projectId: params.id } });
      await tx.edge.deleteMany({ where: { projectId: params.id } });
      await tx.node.createMany({
        data: funnel.nodes.map((n) => ({
          id: n.id,
          projectId: params.id,
          type: n.type,
          label: n.label,
          data: n.data as any,
          positionX: n.position.x,
          positionY: n.position.y,
        })),
      });
      await tx.edge.createMany({
        data: funnel.edges.map((e) => ({
          id: e.id,
          projectId: params.id,
          source: e.source,
          target: e.target,
          label: e.label ?? null,
          data: (e.data as any) ?? null,
        })),
      });
      return true;
    });
    return NextResponse.json({ ok: updated });
  } catch (e) {
    return NextResponse.json({ error: 'Update failed' }, { status: 500 });
  }
}

export async function DELETE(_: NextRequest, { params }: { params: { id: string } }) {
  await prisma.project.delete({ where: { id: params.id } });
  return NextResponse.json({ ok: true });
}