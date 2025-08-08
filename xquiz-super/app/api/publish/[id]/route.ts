import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/src/lib/prisma';
import { randomUUID } from 'node:crypto';

export async function POST(_: NextRequest, { params }: { params: { id: string } }) {
  const project = await prisma.project.findUnique({ where: { id: params.id } });
  if (!project) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  const slug = randomUUID().slice(0, 8);
  const pub = await prisma.published.upsert({
    where: { projectId: project.id },
    create: { projectId: project.id, slug },
    update: { slug },
  });
  return NextResponse.json({ slug: pub.slug, url: `/p/${pub.slug}` });
}

export async function GET(_: NextRequest, { params }: { params: { id: string } }) {
  const pub = await prisma.published.findFirst({ where: { projectId: params.id } });
  if (!pub) return NextResponse.json({ error: 'Not published' }, { status: 404 });
  return NextResponse.json({ slug: pub.slug, url: `/p/${pub.slug}` });
}