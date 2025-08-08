import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/src/lib/prisma';

export async function POST(req: NextRequest) {
  const body = await req.json();
  const { projectId, email, name, answers, outcome } = body ?? {};
  if (!projectId || !email) return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  const lead = await prisma.lead.create({
    data: { projectId, email, name: name ?? null, answers: answers ?? {}, outcome: outcome ?? null },
  });
  return NextResponse.json(lead);
}