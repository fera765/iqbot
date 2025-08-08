"use client";
import { useCallback, useMemo, useState } from 'react';
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useEdgesState,
  useNodesState,
  type Connection,
  type Edge,
  type Node,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { v4 as uuidv4 } from 'uuid';
import { FunnelSchema, type FunnelInput } from '@/src/lib/validate';

const START_NODE_ID = 'start';

export default function EditorPage() {
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState<string>('Meu Funil');

  const initialNodes: Node[] = useMemo(
    () => [
      {
        id: START_NODE_ID,
        type: 'input',
        position: { x: 100, y: 100 },
        data: { label: 'Início' },
      },
    ],
    []
  );
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  const onConnect = useCallback(
    (params: Connection) =>
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            id: uuidv4(),
          } as Edge,
          eds
        )
      ),
    [setEdges]
  );

  function addNode(kind: 'question' | 'form' | 'result' | 'content') {
    const id = uuidv4();
    const base: Node = {
      id,
      position: { x: 300 + Math.random() * 200, y: 100 + Math.random() * 200 },
      data: { label: kind.toUpperCase() },
      type: kind === 'result' ? 'output' : 'default',
    };
    setNodes((ns) => [...ns, base]);
  }

  function toFunnel(): FunnelInput {
    return {
      version: 1,
      name: name || 'Sem nome',
      description: '',
      nodes: nodes.map((n) => ({
        id: n.id,
        type:
          n.id === START_NODE_ID ? 'start' : n.type === 'output' ? 'result' : (n.data.kind as any) || 'question',
        label: (n.data?.label as string) || (n.id === START_NODE_ID ? 'Início' : 'Bloco'),
        position: { x: n.position.x, y: n.position.y },
        data:
          n.id === START_NODE_ID
            ? {}
            : (n.data?.payload as any) || { question: 'Pergunta?', options: [{ id: 'a', label: 'Opção A' }] },
      })),
      edges: edges.map((e) => ({
        id: (e.id as string) || uuidv4(),
        source: e.source!,
        target: e.target!,
      })),
    };
  }

  async function handleSaveAndPublish() {
    try {
      const funnel = toFunnel();
      const parsed = FunnelSchema.parse(funnel);
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(parsed),
      });
      if (!res.ok) throw new Error('Falha ao salvar projeto');
      const project = await res.json();
      const pub = await fetch(`/api/publish/${project.id}`, { method: 'POST' });
      if (!pub.ok) throw new Error('Falha ao publicar');
      const { url } = await pub.json();
      window.open(url, '_blank');
    } catch (e: any) {
      setError(e.message || 'Erro desconhecido');
    }
  }

  function handleImport(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    file.text().then((txt) => {
      try {
        const parsed = FunnelSchema.parse(JSON.parse(txt));
        setName(parsed.name);
        // Map nodes to RF
        const rfNodes: Node[] = parsed.nodes.map((n) => ({
          id: n.id,
          position: { x: n.position.x, y: n.position.y },
          data: { label: n.label, kind: n.type, payload: n.data },
          type: n.type === 'start' ? 'input' : n.type === 'result' ? 'output' : 'default',
        }));
        const rfEdges: Edge[] = parsed.edges.map((e) => ({ id: e.id, source: e.source, target: e.target }));
        setNodes(rfNodes);
        setEdges(rfEdges);
        setError(null);
      } catch (err: any) {
        setError('JSON inválido');
      }
    });
  }

  function handleExport() {
    try {
      const funnel = toFunnel();
      const blob = new Blob([JSON.stringify(funnel, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${funnel.name.replace(/\s+/g, '-')}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      setError('Falha ao exportar');
    }
  }

  return (
    <main className="h-dvh grid grid-rows-[auto,1fr]">
      <header className="border-b px-4 py-3 flex items-center gap-3">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="rounded border px-3 py-2 text-sm"
          placeholder="Nome do Funil"
        />
        <div className="ml-auto flex items-center gap-3">
          <label className="text-sm underline cursor-pointer">
            Importar JSON
            <input type="file" accept="application/json" className="hidden" onChange={handleImport} />
          </label>
          <button onClick={handleExport} className="rounded bg-slate-100 px-3 py-2 text-sm">Exportar</button>
          <button onClick={handleSaveAndPublish} className="rounded bg-slate-900 text-white px-3 py-2 text-sm">
            Salvar & Publicar
          </button>
        </div>
      </header>
      <section className="grid grid-cols-12">
        <aside className="col-span-3 border-r p-3 space-y-2">
          <div className="text-xs uppercase text-slate-500">Elementos</div>
          <div className="grid gap-2">
            <button className="rounded border px-3 py-2 text-left hover:bg-slate-50" onClick={() => addNode('question')}>Pergunta</button>
            <button className="rounded border px-3 py-2 text-left hover:bg-slate-50" onClick={() => addNode('form')}>Formulário</button>
            <button className="rounded border px-3 py-2 text-left hover:bg-slate-50" onClick={() => addNode('result')}>Resultado</button>
            <button className="rounded border px-3 py-2 text-left hover:bg-slate-50" onClick={() => addNode('content')}>Conteúdo</button>
          </div>
          {error && <div className="text-red-600 text-sm">{error}</div>}
        </aside>
        <div className="col-span-9">
          <div className="h-full">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
            >
              <Background gap={12} size={1} color="#e2e8f0" />
              <MiniMap pannable zoomable />
              <Controls />
            </ReactFlow>
          </div>
        </div>
      </section>
    </main>
  );
}