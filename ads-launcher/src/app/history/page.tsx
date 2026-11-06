"use client";
import { ChevronRight, ExternalLink, RefreshCw } from "lucide-react";
import { useState } from "react";
import { Badge, Button, Callout, Card, cn } from "@/components/ui";
import { useApi } from "@/lib/client/api";
import { adsManagerUrl } from "@/lib/client/launch";
import type { LaunchRecord } from "@/lib/launch/executor";

export default function HistoryPage() {
  const { data, error, loading, reload } = useApi<{ launches: LaunchRecord[] }>("/api/history");
  const launches = data?.launches ?? [];
  return (
    <div className="mx-auto max-w-5xl space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold">Launch history</h1>
          <p className="text-sm text-muted-foreground">Every real launch, with the IDs Meta returned. Dry runs are not saved.</p>
        </div>
        <Button variant="outline" size="sm" onClick={reload} disabled={loading}>
          <RefreshCw className={cn("h-3.5 w-3.5", loading && "animate-spin")} /> Refresh
        </Button>
      </div>
      {error ? <Callout tone="red">{error}</Callout> : null}
      {!loading && !launches.length && !error ? (
        <Card className="p-8 text-center text-sm text-muted-foreground">No launches yet.</Card>
      ) : null}
      {launches.map((r) => (
        <LaunchRow key={r.id} r={r} />
      ))}
    </div>
  );
}

function LaunchRow({ r }: { r: LaunchRecord }) {
  const [open, setOpen] = useState(false);
  const link = adsManagerUrl(r);
  const tone = r.totals.failed ? (r.totals.adsCreated ? "amber" : "red") : "green";
  return (
    <Card>
      <button className="flex w-full items-center gap-3 px-4 py-3 text-left" onClick={() => setOpen((v) => !v)}>
        <ChevronRight className={cn("h-4 w-4 text-muted-foreground transition-transform", open && "rotate-90")} />
        <div className="min-w-0 flex-1">
          <div className="truncate text-sm font-medium">{r.campaign.name}</div>
          <div className="text-xs text-muted-foreground">
            {new Date(r.createdAt).toLocaleString()} · {r.accountId}
          </div>
        </div>
        <Badge tone={tone}>
          {r.totals.adsCreated} ads{r.totals.failed ? ` · ${r.totals.failed} failed` : ""}
        </Badge>
        {link ? (
          <a href={link} target="_blank" rel="noreferrer" onClick={(e) => e.stopPropagation()} className="text-primary" title="Open in Ads Manager">
            <ExternalLink className="h-4 w-4" />
          </a>
        ) : null}
      </button>
      {open ? (
        <div className="border-t px-4 py-3 text-sm">
          {r.campaign.error ? <Callout tone="red" className="mb-2">Campaign: {r.campaign.error}</Callout> : null}
          {r.warnings.map((w) => (
            <Callout key={w} tone="amber" className="mb-2">
              {w}
            </Callout>
          ))}
          <div className="text-xs text-muted-foreground">Campaign ID {r.campaign.id ?? "none"}</div>
          <ul className="mt-2 space-y-2">
            {r.adsets.map((s, i) => (
              <li key={i}>
                <div className="font-medium">
                  {s.name} <span className="font-mono text-xs font-normal text-muted-foreground">{s.id ?? ""}</span>
                </div>
                {s.error ? <div className="text-xs text-danger">{s.error}</div> : null}
                <ul className="ml-4 mt-1 space-y-0.5">
                  {s.ads.map((a, j) => (
                    <li key={j} className="text-xs">
                      <span className={a.error ? "text-danger" : ""}>{a.name}</span>{" "}
                      <span className="font-mono text-muted-foreground">{a.id ?? ""}</span>
                      {a.error ? <div className="text-danger">{a.error}</div> : null}
                      {a.warnings.map((w) => (
                        <div key={w} className="text-warning">
                          {w}
                        </div>
                      ))}
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </Card>
  );
}
