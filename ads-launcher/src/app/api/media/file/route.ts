import fs from "node:fs";
import fsp from "node:fs/promises";
import { Readable } from "node:stream";
import { NextRequest, NextResponse } from "next/server";
import { mimeForKey, storage, STORAGE_KEY_RE } from "@/lib/server/storage";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function keyFrom(req: NextRequest): string | null {
  const key = req.nextUrl.searchParams.get("key") ?? "";
  return STORAGE_KEY_RE.test(key) ? key : null;
}

/** Serves a preview of an uploaded file (with Range support for video seeking). */
export async function GET(req: NextRequest) {
  const key = keyFrom(req);
  if (!key) return NextResponse.json({ error: "Invalid key" }, { status: 400 });

  if (storage.kind() === "supabase") {
    try {
      const url = await storage.remoteUrl(key, 6 * 3600);
      return NextResponse.redirect(url!, 302);
    } catch (err) {
      return NextResponse.json({ error: (err as Error).message }, { status: 404 });
    }
  }

  const file = storage.localPath(key);
  let size: number;
  try {
    size = (await fsp.stat(file)).size;
  } catch {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  const headers: Record<string, string> = {
    "content-type": mimeForKey(key),
    "accept-ranges": "bytes",
    "cache-control": "private, max-age=86400",
  };
  const range = req.headers.get("range");
  const m = range?.match(/bytes=(\d*)-(\d*)/);
  if (m && (m[1] || m[2])) {
    let start = m[1] ? Number(m[1]) : size - Number(m[2]);
    let end = m[1] && m[2] ? Number(m[2]) : size - 1;
    start = Math.max(0, start);
    end = Math.min(size - 1, end);
    if (start > end) return new NextResponse(null, { status: 416, headers: { "content-range": `bytes */${size}` } });
    const stream = Readable.toWeb(fs.createReadStream(file, { start, end })) as ReadableStream;
    return new NextResponse(stream, {
      status: 206,
      headers: { ...headers, "content-range": `bytes ${start}-${end}/${size}`, "content-length": String(end - start + 1) },
    });
  }
  const stream = Readable.toWeb(fs.createReadStream(file)) as ReadableStream;
  return new NextResponse(stream, { headers: { ...headers, "content-length": String(size) } });
}

export async function DELETE(req: NextRequest) {
  const key = keyFrom(req);
  if (!key) return NextResponse.json({ error: "Invalid key" }, { status: 400 });
  try {
    await storage.remove(key);
    return NextResponse.json({ ok: true });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 500 });
  }
}
