-- Run this once in the Supabase SQL editor (only needed if you use Supabase).

-- 1. Private storage bucket for creatives. The app uploads with one-time signed
--    URLs and reads with the service role key, so the bucket can stay private.
insert into storage.buckets (id, name, public, file_size_limit)
values ('creatives', 'creatives', false, 4294967296)
on conflict (id) do nothing;

-- 2. Launch history.
create table if not exists public.launches (
  id uuid primary key,
  created_at timestamptz not null default now(),
  record jsonb not null
);

-- Only the server (service role) touches this table; block the public keys.
alter table public.launches enable row level security;
