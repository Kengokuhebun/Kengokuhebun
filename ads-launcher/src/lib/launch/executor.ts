/**
 * Runs a Plan against the Meta Graph API, one object at a time, and reports
 * progress through `emit`. A failure in one ad set or ad does not stop the
 * rest. Everything is created PAUSED.
 *
 * No Node-only imports here, so it can be unit-tested with a fake graph.
 */
import { findEnabledEnhancements, findRejectedFeatureKey } from "./advantage";
import { buildCreativePayload, Plan } from "./plan";
import type { Asset } from "./schema";

export interface GraphLike {
  get<T = Record<string, unknown>>(path: string, params?: Record<string, unknown>): Promise<T>;
  post<T = Record<string, unknown>>(path: string, params?: Record<string, unknown>): Promise<T>;
  postMultipart<T = Record<string, unknown>>(
    path: string,
    fields: Record<string, string>,
    file?: { field: string; data: Uint8Array; fileName: string; mime: string },
  ): Promise<T>;
}

export interface MediaSource {
  readBytes(key: string): Promise<Uint8Array>;
  /** URL Meta can download from, or null to upload the bytes directly. */
  remoteUrl(key: string): Promise<string | null>;
}

export type StepStatus = "running" | "done" | "error" | "warn" | "skipped";

export type LaunchEvent =
  | { type: "step"; id: string; label: string; status: StepStatus; detail?: string }
  | { type: "done"; record: LaunchRecord };

export interface LaunchRecord {
  id: string;
  createdAt: string;
  dryRun: boolean;
  accountId: string;
  campaign: { mode: "new" | "existing"; id?: string; name: string; error?: string };
  adsets: {
    name: string;
    id?: string;
    error?: string;
    warnings: string[];
    ads: {
      name: string;
      creativeName: string;
      assetName: string;
      kind: "image" | "video";
      id?: string;
      creativeId?: string;
      error?: string;
      warnings: string[];
    }[];
  }[];
  warnings: string[];
  totals: { adsetsCreated: number; adsCreated: number; failed: number };
  /** Dry run only: every call that would have been sent. */
  calls?: { method: string; path: string; params: unknown }[];
}

export interface ExecuteOptions {
  graph: GraphLike;
  media: MediaSource;
  accountId: string;
  plan: Plan;
  dryRun?: boolean;
  emit: (e: LaunchEvent) => void;
  sleep?: (ms: number) => Promise<void>;
  now?: () => Date;
  /** How long to wait for Meta to process a video. */
  videoTimeoutMs?: number;
  videoPollMs?: number;
  newId?: () => string;
}

function errText(err: unknown): string {
  if (err && typeof err === "object" && "describe" in err && typeof (err as { describe: unknown }).describe === "function") {
    return (err as { describe: () => string }).describe();
  }
  return err instanceof Error ? err.message : String(err);
}

function toBase64(data: Uint8Array): string {
  // Buffer exists on the server; btoa fallback keeps this module isomorphic.
  const B = (globalThis as { Buffer?: { from(d: Uint8Array): { toString(enc: string): string } } }).Buffer;
  if (B) return B.from(data).toString("base64");
  let s = "";
  for (let i = 0; i < data.length; i++) s += String.fromCharCode(data[i]);
  return btoa(s);
}

type MediaResult =
  | { ok: true; media: { imageHash: string } | { videoId: string; thumbnailUrl: string } }
  | { ok: false; error: string };

