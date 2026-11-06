"use client";
import { ShieldCheck, ShieldOff } from "lucide-react";
import { useState } from "react";
import type { AccountData } from "@/lib/client/api";
import { CREATIVE_FEATURE_KEYS, FEATURE_LABELS } from "@/lib/launch/advantage";
import { DEFAULT_URL_TAGS } from "@/lib/launch/defaults";
import { NAMING_TOKENS, objectiveLabel } from "@/lib/launch/naming";
import { defaultAudienceLabel } from "@/lib/launch/plan";
import {
  CONVERSION_EVENTS,
  CTA_TYPES,
  FACEBOOK_POSITIONS,
  GOALS_BY_OBJECTIVE,
  INSTAGRAM_POSITIONS,
  LaunchConfig,
  Objective,
  OBJECTIVES,
  OptimizationGoal,
} from "@/lib/launch/schema";
import { useStore } from "@/lib/store";
import { Badge, Callout, Checkbox, cn, Field, Input, Section, Segmented, Select, Switch, Textarea } from "../ui";

const pretty = (s: string) => s.toLowerCase().replace(/_/g, " ").replace(/^\w/, (c) => c.toUpperCase());

const GOAL_LABEL: Record<OptimizationGoal, string> = {
  OFFSITE_CONVERSIONS: "Conversions (pixel event)",
  LANDING_PAGE_VIEWS: "Landing page views",
  LINK_CLICKS: "Link clicks",
  REACH: "Reach",
  IMPRESSIONS: "Impressions",
};

const POSITION_LABEL: Record<string, string> = {
  feed: "Feed",
  story: "Stories",
  facebook_reels: "Reels",
  marketplace: "Marketplace",
  video_feeds: "Video feeds",
  search: "Search results",
  profile_feed: "Profile feed",
  stream: "Feed",
  reels: "Reels",
  explore: "Explore",
  explore_home: "Explore home",
};

