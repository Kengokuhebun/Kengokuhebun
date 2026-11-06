import { NextRequest, NextResponse } from "next/server";
import { ALLOWED, storage } from "@/lib/server/storage";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

const MAX_BYTES = { image: 30 * 1024 * 1024, video: 4 * 1024 * 1024 * 1024 };

/**
 * Local-storage upload: the browser sends the raw file body, which is
 * streamed to disk (no size limit from buffering in memory).
 */
export async function POST(req: NextRequest) {
  if (storage.kind() !== "local") {
    return NextResponse.json({ error: "Uploads go straight to Supabase in this setup." }, { status: 400 });
  }
  const mime = (req.headers.get("content-type") ?? "").split(";")[0].trim().toLowerCase();
  const allowed = ALLOWED[mime];
  if (!allowed) return NextResponse.json({ error: `File type ${mime || "unknown"} is not allowed` }, { status: 415 });
  const declared = Number(req.headers.get("content-length") ?? 0);
  if (declared > MAX_BYTES[allowed.kind]) {
    return NextResponse.json({ error: "File is larger than Meta allows" }, { status: 413 });
  }
  if (!req.body) return NextResponse.json({ error: "Empty upload" }, { status: 400 });

  const key = `${crypto.randomUUID()}.${allowed.ext}`;
  try {
    const size = await storage.saveLocalStream(key, req.body);
    if (size > MAX_BYTES[allowed.kind]) {
      await storage.remove(key);
      return NextResponse.json({ error: "File is larger than Meta allows" }, { status: 413 });
    }
    return NextResponse.json({ storageKey: key, size });
  } catch (err) {
    return NextResponse.json({ error: `Upload failed: ${(err as Error).message}` }, { status: 500 });
  }
}
