-- Synthetic-only, idempotent demo seed matching data/synthetic_bundle.json.
-- This file contains no real workspace data.

insert into public.knowledge_documents
  (id, workspace_id, resource_type, event_time, title, content, metadata, embedding)
values
  (
    'guide-deploy-001',
    'workspace-demo',
    'Guide',
    '2025-01-10T09:00:00Z'::timestamptz,
    'Primary deployment window',
    'Primary deployment window. Status: final. Value: 30 minutes.',
    '{"synthetic": true, "source": "bundled representative synthetic source JSON"}'::jsonb,
    array_fill(0::real, array[384])::vector
  ),
  (
    'guide-uptime-001',
    'workspace-demo',
    'Guide',
    '2025-02-12T10:30:00Z'::timestamptz,
    'Service uptime',
    'Service uptime. Status: final. Value: 99.9 %.',
    '{"synthetic": true, "source": "bundled representative synthetic source JSON"}'::jsonb,
    array_fill(0::real, array[384])::vector
  ),
  (
    'policy-access-001',
    'workspace-demo',
    'Policy',
    '2024-06-01T00:00:00Z'::timestamptz,
    'Repository access policy',
    'Repository access policy. Status: active.',
    '{"synthetic": true, "source": "bundled representative synthetic source JSON"}'::jsonb,
    array_fill(0::real, array[384])::vector
  ),
  (
    'note-review-001',
    'workspace-demo',
    'Note',
    '2025-02-12T10:00:00Z'::timestamptz,
    'Quarterly operations review',
    'Quarterly operations review. Status: finished.',
    '{"synthetic": true, "source": "bundled representative synthetic source JSON"}'::jsonb,
    array_fill(0::real, array[384])::vector
  )
on conflict (id) do update set
  workspace_id = excluded.workspace_id,
  resource_type = excluded.resource_type,
  event_time = excluded.event_time,
  title = excluded.title,
  content = excluded.content,
  metadata = excluded.metadata,
  embedding = excluded.embedding;

