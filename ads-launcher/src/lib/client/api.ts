"use client";
import { useCallback, useEffect, useState } from "react";

export interface AppConfig {
  metaConfigured: boolean;
  appSecretProof: boolean;
  apiVersion: string;
  storage: "supabase" | "local";
  supabaseUrl: string;
  supabaseAnonKey: string;
  bucket: string;
}

export interface MeResponse {
  user: { id: string; name?: string };
  accounts: { id: string; name: string; currency: string; timezone: string; business: string; status: string; active: boolean }[];
}

export interface AccountData {
  pages: { id: string; name: string; instagram: { id: string; username: string } | null }[];
  pixels: { id: string; name: string; last_fired_time?: string }[];
  audiences: { id: string; name: string; subtype: string; size: number | null }[];
  campaigns: { id: string; name: string; objective: string; status: string; hasCampaignBudget: boolean }[];
  warnings: string[];
}

const cache = new Map<string, unknown>();

export async function getJSON<T>(url: string): Promise<T> {
  const res = await fetch(url, { cache: "no-store" });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error((body as { error?: string }).error || `Request failed (${res.status})`);
  return body as T;
}

/** Tiny fetch hook with an in-memory cache and a reload function. */
export function useApi<T>(url: string | null) {
  const [data, setData] = useState<T | null>(url ? ((cache.get(url) as T) ?? null) : null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(
    async (force = false) => {
      if (!url) return;
      if (!force && cache.has(url)) {
        setData(cache.get(url) as T);
        return;
      }
      setLoading(true);
      setError(null);
      try {
        const d = await getJSON<T>(url);
        cache.set(url, d);
        setData(d);
      } catch (e) {
        setError((e as Error).message);
        setData(null);
      } finally {
        setLoading(false);
      }
    },
    [url],
  );

  useEffect(() => {
    if (url) void load();
    else setData(null);
  }, [url, load]);

  return { data, error, loading, reload: () => load(true) };
}
