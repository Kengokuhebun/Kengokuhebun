"use client";
import { createClient } from "@supabase/supabase-js";
import type { Ratio } from "../launch/schema";
import { stripExtension } from "../launch/naming";
import type { AppConfig } from "./api";

export const ACCEPT = ".mp4,.mov,.jpg,.jpeg,.png,video/mp4,video/quicktime,image/jpeg,image/png";

const BY_EXT: Record<string, { mime: string; kind: "image" | "video" }> = {
  jpg: { mime: "image/jpeg", kind: "image" },
  jpeg: { mime: "image/jpeg", kind: "image" },
  png: { mime: "image/png", kind: "image" },
  mp4: { mime: "video/mp4", kind: "video" },
  mov: { mime: "video/quicktime", kind: "video" },
};

export const MAX_IMAGE = 30 * 1024 * 1024;
export const MAX_VIDEO = 4 * 1024 * 1024 * 1024;

export function classifyFile(file: File): { mime: string; kind: "image" | "video" } | null {
  const ext = file.name.split(".").pop()?.toLowerCase() ?? "";
  const byExt = BY_EXT[ext];
  if (!byExt) return null;
  // Trust the extension; browsers sometimes report an empty or odd type.
  return byExt;
}

export function classifyRatio(w: number, h: number): Ratio {
  if (!w || !h) return "other";
  const r = w / h;
  const near = (target: number) => Math.abs(r - target) / target < 0.02;
  if (near(1)) return "1:1";
  if (near(4 / 5)) return "4:5";
  if (near(9 / 16)) return "9:16";
  return "other";
}

export async function probeDimensions(file: File, kind: "image" | "video"): Promise<{ width: number; height: number }> {
  const url = URL.createObjectURL(file);
  try {
    if (kind === "image") {
      return await new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve({ width: img.naturalWidth, height: img.naturalHeight });
        img.onerror = () => resolve({ width: 0, height: 0 });
        img.src = url;
      });
    }
    return await new Promise((resolve) => {
      const v = document.createElement("video");
      v.preload = "metadata";
      v.muted = true;
      const timer = setTimeout(() => resolve({ width: 0, height: 0 }), 15000);
      v.onloadedmetadata = () => {
        clearTimeout(timer);
        resolve({ width: v.videoWidth, height: v.videoHeight });
      };
      v.onerror = () => {
        clearTimeout(timer);
        resolve({ width: 0, height: 0 });
      };
      v.src = url;
    });
  } finally {
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
}

function uploadLocal(file: File, mime: string, onProgress: (p: number) => void): Promise<{ storageKey: string }> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/media/upload");
    xhr.setRequestHeader("content-type", mime);
    xhr.upload.onprogress = (e) => e.lengthComputable && onProgress(e.loaded / e.total);
    xhr.onload = () => {
      let body: { storageKey?: string; error?: string } = {};
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        // ignore
      }
      if (xhr.status >= 200 && xhr.status < 300 && body.storageKey) resolve({ storageKey: body.storageKey });
      else reject(new Error(body.error || `Upload failed (${xhr.status})`));
    };
    xhr.onerror = () => reject(new Error("Network error during upload"));
    xhr.send(file);
  });
}

async function uploadSupabase(file: File, mime: string, cfg: AppConfig, onProgress: (p: number) => void) {
  const res = await fetch("/api/media/sign", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ mime }),
  });
  const signed = (await res.json()) as { storageKey?: string; path?: string; token?: string; error?: string };
  if (!res.ok || !signed.storageKey || !signed.token || !signed.path) throw new Error(signed.error || "Could not start upload");
  const sb = createClient(cfg.supabaseUrl, cfg.supabaseAnonKey, { auth: { persistSession: false } });
  onProgress(0.05);
  const { error } = await sb.storage.from(cfg.bucket).uploadToSignedUrl(signed.path, signed.token, file, { contentType: mime });
  if (error) throw new Error(`Supabase upload failed: ${error.message}`);
  onProgress(1);
  return { storageKey: signed.storageKey };
}

export async function uploadFile(file: File, mime: string, cfg: AppConfig, onProgress: (p: number) => void) {
  return cfg.storage === "supabase" ? uploadSupabase(file, mime, cfg, onProgress) : uploadLocal(file, mime, onProgress);
}

export function displayName(fileName: string): string {
  return stripExtension(fileName).trim().slice(0, 200) || "Creative";
}

export function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 ** 2) return `${(n / 1024).toFixed(0)} KB`;
  if (n < 1024 ** 3) return `${(n / 1024 ** 2).toFixed(1)} MB`;
  return `${(n / 1024 ** 3).toFixed(2)} GB`;
}

export const mediaUrl = (key: string) => `/api/media/file?key=${encodeURIComponent(key)}`;
