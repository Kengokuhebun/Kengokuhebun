import { NextResponse } from "next/server";
import { listLaunches } from "@/lib/server/history";

export const dynamic = "force-dynamic";

export async function GET() {
  try {
    return NextResponse.json({ launches: await listLaunches() });
  } catch (err) {
    return NextResponse.json({ error: (err as Error).message }, { status: 500 });
  }
}
