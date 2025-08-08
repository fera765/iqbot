"use client";
import { useEffect, useMemo, useState } from 'react';

type Funnel = {
  name: string;
  nodes: any[];
  edges: any[];
};

export default function RunClient({ funnel, projectId }: { funnel: Funnel; projectId: string }) {
  const nodes = funnel.nodes;
  const edges = funnel.edges;
  const [currentId, setCurrentId] = useState<string | null>(() => {
    const start = nodes.find((n) => n.type === 'start');
    return start?.id ?? nodes[0]?.id ?? null;
  });
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const current = useMemo(() => nodes.find((n) => n.id === currentId), [nodes, currentId]);

  useEffect(() => {
    if (!current) return;
  }, [current]);

  function gotoNext(optionId?: string) {
    if (!current) return;
    const outgoing = edges.filter((e) => e.source === current.id);
    let nextId: string | undefined;
    if (optionId) {
      const edge = outgoing.find((e) => e.data?.condition === 'option' && e.data?.value === optionId) ?? outgoing[0];
      nextId = edge?.target;
    } else {
      nextId = outgoing[0]?.target;
    }
    if (nextId) setCurrentId(nextId);
  }

  async function submitLead(email: string, name?: string) {
    await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ projectId, email, name, answers }),
    });
  }

  if (!current) return <div className="text-slate-500">Nada para exibir</div>;

  if (current.type === 'question') {
    return (
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">{current.data?.question ?? current.label}</h2>
        <div className="grid gap-2">
          {(current.data?.options ?? []).map((opt: any) => (
            <button
              key={opt.id}
              className="rounded border px-3 py-2 text-left hover:bg-slate-50"
              onClick={() => {
                setAnswers((a) => ({ ...a, [current.id]: opt.id }));
                gotoNext(opt.id);
              }}
            >
              {opt.label}
            </button>
          ))}
        </div>
      </div>
    );
  }

  if (current.type === 'content') {
    return (
      <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: current.data?.html ?? '' }} />
    );
  }

  if (current.type === 'form') {
    return (
      <FormStep
        fields={current.data?.formFields ?? []}
        onSubmit={async (payload) => {
          await submitLead(payload.email, payload.name);
          gotoNext();
        }}
      />
    );
  }

  if (current.type === 'result') {
    return (
      <div className="space-y-3">
        <h2 className="text-xl font-semibold">{current.data?.result?.title ?? current.label}</h2>
        {current.data?.result?.body && (
          <p className="text-slate-600">{current.data.result.body}</p>
        )}
        {current.data?.result?.ctaUrl && (
          <a className="inline-block rounded bg-slate-900 text-white px-4 py-2" href={current.data.result.ctaUrl}>
            {current.data.result.ctaLabel ?? 'Continuar'}
          </a>
        )}
      </div>
    );
  }

  return <div className="text-slate-500">Etapa não suportada: {current.type}</div>;
}

function FormStep({
  fields,
  onSubmit,
}: {
  fields: { id: string; label: string; type: string; required?: boolean; options?: string[] }[];
  onSubmit: (payload: any) => void | Promise<void>;
}) {
  const [form, setForm] = useState<Record<string, any>>({});
  return (
    <form
      className="space-y-3"
      onSubmit={async (e) => {
        e.preventDefault();
        await onSubmit(form);
      }}
    >
      {fields.map((f) => (
        <label key={f.id} className="block text-sm">
          <div className="mb-1 text-slate-600">{f.label}</div>
          <input
            type={f.type === 'email' ? 'email' : 'text'}
            required={f.required}
            className="w-full rounded border px-3 py-2"
            onChange={(e) => setForm((s) => ({ ...s, [f.id]: e.target.value }))}
          />
        </label>
      ))}
      <button className="rounded bg-slate-900 text-white px-4 py-2" type="submit">
        Enviar
      </button>
    </form>
  );
}