export async function executePlan(opts: ExecuteOptions): Promise<LaunchRecord> {
  const { graph, media, plan, emit } = opts;
  const act = opts.accountId;
  const sleep = opts.sleep ?? ((ms: number) => new Promise((r) => setTimeout(r, ms)));
  const now = opts.now ?? (() => new Date());
  const videoTimeout = opts.videoTimeoutMs ?? 20 * 60_000;
  const videoPoll = opts.videoPollMs ?? 5_000;

  const record: LaunchRecord = {
    id: opts.newId?.() ?? (globalThis.crypto?.randomUUID?.() ?? `launch-${now().getTime()}`),
    createdAt: now().toISOString(),
    dryRun: Boolean(opts.dryRun),
    accountId: act,
    campaign: { mode: plan.campaign.mode, name: plan.campaign.name },
    adsets: plan.adsets.map((s) => ({
      name: s.name,
      warnings: [],
      ads: s.ads.map((a) => ({
        name: a.name,
        creativeName: a.creative.name,
        assetName: a.asset.name,
        kind: a.asset.kind,
        warnings: [],
      })),
    })),
    warnings: [],
    totals: { adsetsCreated: 0, adsCreated: 0, failed: 0 },
  };
  const finish = () => {
    record.totals.adsetsCreated = record.adsets.filter((s) => s.id).length;
    record.totals.adsCreated = record.adsets.reduce((n, s) => n + s.ads.filter((a) => a.id).length, 0);
    record.totals.failed =
      record.adsets.reduce((n, s) => n + s.ads.filter((a) => a.error).length, 0) +
      (record.campaign.error ? 1 : 0);
    emit({ type: "done", record });
    return record;
  };

  // 1. Campaign
  let campaignId: string;
  if (plan.campaign.mode === "existing") {
    campaignId = plan.campaign.id;
    record.campaign.id = campaignId;
    emit({ type: "step", id: "campaign", label: `Using campaign "${plan.campaign.name}"`, status: "done" });
  } else {
    emit({ type: "step", id: "campaign", label: `Creating campaign "${plan.campaign.name}"`, status: "running" });
    try {
      const res = await graph.post<{ id: string }>(`/${act}/campaigns`, plan.campaign.payload);
      campaignId = res.id;
      record.campaign.id = campaignId;
      emit({ type: "step", id: "campaign", label: `Campaign created`, status: "done", detail: campaignId });
    } catch (err) {
      record.campaign.error = errText(err);
      emit({ type: "step", id: "campaign", label: "Campaign failed", status: "error", detail: record.campaign.error });
      return finish();
    }
  }

  // 2. Media: upload each unique asset once
  const assets = new Map<string, Asset>();
  for (const s of plan.adsets) for (const a of s.ads) assets.set(a.asset.id, a.asset);
  const mediaResults = new Map<string, MediaResult>();
  const pendingVideos: { asset: Asset; videoId: string }[] = [];

  for (const asset of assets.values()) {
    const stepId = `media-${asset.id}`;
    emit({ type: "step", id: stepId, label: `Uploading ${asset.kind} "${asset.name}"`, status: "running" });
    try {
      if (asset.kind === "image") {
        const bytes = await media.readBytes(asset.storageKey);
        const res = await graph.post<{ images?: Record<string, { hash: string }> }>(`/${act}/adimages`, {
          bytes: toBase64(bytes),
          name: asset.fileName || asset.name,
        });
        const hash = Object.values(res.images ?? {})[0]?.hash;
        if (!hash) throw new Error("Meta did not return an image hash");
        mediaResults.set(asset.id, { ok: true, media: { imageHash: hash } });
        emit({ type: "step", id: stepId, label: `Image "${asset.name}" uploaded`, status: "done", detail: hash });
      } else {
        const url = await media.remoteUrl(asset.storageKey);
        let res: { id: string };
        if (url) {
          res = await graph.post<{ id: string }>(`/${act}/advideos`, { file_url: url, name: asset.name });
        } else {
          const bytes = await media.readBytes(asset.storageKey);
          res = await graph.postMultipart<{ id: string }>(
            `/${act}/advideos`,
            { name: asset.name },
            { field: "source", data: bytes, fileName: asset.fileName || `${asset.name}.mp4`, mime: asset.mime },
          );
        }
        if (!res.id) throw new Error("Meta did not return a video id");
        pendingVideos.push({ asset, videoId: res.id });
        emit({ type: "step", id: stepId, label: `Video "${asset.name}" uploaded, Meta is processing it`, status: "running", detail: res.id });
      }
    } catch (err) {
      mediaResults.set(asset.id, { ok: false, error: errText(err) });
      emit({ type: "step", id: stepId, label: `Upload failed for "${asset.name}"`, status: "error", detail: errText(err) });
    }
  }

  // Wait for videos to finish processing, then fetch a thumbnail for each.
  for (const { asset, videoId } of pendingVideos) {
    const stepId = `media-${asset.id}`;
    try {
      const started = Date.now();
      for (;;) {
        const v = await graph.get<{ status?: { video_status?: string; processing_phase?: { error?: { message?: string } } } }>(
          `/${videoId}`,
          { fields: "status" },
        );
        const st = v.status?.video_status;
        if (st === "ready") break;
        if (st === "error") {
          throw new Error(`Meta could not process the video${v.status?.processing_phase?.error?.message ? `: ${v.status.processing_phase.error.message}` : ""}`);
        }
        if (Date.now() - started > videoTimeout) throw new Error("Timed out waiting for Meta to process the video");
        await sleep(videoPoll);
      }
      const thumbs = await graph.get<{ data?: { uri: string; is_preferred?: boolean }[] }>(`/${videoId}/thumbnails`);
      const list = thumbs.data ?? [];
      const thumb = (list.find((t) => t.is_preferred) ?? list[0])?.uri;
      if (!thumb) throw new Error("Meta returned no thumbnail for the video");
      mediaResults.set(asset.id, { ok: true, media: { videoId, thumbnailUrl: thumb } });
      emit({ type: "step", id: stepId, label: `Video "${asset.name}" ready`, status: "done", detail: videoId });
    } catch (err) {
      mediaResults.set(asset.id, { ok: false, error: errText(err) });
      emit({ type: "step", id: stepId, label: `Video "${asset.name}" failed`, status: "error", detail: errText(err) });
    }
  }

  // 3. Ad sets and ads
  const rejectedKeys = new Set<string>();
  let verifiedAudienceOnce = false;

  for (const [si, set] of plan.adsets.entries()) {
    const rs = record.adsets[si];
    const setStep = `adset-${si}`;
    if (!set.ads.some((a) => mediaResults.get(a.asset.id)?.ok)) {
      rs.error = "Skipped: none of its creatives uploaded, so no empty ad set was created.";
      emit({ type: "step", id: setStep, label: `Ad set "${set.name}" skipped`, status: "skipped", detail: rs.error });
      for (const [ai, ad] of rs.ads.entries()) {
        const m = mediaResults.get(set.ads[ai].asset.id);
        ad.error = `Media not available: ${m && !m.ok ? m.error : "unknown"}`;
      }
      continue;
    }
    emit({ type: "step", id: setStep, label: `Creating ad set "${set.name}"`, status: "running" });
    try {
      const res = await graph.post<{ id: string }>(`/${act}/adsets`, { ...set.payload, campaign_id: campaignId });
      rs.id = res.id;
      emit({ type: "step", id: setStep, label: `Ad set "${set.name}" created`, status: "done", detail: res.id });
    } catch (err) {
      rs.error = errText(err);
      emit({ type: "step", id: setStep, label: `Ad set "${set.name}" failed`, status: "error", detail: rs.error });
      for (const ad of rs.ads) {
        ad.error = "Skipped because its ad set failed.";
      }
      continue;
    }

    // Read back once per launch: is Advantage+ audience really off?
    const wantAudienceOff =
      (set.payload.targeting as { targeting_automation?: { advantage_audience?: number } })?.targeting_automation
        ?.advantage_audience === 0;
    if (wantAudienceOff && !verifiedAudienceOnce && !opts.dryRun) {
      verifiedAudienceOnce = true;
      try {
        const back = await graph.get<{ targeting?: { targeting_automation?: { advantage_audience?: number } } }>(`/${rs.id}`, {
          fields: "targeting",
        });
        if (back.targeting?.targeting_automation?.advantage_audience === 1) {
          const w = "Meta reports Advantage+ audience is ON for this ad set even though we sent it OFF.";
          rs.warnings.push(w);
          emit({ type: "step", id: `${setStep}-verify`, label: w, status: "warn" });
        }
      } catch {
        // Verification is best-effort.
      }
    }

    for (const [ai, ad] of set.ads.entries()) {
      const ra = rs.ads[ai];
      const adStep = `ad-${si}-${ai}`;
      const m = mediaResults.get(ad.asset.id);
      if (!m || !m.ok) {
        ra.error = `Media not available: ${m && !m.ok ? m.error : "unknown"}`;
        emit({ type: "step", id: adStep, label: `Ad "${ad.name}" skipped`, status: "skipped", detail: ra.error });
        continue;
      }
      emit({ type: "step", id: adStep, label: `Creating ad "${ad.name}"`, status: "running" });
      try {
        // Creative, dropping any feature key this API version rejects.
        let creativeId: string | undefined;
        for (let attempt = 0; attempt < 12 && !creativeId; attempt++) {
          try {
            const res = await graph.post<{ id: string }>(
              `/${act}/adcreatives`,
              buildCreativePayload(ad.creative, m.media, rejectedKeys),
            );
            creativeId = res.id;
          } catch (err) {
            const key = ad.creative.advantageDisabled ? findRejectedFeatureKey(errText(err), rejectedKeys) : null;
            if (!key) throw err;
            if (key === "__unknown_feature__") {
              throw new Error(
                `Meta rejected the Advantage+ opt-out settings and did not say which one: ${errText(err)}. ` +
                  "Nothing was created for this ad, so no enhancement was left on by accident.",
              );
            }
            rejectedKeys.add(key);
            const w = `Meta (this API version) does not accept the setting "${key}", so it was not sent.`;
            record.warnings.push(w);
            emit({ type: "step", id: `${adStep}-key-${key}`, label: w, status: "warn" });
          }
        }
        if (!creativeId) throw new Error("Could not create the creative.");
        ra.creativeId = creativeId;

        const adRes = await graph.post<{ id: string }>(`/${act}/ads`, {
          name: ad.name,
          adset_id: rs.id,
          creative: { creative_id: creativeId },
          status: "PAUSED",
        });
        ra.id = adRes.id;

        if (ad.creative.advantageDisabled && !opts.dryRun) {
          try {
            const back = await graph.get<Parameters<typeof findEnabledEnhancements>[0]>(`/${creativeId}`, {
              fields: "degrees_of_freedom_spec,contextual_multi_ads",
            });
            const on = findEnabledEnhancements(back);
            if (on.length) {
              const w = `Meta shows these enhancements ON after creation: ${on.join(", ")}. Check this ad in Ads Manager.`;
              ra.warnings.push(w);
              emit({ type: "step", id: `${adStep}-verify`, label: w, status: "warn" });
            }
          } catch (err) {
            ra.warnings.push(`Could not read the creative back to verify: ${errText(err)}`);
          }
        }
        emit({ type: "step", id: adStep, label: `Ad "${ad.name}" created (paused)`, status: "done", detail: adRes.id });
      } catch (err) {
        ra.error = errText(err);
        emit({ type: "step", id: adStep, label: `Ad "${ad.name}" failed`, status: "error", detail: ra.error });
      }
    }
  }

  return finish();
}

