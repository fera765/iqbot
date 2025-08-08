import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">XQuiz Super</h1>
        <p className="mt-6 text-lg leading-8 text-slate-600">
          Construa funis de vendas baseados em quizzes com edição visual, lógica avançada e publicação instantânea.
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link href="/editor" className="rounded-md bg-slate-900 px-6 py-3 text-white hover:bg-slate-800">
            Criar Funil
          </Link>
          <Link href="/explorar" className="text-slate-900 underline">
            Explorar exemplos
          </Link>
        </div>
      </div>
    </main>
  );
}