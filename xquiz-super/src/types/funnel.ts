export type NodeType = 'start' | 'question' | 'result' | 'form' | 'logic' | 'content';

export type FunnelNodeData = {
  description?: string;
  question?: string;
  options?: { id: string; label: string; value?: number; next?: string }[];
  html?: string;
  formFields?: { id: string; label: string; type: 'text' | 'email' | 'tel' | 'checkbox' | 'select'; required?: boolean; options?: string[] }[];
  scoring?: { [optionId: string]: number };
  result?: { title: string; body?: string; ctaLabel?: string; ctaUrl?: string };
};

export type FunnelNode = {
  id: string;
  type: NodeType;
  label: string;
  position: { x: number; y: number };
  data: FunnelNodeData;
};

export type FunnelEdge = {
  id: string;
  source: string;
  target: string;
  label?: string;
  data?: { condition?: string; value?: string | number | boolean };
};

export type Funnel = {
  version: 1;
  name: string;
  description?: string;
  nodes: FunnelNode[];
  edges: FunnelEdge[];
};