/**
 * Dry-run graph: records every call and returns fake IDs, so a dry run walks
 * the exact same code path as a real launch without touching Meta.
 */
export class RecordingGraph implements GraphLike {
  calls: { method: string; path: string; params: unknown }[] = [];
  private n = 0;
  private id(prefix: string) {
    this.n += 1;
    return `DRYRUN_${prefix}_${this.n}`;
  }
  async get<T>(path: string, params: Record<string, unknown> = {}): Promise<T> {
    this.calls.push({ method: "GET", path, params });
    if (path.endsWith("/thumbnails")) return { data: [{ uri: "https://example.invalid/thumbnail.jpg", is_preferred: true }] } as T;
    return { status: { video_status: "ready" } } as T;
  }
  async post<T>(path: string, params: Record<string, unknown> = {}): Promise<T> {
    const shown = { ...params };
    if (typeof shown.bytes === "string") shown.bytes = "<the image file, base64>";
    if (typeof shown.file_url === "string") shown.file_url = "<signed storage URL>";
    this.calls.push({ method: "POST", path, params: shown });
    if (path.endsWith("/adimages")) return { images: { bytes: { hash: this.id("IMAGEHASH") } } } as T;
    const kind = path.split("/").pop() ?? "obj";
    return { id: this.id(kind.toUpperCase()) } as T;
  }
  async postMultipart<T>(path: string, fields: Record<string, string>, file?: { fileName: string; data: Uint8Array }): Promise<T> {
    this.calls.push({ method: "POST (multipart)", path, params: { ...fields, source: file ? `<${file.fileName}>` : undefined } });
    return { id: this.id("VIDEO") } as T;
  }
}
