"use client";
import type { LaunchEvent, LaunchRecord, StepStatus } from "../launch/executor";
import type { Asset, LaunchConfig } from "../launch/schema";

export interface StepRow {
  id: string;
  label: string;
  status: StepStatus;
  detail?: string;
}

export type StreamEvent = LaunchEvent | { type: "error"; error: string } | { type: "notice"; message: string };

export async function runLaunch(
  body: { config: LaunchConfig; assets: Asset[]; dryRun: boolean },
  onEvent: (e: StreamEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const res = await fetch("/api/launch", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
    signal,
  });
  if (!res.ok || !res.body) {
    const j = (await res.json().catch(() => ({}))) as { error?: string; issues?: string[] };
    throw new Error(j.issues?.join(" ") || j.error || `Launch failed (${res.status})`);
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buf = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buf += decoder.decode(value, { stream: true });
    let nl: number;
    while ((nl = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, nl).trim();
      buf = buf.slice(nl + 1);
      if (line) onEvent(JSON.parse(line) as StreamEvent);
    }
  }
  if (buf.trim()) onEvent(JSON.parse(buf) as StreamEvent);
}

export function adsManagerUrl(record: Pick<LaunchRecord, "accountId" | "campaign">): string | null {
  if (!record.campaign.id || record.campaign.id.startsWith("DRYRUN")) return null;
  const act = record.accountId.replace("act_", "");
  return `https://adsmanager.facebook.com/adsmanager/manage/ads?act=${act}&selected_campaign_ids=${record.campaign.id}`;
}
