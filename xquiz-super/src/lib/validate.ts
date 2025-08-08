import { z } from 'zod';

export const OptionSchema = z.object({
  id: z.string().min(1),
  label: z.string().min(1),
  value: z.number().optional(),
  next: z.string().optional(),
});

export const FormFieldSchema = z.object({
  id: z.string().min(1),
  label: z.string().min(1),
  type: z.enum(['text', 'email', 'tel', 'checkbox', 'select']),
  required: z.boolean().optional(),
  options: z.array(z.string()).optional(),
});

export const NodeDataSchema = z.object({
  description: z.string().optional(),
  question: z.string().optional(),
  options: z.array(OptionSchema).optional(),
  html: z.string().optional(),
  formFields: z.array(FormFieldSchema).optional(),
  scoring: z.record(z.string(), z.number()).optional(),
  result: z
    .object({
      title: z.string().min(1),
      body: z.string().optional(),
      ctaLabel: z.string().optional(),
      ctaUrl: z.string().url().optional(),
    })
    .optional(),
});

export const NodeSchema = z.object({
  id: z.string().min(1),
  type: z.enum(['start', 'question', 'result', 'form', 'logic', 'content']),
  label: z.string().min(1),
  position: z.object({ x: z.number(), y: z.number() }),
  data: NodeDataSchema,
});

export const EdgeSchema = z.object({
  id: z.string().min(1),
  source: z.string().min(1),
  target: z.string().min(1),
  label: z.string().optional(),
  data: z
    .object({ condition: z.string().optional(), value: z.union([z.string(), z.number(), z.boolean()]).optional() })
    .optional(),
});

export const FunnelSchema = z.object({
  version: z.literal(1),
  name: z.string().min(1),
  description: z.string().optional(),
  nodes: z.array(NodeSchema),
  edges: z.array(EdgeSchema),
});

export type FunnelInput = z.infer<typeof FunnelSchema>;