import { NextRequest, NextResponse } from "next/server";
import { ALLOWED, storage } from "@/lib/server/storage";

export const dynamic = "force-dynamic";

/** Supabase: returns a one-time signed upload token so the browser uploads directly. */
export async function POST(req: NextRequest) {
  if (storage.kind() !== "supabase") {
    return NextResponse.json({ error: "Supabase is not configured" }, { status: 400 });
  }
  const { mime } = (await req.json().catch(() => ({}))) as { mime?: string };
  const allowed = ALLOWED[(mime ?? "").toLowerCase()];
  if (!allowed) return NextResponse.json({ error: `File type ${mime || "unknown"} is not allowed` }, { status: 415 });
  const key = `${crypto.randomUUID()}.${allowed.ext}`;
  try {
    const signed = await storage.createSignedUpload(key);
    return NextResponse.json({ storageKey: key, ...signed });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 500 });
  }
}
