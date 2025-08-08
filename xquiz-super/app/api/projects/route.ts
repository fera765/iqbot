import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/src/lib/prisma';
import { FunnelSchema } from '@/src/lib/validate';

export async function GET() {
  const projects = await prisma.project.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(projects);
}

export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = FunnelSchema.safeParse(body);
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.flatten() }, { status: 400 });
  }
  const funnel = parsed.data;
  const project = await prisma.$transaction(async (tx) => {
    const created = await tx.project.create({
      data: { name: funnel.name, description: funnel.description ?? null },
    });
    await tx.node.createMany({
      data: funnel.nodes.map((n) => ({
        id: n.id,
        projectId: created.id,
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
        projectId: created.id,
        source: e.source,
        target: e.target,
        label: e.label ?? null,
        data: (e.data as any) ?? null,
      })),
    });
    return created;
  });
  return NextResponse.json(project);
}