import "server-only";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { createClient, SupabaseClient } from "@supabase/supabase-js";
import { env, supabaseEnabled } from "./env";

/**
 * Media storage. Uses Supabase Storage when it is configured, otherwise a
 * local folder (DATA_DIR/uploads), which is fine when running on your own
 * computer.
 */

export const STORAGE_KEY_RE = /^[0-9a-f-]{36}\.(jpg|jpeg|png|mp4|mov)$/;

export const ALLOWED: Record<string, { ext: string; kind: "image" | "video" }> = {
  "image/jpeg": { ext: "jpg", kind: "image" },
  "image/png": { ext: "png", kind: "image" },
  "video/mp4": { ext: "mp4", kind: "video" },
  "video/quicktime": { ext: "mov", kind: "video" },
};

export const MIME_BY_EXT: Record<string, string> = {
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  png: "image/png",
  mp4: "video/mp4",
  mov: "video/quicktime",
};

export function assertKey(key: string): string {
  if (!STORAGE_KEY_RE.test(key)) throw new Error("Invalid media key");
  return key;
}

export function mimeForKey(key: string): string {
  return MIME_BY_EXT[key.split(".").pop() as string] ?? "application/octet-stream";
}

let supa: SupabaseClient | null = null;
function admin(): SupabaseClient {
  if (!supa) {
    supa = createClient(env.supabaseUrl, env.supabaseServiceKey, {
      auth: { persistSession: false, autoRefreshToken: false },
    });
  }
  return supa;
}

const uploadsDir = () => path.join(env.dataDir, "uploads");

export const storage = {
  kind: (): "supabase" | "local" => (supabaseEnabled() ? "supabase" : "local"),

  localPath(key: string): string {
    return path.join(uploadsDir(), assertKey(key));
  },

  async saveLocalStream(key: string, body: ReadableStream<Uint8Array>): Promise<number> {
    await fsp.mkdir(uploadsDir(), { recursive: true });
    const file = this.localPath(key);
    const out = fs.createWriteStream(file);
    let size = 0;
    const reader = body.getReader();
    try {
      for (;;) {
        const { done, value } = await reader.read();
        if (done) break;
        size += value.byteLength;
        if (!out.write(value)) await new Promise<void>((r) => out.once("drain", () => r()));
      }
    } catch (err) {
      out.destroy();
      await fsp.rm(file, { force: true });
      throw err;
    }
    await new Promise<void>((resolve, reject) => out.end((e?: Error | null) => (e ? reject(e) : resolve())));
    return size;
  },

  async createSignedUpload(key: string) {
    const { data, error } = await admin().storage.from(env.supabaseBucket).createSignedUploadUrl(assertKey(key));
    if (error || !data) throw new Error(`Supabase: ${error?.message ?? "could not sign upload"}`);
    return { path: data.path, token: data.token };
  },

  async readBytes(key: string): Promise<Uint8Array> {
    if (this.kind() === "local") return new Uint8Array(await fsp.readFile(this.localPath(key)));
    const { data, error } = await admin().storage.from(env.supabaseBucket).download(assertKey(key));
    if (error || !data) throw new Error(`Supabase download failed: ${error?.message ?? "no data"}`);
    return new Uint8Array(await data.arrayBuffer());
  },

  /** A URL Meta's servers can fetch, or null when files only exist locally. */
  async remoteUrl(key: string, seconds = 3600): Promise<string | null> {
    if (this.kind() === "local") return null;
    const { data, error } = await admin().storage.from(env.supabaseBucket).createSignedUrl(assertKey(key), seconds);
    if (error || !data) throw new Error(`Supabase: ${error?.message ?? "could not sign URL"}`);
    return data.signedUrl;
  },

  async remove(key: string): Promise<void> {
    if (this.kind() === "local") {
      await fsp.rm(this.localPath(key), { force: true });
      return;
    }
    await admin().storage.from(env.supabaseBucket).remove([assertKey(key)]);
  },
};

/** Supabase client for the history table (null when not configured). */
export function supabaseAdmin(): SupabaseClient | null {
  return supabaseEnabled() ? admin() : null;
}
