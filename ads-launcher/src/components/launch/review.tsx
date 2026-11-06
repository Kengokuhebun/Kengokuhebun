"use client";
import { AlertTriangle, CheckCircle2, ChevronRight, CircleSlash, ExternalLink, FlaskConical, Loader2, Rocket, Save, XCircle } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { adsManagerUrl, runLaunch, StepRow, StreamEvent } from "@/lib/client/launch";
import type { LaunchRecord } from "@/lib/launch/executor";
import { buildPlan, Plan, Validation } from "@/lib/launch/plan";
import { launchConfigSchema } from "@/lib/launch/schema";
import { useStore } from "@/lib/store";
import { Badge, Button, Callout, Card, cn, Input, Section, Select } from "../ui";

export function usePlan(): Plan | null {
  const config = useStore((s) => s.config);
  const assets = useStore((s) => s.assets);
  return useMemo(() => {
    const parsed = launchConfigSchema.safeParse(config);
    if (!parsed.success) {
      // Still show names with partial data where possible.
      try {
        return buildPlan(config, assets);
      } catch {
        return null;
      }
    }
    return buildPlan(parsed.data, assets);
  }, [config, assets]);
}

export function PlanPreview({ plan }: { plan: Plan | null }) {
  const copy = useStore((s) => s.config.copy);
  const [open, setOpen] = useState<Record<string, boolean>>({});
  if (!plan || !plan.adsets.length) {
    return (
      <Section step={9} id="review" title="Review">
        <p className="text-sm text-muted-foreground">Upload creatives to see exactly what will be created.</p>
      </Section>
    );
  }
  return (
    <Section
      step={9}
      id="review"
      title="Review"
      description="Exactly what will be created in Meta, all paused."
      right={
        <div className="flex gap-1.5">
          <Badge tone="dark">{plan.counts.adsets} ad sets</Badge>
          <Badge tone="dark">{plan.counts.ads} ads</Badge>
        </div>
      }
    >
      <div className="rounded-lg border">
        <div className="flex items-center gap-2 border-b bg-muted/60 px-3 py-2 text-sm">
          <Badge tone="blue">{plan.campaign.mode === "new" ? "New campaign" : "Existing campaign"}</Badge>
          <span className="font-medium">{plan.campaign.name || <i className="text-muted-foreground">unnamed</i>}</span>
        </div>
        <ul className="divide-y">
          {plan.adsets.map((s) => {
            const isOpen = open[s.key] ?? plan.adsets.length <= 6;
            return (
              <li key={s.key}>
                <button className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-muted/50" onClick={() => setOpen((o) => ({ ...o, [s.key]: !isOpen }))}>
                  <ChevronRight className={cn("h-4 w-4 text-muted-foreground transition-transform", isOpen && "rotate-90")} />
                  <Badge>Ad set</Badge>
                  <span className="min-w-0 flex-1 truncate font-medium">{s.name}</span>
                  <span className="text-xs text-muted-foreground">{s.ads.length} ads</span>
                </button>
                {isOpen ? (
                  <ul className="pb-2 pl-11 pr-3">
                    {s.ads.map((a) => (
                      <li key={a.key} className="flex items-center gap-2 py-1 text-sm">
                        <Badge tone={a.asset.kind === "video" ? "amber" : "green"}>{a.asset.kind === "video" ? "Video" : "Image"}</Badge>
                        <Badge>{a.asset.ratio}</Badge>
                        <span className="min-w-0 flex-1 truncate">{a.name}</span>
                        {a.creative.link !== copy.link || a.creative.message !== copy.primaryText.trim() ? (
                          <Badge tone="blue">custom copy</Badge>
                        ) : null}
                      </li>
                    ))}
                  </ul>
                ) : null}
              </li>
            );
          })}
        </ul>
      </div>
    </Section>
  );
}

