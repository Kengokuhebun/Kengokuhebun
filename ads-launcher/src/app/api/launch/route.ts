import { NextRequest, NextResponse } from "next/server";
import { executePlan, LaunchEvent, RecordingGraph } from "@/lib/launch/executor";
import { buildPlan, validateLaunch } from "@/lib/launch/plan";
import { launchRequestSchema } from "@/lib/launch/schema";
import { saveLaunch } from "@/lib/server/history";
import { errorResponse, getGraph } from "@/lib/server/meta";
import { storage } from "@/lib/server/storage";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";
// Video processing can take minutes. (Applies when hosted on Vercel.)
export const maxDuration = 800;

/**
 * Validates, builds the plan and runs it. Streams progress as
 * newline-delimited JSON (one LaunchEvent per line).
 */
export async function POST(req: NextRequest) {
  const parsed = launchRequestSchema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json(
      { error: "Invalid launch request", issues: parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`) },
      { status: 400 },
    );
  }
  const { config, assets, dryRun } = parsed.data;
  const v = validateLaunch(config, assets);
  if (v.errors.length) return NextResponse.json({ error: v.errors.join(" "), issues: v.errors }, { status: 400 });

  let graph;
  try {
    graph = dryRun ? new RecordingGraph() : getGraph();
  } catch (err) {
    return errorResponse(err);
  }
  const plan = buildPlan(config, assets);

  const encoder = new TextEncoder();
  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const send = (e: LaunchEvent | { type: "error"; error: string } | { type: "notice"; message: string }) => {
        try {
          controller.enqueue(encoder.encode(JSON.stringify(e) + "\n"));
        } catch {
          // Client went away; keep going so the launch finishes and is saved.
        }
      };
      try {
        const record = await executePlan({
          graph,
          accountId: config.accountId,
          plan,
          dryRun,
          media: dryRun
            ? { readBytes: async () => new Uint8Array(0), remoteUrl: async () => (storage.kind() === "local" ? null : "signed") }
            : { readBytes: (k) => storage.readBytes(k), remoteUrl: (k) => storage.remoteUrl(k) },
          emit: (e) => {
            if (e.type === "done" && dryRun && graph instanceof RecordingGraph) e.record.calls = graph.calls;
            send(e);
          },
        });
        if (!dryRun) {
          const warning = await saveLaunch(record);
          if (warning) send({ type: "notice", message: warning });
        }
      } catch (err) {
        send({ type: "error", error: err instanceof Error ? err.message : String(err) });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: { "content-type": "application/x-ndjson; charset=utf-8", "cache-control": "no-store" },
  });
}