/** datetime-local value <-> ISO with offset */
function toLocalInput(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}`;
}
function fromLocalInput(v: string): string {
  if (!v) return "";
  const d = new Date(v);
  return Number.isNaN(d.getTime()) ? "" : d.toISOString();
}

export function IdentitySection({ data, loading }: { data: AccountData | null; loading: boolean }) {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const page = data?.pages.find((p) => p.id === config.pageId);
  return (
    <Section step={2} id="identity" title="Identity" description="The Facebook Page and Instagram account the ads run from.">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Facebook Page">
          <Select
            value={config.pageId}
            onChange={(e) =>
              update((c) => {
                c.pageId = e.target.value;
                const p = data?.pages.find((x) => x.id === e.target.value);
                c.instagramUserId = p?.instagram?.id ?? "";
              })
            }
          >
            <option value="">{loading ? "Loading pages" : !data ? "Choose an ad account first" : data.pages.length ? "Choose a Page" : "No Pages found"}</option>
            {data?.pages.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </Select>
        </Field>
        <Field label="Instagram account" hint="optional">
          <Select value={config.instagramUserId} onChange={(e) => update((c) => void (c.instagramUserId = e.target.value))}>
            <option value="">Use the Page (no linked Instagram)</option>
            {data?.pages
              .filter((p) => p.instagram)
              .map((p) => (
                <option key={p.instagram!.id} value={p.instagram!.id}>
                  @{p.instagram!.username || p.instagram!.id} {p.id === page?.id ? "(linked to this Page)" : `(via ${p.name})`}
                </option>
              ))}
          </Select>
        </Field>
      </div>
      {data?.warnings.length ? (
        <Callout tone="amber" className="mt-4" title="Some account data could not be loaded">
          <ul className="list-disc pl-4">
            {data.warnings.map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </Callout>
      ) : null}
    </Section>
  );
}

export function CampaignSection({ data }: { data: AccountData | null }) {
  const config = useStore((s) => s.config);
  const account = useStore((s) => s.account);
  const update = useStore((s) => s.update);
  const c = config.campaign;
  const currency = account?.currency ?? config.currency;
  const usesCbo = c.mode === "existing" ? c.existingHasCampaignBudget : c.budgetLevel === "campaign";

  return (
    <Section step={3} id="campaign" title="Campaign and budget" description="Create a new campaign or add ad sets to one you already have.">
      <div className="space-y-5">
        <Segmented
          value={c.mode}
          onChange={(v) => update((d) => void (d.campaign.mode = v))}
          options={[
            { value: "new", label: "New campaign" },
            { value: "existing", label: "Existing campaign" },
          ]}
        />
        {c.mode === "new" ? (
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Campaign label" hint="used in {campaign}">
              <Input placeholder="e.g. R17 hook test" value={c.label} onChange={(e) => update((d) => void (d.campaign.label = e.target.value))} />
            </Field>
            <Field label="Objective">
              <Select
                value={c.objective}
                onChange={(e) =>
                  update((d) => {
                    d.campaign.objective = e.target.value as Objective;
                    const goals = GOALS_BY_OBJECTIVE[d.campaign.objective];
                    if (!goals.includes(d.optimization.goal)) d.optimization.goal = goals[0];
                  })
                }
              >
                {OBJECTIVES.map((o) => (
                  <option key={o} value={o}>
                    {objectiveLabel(o)}
                  </option>
                ))}
              </Select>
            </Field>
          </div>
        ) : (
          <Field label="Campaign">
            <Select
              value={c.existingId}
              onChange={(e) =>
                update((d) => {
                  const camp = data?.campaigns.find((x) => x.id === e.target.value);
                  d.campaign.existingId = camp?.id ?? "";
                  d.campaign.existingName = camp?.name ?? "";
                  d.campaign.existingHasCampaignBudget = camp?.hasCampaignBudget ?? false;
                  if (camp && (OBJECTIVES as readonly string[]).includes(camp.objective)) {
                    d.campaign.objective = camp.objective as Objective;
                    const goals = GOALS_BY_OBJECTIVE[d.campaign.objective];
                    if (!goals.includes(d.optimization.goal)) d.optimization.goal = goals[0];
                  }
                })
              }
            >
              <option value="">{data?.campaigns.length ? "Choose a campaign" : "No active or paused campaigns found"}</option>
              {data?.campaigns.map((camp) => (
                <option key={camp.id} value={camp.id}>
                  {camp.name} · {objectiveLabel(camp.objective)} · {pretty(camp.status)}
                  {camp.hasCampaignBudget ? " · campaign budget" : ""}
                </option>
              ))}
            </Select>
            {c.existingId && !(OBJECTIVES as readonly string[]).includes(data?.campaigns.find((x) => x.id === c.existingId)?.objective ?? "") ? (
              <p className="mt-1.5 text-xs text-warning">This campaign uses an objective this tool does not support yet. Ad sets may be rejected.</p>
            ) : null}
          </Field>
        )}

        <div className="grid gap-4 sm:grid-cols-3">
          {c.mode === "new" ? (
            <Field label="Budget level">
              <Select value={c.budgetLevel} onChange={(e) => update((d) => void (d.campaign.budgetLevel = e.target.value as "campaign" | "adset"))}>
                <option value="adset">Ad set budget (ABO)</option>
                <option value="campaign">Campaign budget (CBO)</option>
              </Select>
            </Field>
          ) : (
            <Field label="Budget level">
              <div className="flex h-9 items-center text-sm text-muted-foreground">{usesCbo ? "Campaign budget (set in Ads Manager)" : "Ad set budget"}</div>
            </Field>
          )}
          {!(c.mode === "existing" && usesCbo) ? (
            <>
              <Field label="Budget type">
                <Select value={config.budget.type} onChange={(e) => update((d) => void (d.budget.type = e.target.value as "daily" | "lifetime"))}>
                  <option value="daily">Daily</option>
                  <option value="lifetime">Lifetime</option>
                </Select>
              </Field>
              <Field label={`Amount (${currency})`} hint={usesCbo ? "per campaign" : "per ad set"}>
                <Input
                  type="number"
                  min={1}
                  step="0.01"
                  inputMode="decimal"
                  value={Number.isFinite(config.budget.amount) ? config.budget.amount : ""}
                  onChange={(e) => update((d) => void (d.budget.amount = parseFloat(e.target.value)))}
                />
              </Field>
            </>
          ) : null}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Start" hint="blank = when you switch it on">
            <Input
              type="datetime-local"
              value={toLocalInput(config.schedule.startTime)}
              onChange={(e) => update((d) => void (d.schedule.startTime = fromLocalInput(e.target.value)))}
            />
          </Field>
          <Field label="End" hint={config.budget.type === "lifetime" ? "required for lifetime budget" : "optional"}>
            <Input
              type="datetime-local"
              value={toLocalInput(config.schedule.endTime)}
              onChange={(e) => update((d) => void (d.schedule.endTime = fromLocalInput(e.target.value)))}
            />
          </Field>
        </div>
        {account?.timezone ? (
          <p className="-mt-2 text-xs text-muted-foreground">
            Times are in your computer&apos;s time zone. The ad account runs on {account.timezone}.
          </p>
        ) : null}
      </div>
    </Section>
  );
}

export function AudienceSection({ data }: { data: AccountData | null }) {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const t = config.targeting;
  const [countryInput, setCountryInput] = useState("");

  const addCountries = (raw: string) => {
    const codes = raw
      .toUpperCase()
      .split(/[\s,;+]+/)
      .filter((x) => /^[A-Z]{2}$/.test(x));
    if (codes.length) update((d) => void (d.targeting.countries = [...new Set([...d.targeting.countries, ...codes])]));
    setCountryInput("");
  };

  const toggleAudience = (field: "customAudienceIds" | "excludedAudienceIds", id: string, on: boolean) =>
    update((d) => {
      const set = new Set(d.targeting[field]);
      if (on) set.add(id);
      else set.delete(id);
      d.targeting[field] = [...set];
      const other = field === "customAudienceIds" ? "excludedAudienceIds" : "customAudienceIds";
      if (on) d.targeting[other] = d.targeting[other].filter((x) => x !== id);
    });

  return (
    <Section step={4} id="audience" title="Audience and placements">
      <div className="space-y-5">
        <div className="grid gap-4 lg:grid-cols-2">
          <Field label="Countries" hint="2-letter codes, e.g. US, GB">
            <div className="flex min-h-9 flex-wrap items-center gap-1.5 rounded-md border bg-card px-2 py-1.5">
              {t.countries.map((code) => (
                <Badge key={code} tone="blue" className="gap-1 text-xs">
                  {code}
                  <button
                    onClick={() => update((d) => void (d.targeting.countries = d.targeting.countries.filter((x) => x !== code)))}
                    aria-label={`Remove ${code}`}
                    className="hover:text-danger"
                  >
                    ×
                  </button>
                </Badge>
              ))}
              <input
                className="min-w-24 flex-1 bg-transparent text-sm outline-none"
                placeholder={t.countries.length ? "Add" : "US"}
                value={countryInput}
                onChange={(e) => setCountryInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === "," || e.key === " ") {
                    e.preventDefault();
                    addCountries(countryInput);
                  } else if (e.key === "Backspace" && !countryInput && t.countries.length) {
                    update((d) => void d.targeting.countries.pop());
                  }
                }}
                onBlur={() => countryInput && addCountries(countryInput)}
              />
            </div>
            <div className="mt-1.5 flex gap-1">
              {["US", "GB", "CA", "AU", "IE", "NZ"]
                .filter((x) => !t.countries.includes(x))
                .map((x) => (
                  <button key={x} className="rounded border px-1.5 py-0.5 text-[11px] text-muted-foreground hover:bg-muted" onClick={() => addCountries(x)}>
                    + {x}
                  </button>
                ))}
            </div>
          </Field>
          <div className="grid grid-cols-3 gap-3">
            <Field label="Age min">
              <Input type="number" min={13} max={65} value={t.ageMin} onChange={(e) => update((d) => void (d.targeting.ageMin = parseInt(e.target.value || "18", 10)))} />
            </Field>
            <Field label="Age max" hint="65 = 65+">
              <Input type="number" min={13} max={65} value={t.ageMax} onChange={(e) => update((d) => void (d.targeting.ageMax = parseInt(e.target.value || "65", 10)))} />
            </Field>
            <Field label="Gender">
              <Select value={t.genders} onChange={(e) => update((d) => void (d.targeting.genders = e.target.value as "all" | "male" | "female"))}>
                <option value="all">All</option>
                <option value="female">Women</option>
                <option value="male">Men</option>
              </Select>
            </Field>
          </div>
        </div>

        <Field label="Audience label" hint="used in {audience}">
          <Input
            placeholder={defaultAudienceLabel(config)}
            value={t.audienceLabel}
            onChange={(e) => update((d) => void (d.targeting.audienceLabel = e.target.value))}
          />
        </Field>

        {data?.audiences.length ? (
          <details className="rounded-lg border">
            <summary className="cursor-pointer px-3 py-2 text-sm font-medium">
              Custom audiences{" "}
              <span className="font-normal text-muted-foreground">
                ({t.customAudienceIds.length} included, {t.excludedAudienceIds.length} excluded)
              </span>
            </summary>
            <div className="max-h-64 overflow-auto border-t">
              <table className="w-full text-sm">
                <thead className="sticky top-0 bg-muted text-xs text-muted-foreground">
                  <tr>
                    <th className="px-3 py-1.5 text-left font-medium">Audience</th>
                    <th className="px-3 py-1.5 font-medium">Include</th>
                    <th className="px-3 py-1.5 font-medium">Exclude</th>
                  </tr>
                </thead>
                <tbody>
                  {data.audiences.map((a) => (
                    <tr key={a.id} className="border-t">
                      <td className="px-3 py-1.5">
                        {a.name} <span className="text-xs text-muted-foreground">{pretty(a.subtype)}</span>
                      </td>
                      <td className="text-center">
                        <input type="checkbox" className="accent-[var(--primary)]" checked={t.customAudienceIds.includes(a.id)} onChange={(e) => toggleAudience("customAudienceIds", a.id, e.target.checked)} />
                      </td>
                      <td className="text-center">
                        <input type="checkbox" className="accent-[var(--danger)]" checked={t.excludedAudienceIds.includes(a.id)} onChange={(e) => toggleAudience("excludedAudienceIds", a.id, e.target.checked)} />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        ) : null}

        <div>
          <div className="mb-2 flex items-center justify-between">
            <span className="text-xs font-medium text-foreground/80">Placements</span>
            <Segmented
              value={config.placements.mode}
              onChange={(v) => update((d) => void (d.placements.mode = v))}
              options={[
                { value: "advantage", label: "Advantage+ placements" },
                { value: "manual", label: "Manual" },
              ]}
            />
          </div>
          {config.placements.mode === "manual" ? (
            <div className="grid gap-4 rounded-lg border p-4 sm:grid-cols-2">
              <PositionGroup
                title="Facebook"
                options={FACEBOOK_POSITIONS}
                selected={config.placements.facebook}
                onChange={(v) => update((d) => void (d.placements.facebook = v as LaunchConfig["placements"]["facebook"]))}
              />
              <PositionGroup
                title="Instagram"
                options={INSTAGRAM_POSITIONS}
                selected={config.placements.instagram}
                onChange={(v) => update((d) => void (d.placements.instagram = v as LaunchConfig["placements"]["instagram"]))}
              />
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">Meta chooses placements across Facebook, Instagram, Messenger and Audience Network.</p>
          )}
        </div>
      </div>
    </Section>
  );
}

function PositionGroup({ title, options, selected, onChange }: { title: string; options: readonly string[]; selected: string[]; onChange: (v: string[]) => void }) {
  return (
    <div>
      <div className="mb-2 flex items-center justify-between text-sm font-medium">
        {title}
        <button className="text-xs font-normal text-primary" onClick={() => onChange(selected.length === options.length ? [] : [...options])}>
          {selected.length === options.length ? "None" : "All"}
        </button>
      </div>
      <div className="grid grid-cols-2 gap-1.5">
        {options.map((o) => (
          <Checkbox
            key={o}
            label={POSITION_LABEL[o] ?? o}
            checked={selected.includes(o)}
            onChange={(on) => onChange(on ? [...selected, o] : selected.filter((x) => x !== o))}
          />
        ))}
      </div>
    </div>
  );
}

export function OptimizationSection({ data }: { data: AccountData | null }) {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const o = config.optimization;
  const goals = GOALS_BY_OBJECTIVE[config.campaign.objective];
  return (
    <Section step={5} id="optimization" title="Optimisation">
      <div className="grid gap-4 sm:grid-cols-3">
        <Field label="Optimise for">
          <Select value={o.goal} onChange={(e) => update((d) => void (d.optimization.goal = e.target.value as OptimizationGoal))}>
            {goals.map((g) => (
              <option key={g} value={g}>
                {GOAL_LABEL[g]}
              </option>
            ))}
          </Select>
        </Field>
        {o.goal === "OFFSITE_CONVERSIONS" ? (
          <>
            <Field label="Pixel / dataset">
              <Select value={o.pixelId} onChange={(e) => update((d) => void (d.optimization.pixelId = e.target.value))}>
                <option value="">{data?.pixels.length ? "Choose a pixel" : "No pixels found"}</option>
                {data?.pixels.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} {p.last_fired_time ? "" : "(never fired)"}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="Conversion event">
              <Select value={o.event} onChange={(e) => update((d) => void (d.optimization.event = e.target.value as (typeof CONVERSION_EVENTS)[number]))}>
                {CONVERSION_EVENTS.map((ev) => (
                  <option key={ev} value={ev}>
                    {pretty(ev)}
                  </option>
                ))}
              </Select>
            </Field>
          </>
        ) : null}
      </div>
    </Section>
  );
}

export function CopySection() {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const c = config.copy;
  return (
    <Section step={6} id="copy" title="Ad copy" description="Used for every ad unless a creative has its own copy.">
      <div className="grid gap-4 lg:grid-cols-2">
        <Field label="Primary text" hint={`${c.primaryText.length} chars`} className="lg:row-span-2">
          <Textarea className="min-h-44" value={c.primaryText} onChange={(e) => update((d) => void (d.copy.primaryText = e.target.value))} />
        </Field>
        <Field label="Headline" hint={`${c.headline.length}/255`}>
          <Input value={c.headline} maxLength={255} onChange={(e) => update((d) => void (d.copy.headline = e.target.value))} />
        </Field>
        <Field label="Description" hint="optional">
          <Input value={c.description} maxLength={255} onChange={(e) => update((d) => void (d.copy.description = e.target.value))} />
        </Field>
        <Field label="Website URL">
          <Input type="url" placeholder="https://" value={c.link} onChange={(e) => update((d) => void (d.copy.link = e.target.value.trim()))} />
        </Field>
        <Field label="Call to action">
          <Select value={c.cta} onChange={(e) => update((d) => void (d.copy.cta = e.target.value as (typeof CTA_TYPES)[number]))}>
            {CTA_TYPES.map((x) => (
              <option key={x} value={x}>
                {pretty(x)}
              </option>
            ))}
          </Select>
        </Field>
        <Field
          label="URL parameters"
          className="lg:col-span-2"
          hint={
            c.urlTags !== DEFAULT_URL_TAGS ? (
              <button className="text-primary" onClick={() => update((d) => void (d.copy.urlTags = DEFAULT_URL_TAGS))}>
                Reset to default UTMs
              </button>
            ) : (
              "Meta fills {{ad.id}} etc."
            )
          }
        >
          <Input className="font-mono text-xs" value={c.urlTags} onChange={(e) => update((d) => void (d.copy.urlTags = e.target.value))} />
        </Field>
      </div>
    </Section>
  );
}

export function AdvantageSection() {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const on = config.advantage.disableAll;
  return (
    <Section
      step={7}
      id="advantage"
      title="Advantage+ override"
      description="Stop Meta changing your creative, copy or audience."
      right={on ? <Badge tone="green">Enhancements OFF</Badge> : <Badge tone="amber">Meta defaults</Badge>}
    >
      <div className={cn("flex items-start gap-4 rounded-xl border-2 p-4 transition-colors", on ? "border-success/40 bg-success/5" : "border-warning/40 bg-warning/5")}>
        <div className="pt-0.5">{on ? <ShieldCheck className="h-6 w-6 text-success" /> : <ShieldOff className="h-6 w-6 text-warning" />}</div>
        <div className="flex-1">
          <label htmlFor="adv-toggle" className="block cursor-pointer text-[15px] font-semibold">
            Disable all Advantage+ enhancements
          </label>
          <p className="mt-0.5 text-sm text-muted-foreground">
            {on
              ? "Every creative is sent with each enhancement set to OPT_OUT, multi-advertiser ads off, and Advantage+ audience off. After creating each ad, the tool reads it back from Meta and warns you if anything came back on."
              : "Meta's defaults apply. Meta may add text variations, touch up images, add music, crop or expand media, and widen your audience."}
          </p>
        </div>
        <Switch id="adv-toggle" size="lg" checked={on} onCheckedChange={(v) => update((d) => void (d.advantage.disableAll = v))} aria-label="Disable all Advantage+ enhancements" />
      </div>
      {on ? (
        <details className="mt-3">
          <summary className="cursor-pointer text-sm text-muted-foreground hover:text-foreground">What gets turned off ({CREATIVE_FEATURE_KEYS.length + 2} settings)</summary>
          <ul className="mt-2 grid gap-x-6 gap-y-1 text-xs text-muted-foreground sm:grid-cols-2 lg:grid-cols-3">
            {[...CREATIVE_FEATURE_KEYS, "contextual_multi_ads", "advantage_audience"].map((k) => (
              <li key={k} className="flex items-baseline gap-1.5">
                <span className="text-success">✓</span>
                <span>
                  {FEATURE_LABELS[k] ?? k} <code className="text-[10px] opacity-60">{k}</code>
                </span>
              </li>
            ))}
          </ul>
          <p className="mt-2 text-xs text-muted-foreground">
            Music is not added because no audio is sent. Placements and campaign budget are separate settings above. If a Meta API version stops accepting one of these settings, it is
            skipped and you get a warning.
          </p>
        </details>
      ) : null}
    </Section>
  );
}

export function StructureSection() {
  const config = useStore((s) => s.config);
  const update = useStore((s) => s.update);
  const s = config.structure;
  return (
    <Section step={8} id="structure" title="Structure and naming">
      <div className="space-y-5">
        <div className="flex flex-wrap items-end gap-4">
          <Field label="How to split creatives into ad sets" className="min-w-0 max-w-full">
            <Segmented
              value={s.mode}
              onChange={(v) => update((d) => void (d.structure.mode = v))}
              options={[
                { value: "per_creative", label: "1 ad set per creative" },
                { value: "single", label: "All in 1 ad set" },
                { value: "chunks", label: "Groups of N" },
              ]}
            />
          </Field>
          {s.mode === "chunks" ? (
            <Field label="Creatives per ad set" className="w-40">
              <Input type="number" min={1} max={50} value={s.chunkSize} onChange={(e) => update((d) => void (d.structure.chunkSize = Math.max(1, parseInt(e.target.value || "1", 10))))} />
            </Field>
          ) : null}
        </div>
        <div className="grid gap-4 lg:grid-cols-3">
          {(["campaign", "adset", "ad"] as const).map((k) => (
            <Field key={k} label={k === "adset" ? "Ad set name" : k === "ad" ? "Ad name" : "Campaign name"}>
              <Input
                className="font-mono text-xs"
                value={config.naming[k]}
                disabled={k === "campaign" && config.campaign.mode === "existing"}
                onChange={(e) => update((d) => void (d.naming[k] = e.target.value))}
              />
            </Field>
          ))}
        </div>
        <div className="flex flex-wrap gap-1.5">
          {NAMING_TOKENS.map((t) => (
            <span key={t.token} title={t.help} className="rounded border bg-muted px-1.5 py-0.5 font-mono text-[11px] text-muted-foreground">
              {`{${t.token}}`}
            </span>
          ))}
          <span className="text-[11px] text-muted-foreground">[Date] style works too.</span>
        </div>
      </div>
    </Section>
  );
}