export function LaunchPanel({ plan, validation }: { plan: Plan | null; validation: Validation }) {
  const config = useStore((s) => s.config);
  const assets = useStore((s) => s.assets);
  const presets = useStore((s) => s.presets);
  const savePreset = useStore((s) => s.savePreset);
  const loadPreset = useStore((s) => s.loadPreset);
  const deletePreset = useStore((s) => s.deletePreset);
  const resetConfig = useStore((s) => s.resetConfig);
  const [running, setRunning] = useState<null | { dryRun: boolean }>(null);
  const [presetName, setPresetName] = useState("");

  const blocked = validation.errors.length > 0 || !plan?.counts.ads;

  return (
    <div className="space-y-4">
      <Card className="p-4">
        <div className="text-sm font-semibold">Launch</div>
        <div className="mt-3 grid grid-cols-3 gap-2 text-center">
          {[
            ["Ad sets", plan?.counts.adsets ?? 0],
            ["Ads", plan?.counts.ads ?? 0],
            ["Videos", plan?.counts.videos ?? 0],
          ].map(([k, v]) => (
            <div key={k} className="rounded-lg bg-muted py-2">
              <div className="text-xl font-semibold tabular-nums">{v}</div>
              <div className="text-[11px] text-muted-foreground">{k}</div>
            </div>
          ))}
        </div>

        <div className="mt-3 space-y-2">
          {validation.errors.map((e) => (
            <div key={e} className="flex gap-2 text-xs text-danger">
              <XCircle className="mt-px h-3.5 w-3.5 shrink-0" />
              {e}
            </div>
          ))}
          {validation.warnings.map((w) => (
            <div key={w} className="flex gap-2 text-xs text-warning">
              <AlertTriangle className="mt-px h-3.5 w-3.5 shrink-0" />
              {w}
            </div>
          ))}
          {!validation.errors.length && plan?.counts.ads ? (
            <div className="flex gap-2 text-xs text-success">
              <CheckCircle2 className="mt-px h-3.5 w-3.5 shrink-0" />
              Ready. Everything is created paused.
            </div>
          ) : null}
        </div>

        <div className="mt-4 grid gap-2">
          <Button size="lg" disabled={blocked} onClick={() => setRunning({ dryRun: false })} data-testid="launch-btn">
            <Rocket className="h-4 w-4" /> Launch {plan?.counts.ads ?? 0} ads (paused)
          </Button>
          <Button variant="outline" disabled={blocked} onClick={() => setRunning({ dryRun: true })} data-testid="dryrun-btn">
            <FlaskConical className="h-4 w-4" /> Dry run (nothing sent to Meta)
          </Button>
        </div>
      </Card>

      <Card className="p-4">
        <div className="text-sm font-semibold">Presets</div>
        <p className="mt-0.5 text-xs text-muted-foreground">Save these settings to reuse them. Creatives are not saved in presets.</p>
        <div className="mt-3 flex gap-2">
          <Input placeholder="Preset name" value={presetName} onChange={(e) => setPresetName(e.target.value)} className="h-8 text-xs" />
          <Button
            size="sm"
            variant="outline"
            disabled={!presetName.trim()}
            onClick={() => {
              savePreset(presetName.trim());
              setPresetName("");
            }}
          >
            <Save className="h-3.5 w-3.5" /> Save
          </Button>
        </div>
        {presets.length ? (
          <div className="mt-2 flex gap-2">
            <Select
              className="h-8 text-xs"
              value=""
              onChange={(e) => {
                if (e.target.value) loadPreset(e.target.value);
              }}
            >
              <option value="">Load a preset</option>
              {presets.map((p) => (
                <option key={p.name} value={p.name}>
                  {p.name}
                </option>
              ))}
            </Select>
            <Select
              className="h-8 w-28 text-xs"
              value=""
              onChange={(e) => {
                if (e.target.value && confirm(`Delete preset "${e.target.value}"?`)) deletePreset(e.target.value);
              }}
            >
              <option value="">Delete</option>
              {presets.map((p) => (
                <option key={p.name} value={p.name}>
                  {p.name}
                </option>
              ))}
            </Select>
          </div>
        ) : null}
        <button className="mt-3 text-xs text-muted-foreground hover:text-danger" onClick={() => confirm("Reset all settings to defaults? Creatives stay.") && resetConfig()}>
          Reset settings to defaults
        </button>
      </Card>

      {running ? <LaunchDialog dryRun={running.dryRun} body={{ config, assets, dryRun: running.dryRun }} plan={plan!} onClose={() => setRunning(null)} /> : null}
    </div>
  );
}

function StatusIcon({ status }: { status: StepRow["status"] }) {
  if (status === "running") return <Loader2 className="h-4 w-4 animate-spin text-primary" />;
  if (status === "done") return <CheckCircle2 className="h-4 w-4 text-success" />;
  if (status === "error") return <XCircle className="h-4 w-4 text-danger" />;
  if (status === "warn") return <AlertTriangle className="h-4 w-4 text-warning" />;
  return <CircleSlash className="h-4 w-4 text-muted-foreground" />;
}

