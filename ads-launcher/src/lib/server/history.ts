import "server-only";
import fsp from "node:fs/promises";
import path from "node:path";
import { env } from "./env";
import { supabaseAdmin } from "./storage";
import type { LaunchRecord } from "../launch/executor";

/**
 * Launch history. Saved to the Supabase table `launches` when Supabase is
 * configured (see supabase/schema.sql), and always mirrored to a local JSON
 * file so nothing is lost if the table is missing.
 */

const file = () => path.join(env.dataDir, "history.json");
const MAX = 300;

async function readLocal(): Promise<LaunchRecord[]> {
  try {
    return JSON.parse(await fsp.readFile(file(), "utf8")) as LaunchRecord[];
  } catch {
    return [];
  }
}

export async function saveLaunch(record: LaunchRecord): Promise<string | null> {
  let warning: string | null = null;
  const sb = supabaseAdmin();
  if (sb) {
    const { error } = await sb.from("launches").insert({ id: record.id, created_at: record.createdAt, record });
    if (error) warning = `Could not save to Supabase table "launches" (${error.message}). Saved locally instead.`;
  }
  try {
    await fsp.mkdir(env.dataDir, { recursive: true });
    const all = await readLocal();
    all.unshift(record);
    await fsp.writeFile(file(), JSON.stringify(all.slice(0, MAX), null, 2));
  } catch (err) {
    if (!sb) warning = `Could not save history: ${(err as Error).message}`;
  }
  return warning;
}

export async function listLaunches(): Promise<LaunchRecord[]> {
  const sb = supabaseAdmin();
  if (sb) {
    const { data, error } = await sb
      .from("launches")
      .select("record")
      .order("created_at", { ascending: false })
      .limit(MAX);
    if (!error && data) return data.map((r) => r.record as LaunchRecord);
  }
  return readLocal();
}
