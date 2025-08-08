// @ts-nocheck
const { prisma } = require('../src/lib/prisma.cjs');

async function main() {
  const project = await prisma.project.create({ data: { name: 'Exemplo XQuiz Super', description: 'Funil de exemplo' } });
  await prisma.node.createMany({
    data: [
      { id: 'start-1', projectId: project.id, type: 'start', label: 'Início', data: {}, positionX: 100, positionY: 100 },
      { id: 'q-1', projectId: project.id, type: 'question', label: 'Pergunta 1', data: { question: 'Qual seu objetivo?', options: [ { id: 'a', label: 'Vender mais' }, { id: 'b', label: 'Gerar leads' } ] }, positionX: 300, positionY: 100 },
      { id: 'form-1', projectId: project.id, type: 'form', label: 'Contato', data: { formFields: [ { id: 'email', label: 'E-mail', type: 'email', required: true }, { id: 'name', label: 'Nome', type: 'text' } ] }, positionX: 600, positionY: 60 },
      { id: 'res-1', projectId: project.id, type: 'result', label: 'Resultado', data: { result: { title: 'Obrigado!', body: 'Em breve entraremos em contato.', ctaLabel: 'Visitar site', ctaUrl: 'https://example.com' } }, positionX: 600, positionY: 140 },
    ],
  });
  await prisma.edge.createMany({
    data: [
      { id: 'e1', projectId: project.id, source: 'start-1', target: 'q-1', label: 'começar' },
      { id: 'e2', projectId: project.id, source: 'q-1', target: 'form-1', label: 'A', data: { condition: 'option', value: 'a' } },
      { id: 'e3', projectId: project.id, source: 'q-1', target: 'res-1', label: 'B', data: { condition: 'option', value: 'b' } },
      { id: 'e4', projectId: project.id, source: 'form-1', target: 'res-1', label: 'Enviar' },
    ],
  });
  const pub = await prisma.published.create({ data: { projectId: project.id, slug: 'exemplo' } });
  console.log('Seeded projectId:', project.id, 'slug:', pub.slug);
}

main().finally(() => prisma.$disconnect());