function LaunchDialog({
  dryRun,
  body,
  plan,
  onClose,
}: {
  dryRun: boolean;
  body: Parameters<typeof runLaunch>[0];
  plan: Plan;
  onClose: () => void;
}) {
  const [phase, setPhase] = useState<"confirm" | "running" | "finished">(dryRun ? "running" : "confirm");
  const [steps, setSteps] = useState<StepRow[]>([]);
  const [record, setRecord] = useState<LaunchRecord | null>(null);
  const [notices, setNotices] = useState<string[]>([]);
  const [fatal, setFatal] = useState<string | null>(null);
  const started = useRef(false);

  const start = () => {
    if (started.current) return;
    started.current = true;
    setPhase("running");
    const onEvent = (e: StreamEvent) => {
      if (e.type === "step") {
        setSteps((prev) => {
          const i = prev.findIndex((s) => s.id === e.id);
          const row = { id: e.id, label: e.label, status: e.status, detail: e.detail };
          if (i === -1) return [...prev, row];
          const next = prev.slice();
          next[i] = row;
          return next;
        });
      } else if (e.type === "done") setRecord(e.record);
      else if (e.type === "notice") setNotices((n) => [...n, e.message]);
      else if (e.type === "error") setFatal(e.error);
    };
    runLaunch(body, onEvent)
      .catch((err: Error) => setFatal(err.message))
      .finally(() => setPhase("finished"));
  };

  useEffect(() => {
    if (dryRun) start();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const link = record ? adsManagerUrl(record) : null;
  const done = steps.filter((s) => s.status === "done").length;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" role="dialog" aria-modal>
      <Card className="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden shadow-2xl">
        <div className="flex items-center justify-between border-b px-5 py-3">
          <div className="font-semibold">{dryRun ? "Dry run" : phase === "confirm" ? "Confirm launch" : phase === "running" ? "Launching" : "Launch finished"}</div>
          {phase !== "running" ? (
            <Button variant="ghost" size="sm" onClick={onClose}>
              Close
            </Button>
          ) : (
            <span className="text-xs text-muted-foreground">Keep this tab open</span>
          )}
        </div>

        {phase === "confirm" ? (
          <div className="space-y-4 p-5 text-sm">
            <p>
              This creates <b>{plan.campaign.mode === "new" ? "1 campaign, " : ""}
              {plan.counts.adsets} ad sets and {plan.counts.ads} ads</b> in <b>{body.config.accountId}</b>. Everything is created <b>paused</b>, so nothing spends until you switch it on in Ads Manager.
            </p>
            <Callout tone={body.config.advantage.disableAll ? "green" : "amber"}>
              Advantage+ enhancements: <b>{body.config.advantage.disableAll ? "OFF" : "Meta defaults (ON)"}</b>
            </Callout>
            <div className="flex justify-end gap-2">
              <Button variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button onClick={start} data-testid="confirm-launch">
                <Rocket className="h-4 w-4" /> Launch now
              </Button>
            </div>
          </div>
        ) : (
          <div className="min-h-0 flex-1 overflow-auto p-5">
            {record ? <Summary record={record} link={link} /> : null}
            {fatal ? (
              <Callout tone="red" title="Launch stopped" className="mb-4">
                {fatal}
              </Callout>
            ) : null}
            {notices.map((n) => (
              <Callout key={n} tone="amber" className="mb-3">
                {n}
              </Callout>
            ))}
            {phase === "running" && !steps.length ? (
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" /> Starting
              </div>
            ) : null}
            {steps.length ? (
              <div>
                <div className="mb-2 text-xs font-medium text-muted-foreground">
                  Progress · {done} of {steps.length} steps done
                </div>
                <ul className="space-y-1" data-testid="launch-steps">
                  {steps.map((s) => (
                    <li key={s.id} className="flex gap-2 text-sm">
                      <span className="mt-0.5">
                        <StatusIcon status={s.status} />
                      </span>
                      <span className="min-w-0 flex-1">
                        <span className={cn(s.status === "error" && "text-danger", s.status === "warn" && "text-warning")}>{s.label}</span>
                        {s.detail ? <span className="block break-all font-mono text-[11px] text-muted-foreground">{s.detail}</span> : null}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
            {record?.calls ? (
              <details className="mt-4">
                <summary className="cursor-pointer text-sm font-medium">Show the {record.calls.length} API calls that would be sent</summary>
                <pre className="mt-2 max-h-96 overflow-auto rounded-lg bg-[#0f1115] p-3 text-[11px] leading-relaxed text-[#d7dae0]">
                  {record.calls.map((c) => `${c.method} ${c.path}\n${JSON.stringify(c.params, null, 2)}`).join("\n\n")}
                </pre>
              </details>
            ) : null}
          </div>
        )}
      </Card>
    </div>
  );
}

function Summary({ record, link }: { record: LaunchRecord; link: string | null }) {
  const ok = record.totals.failed === 0;
  const adWarnings = record.adsets.reduce((n, s) => n + s.warnings.length + s.ads.reduce((m, a) => m + a.warnings.length, 0), 0);
  return (
    <Callout
      tone={ok && !adWarnings ? "green" : record.totals.adsCreated ? "amber" : "red"}
      className="mb-4"
      title={
        record.dryRun
          ? `Dry run passed: ${record.totals.adsCreated} ads would be created. Nothing was sent to Meta.`
          : ok
            ? `Done. ${record.totals.adsCreated} ads created in ${record.totals.adsetsCreated} ad sets, all paused.${adWarnings ? ` ${adWarnings} warning(s) below need a look before you switch them on.` : ""}`
            : `Finished with problems: ${record.totals.adsCreated} ads created, ${record.totals.failed} failed.`
      }
    >
      {link ? (
        <a href={link} target="_blank" rel="noreferrer" className="mt-1 inline-flex items-center gap-1 font-medium underline">
          Open in Ads Manager <ExternalLink className="h-3.5 w-3.5" />
        </a>
      ) : null}
      {record.warnings.length ? (
        <ul className="mt-1 list-disc pl-4 text-xs">
          {record.warnings.map((w) => (
            <li key={w}>{w}</li>
          ))}
        </ul>
      ) : null}
    </Callout>
  );
}
