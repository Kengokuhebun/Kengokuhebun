import { describe, expect, it } from "vitest";
import { executePlan, GraphLike, LaunchEvent, RecordingGraph } from "@/lib/launch/executor";
import { buildPlan } from "@/lib/launch/plan";
import { GraphClient, MetaApiError } from "@/lib/meta/graph";
import { makeAsset, makeConfig } from "./helpers";

type Handler = (method: string, path: string, params: Record<string, unknown>) => unknown;

class FakeGraph implements GraphLike {
  calls: { method: string; path: string; params: Record<string, unknown> }[] = [];
  constructor(private handler: Handler) {}
  private run<T>(method: string, path: string, params: Record<string, unknown>): Promise<T> {
    this.calls.push({ method, path, params });
    try {
      return Promise.resolve(this.handler(method, path, params) as T);
    } catch (e) {
      return Promise.reject(e);
    }
  }
  get<T>(path: string, params: Record<string, unknown> = {}) {
    return this.run<T>("GET", path, params);
  }
  post<T>(path: string, params: Record<string, unknown> = {}) {
    return this.run<T>("POST", path, params);
  }
  postMultipart<T>(path: string, fields: Record<string, string>) {
    return this.run<T>("MULTIPART", path, fields);
  }
}

const metaError = (message: string, code = 100) => new MetaApiError(400, { error: { message, code } }, "x");

function happyHandler(over: Partial<Record<string, Handler>> = {}): Handler {
  let n = 0;
  return (method, path, params) => {
    for (const [k, h] of Object.entries(over)) if (path.endsWith(k) && h) return h(method, path, params);
    n += 1;
    if (path.endsWith("/adimages")) return { images: { bytes: { hash: `hash${n}` } } };
    if (path.endsWith("/thumbnails")) return { data: [{ uri: "https://thumb/a.jpg", is_preferred: true }] };
    if (method === "GET" && params.fields === "status") return { status: { video_status: "ready" } };
    if (method === "GET") return {};
    return { id: `id${n}` };
  };
}

const media = { readBytes: async () => new Uint8Array([1, 2, 3]), remoteUrl: async () => null };
const noSleep = async () => {};

describe("executePlan", () => {
  it("creates campaign, uploads media once, ad sets, creatives and ads, all paused", async () => {
    const plan = buildPlan(
      makeConfig((c) => (c.structure.mode = "single")),
      [makeAsset(1), makeAsset(2, { kind: "video", mime: "video/mp4", ratio: "9:16" })],
    );
    const graph = new FakeGraph(happyHandler());
    const events: LaunchEvent[] = [];
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: (e) => events.push(e), sleep: noSleep });

    expect(rec.totals).toEqual({ adsetsCreated: 1, adsCreated: 2, failed: 0 });
    const posts = graph.calls.filter((c) => c.method !== "GET").map((c) => `${c.method} ${c.path}`);
    expect(posts).toEqual([
      "POST /act_123/campaigns",
      "POST /act_123/adimages",
      "MULTIPART /act_123/advideos",
      "POST /act_123/adsets",
      "POST /act_123/adcreatives",
      "POST /act_123/ads",
      "POST /act_123/adcreatives",
      "POST /act_123/ads",
    ]);
    for (const c of graph.calls.filter((c) => /campaigns|adsets|\/ads$/.test(c.path))) expect(c.params.status).toBe("PAUSED");
    const adset = graph.calls.find((c) => c.path.endsWith("/adsets"))!;
    expect(adset.params.campaign_id).toBeTruthy();
    const videoCreative = graph.calls.filter((c) => c.path.endsWith("/adcreatives"))[1];
    expect(videoCreative.params.object_story_spec).toMatchObject({ video_data: { image_url: "https://thumb/a.jpg" } });
    // read-back verification happened
    expect(graph.calls.some((c) => c.method === "GET" && c.params.fields === "degrees_of_freedom_spec,contextual_multi_ads")).toBe(true);
    expect(events.at(-1)?.type).toBe("done");
  });

  it("uses file_url for videos when storage gives a remote URL", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1, { kind: "video", mime: "video/mp4" })]);
    const graph = new FakeGraph(happyHandler());
    await executePlan({
      graph,
      media: { ...media, remoteUrl: async () => "https://signed/url" },
      plan,
      accountId: "act_123",
      emit: () => {},
      sleep: noSleep,
    });
    const v = graph.calls.find((c) => c.path.endsWith("/advideos"))!;
    expect(v.method).toBe("POST");
    expect(v.params.file_url).toBe("https://signed/url");
  });

  it("drops a feature key Meta rejects, retries, and remembers it for later ads", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1), makeAsset(2)]);
    const graph = new FakeGraph(
      happyHandler({
        "/adcreatives": (_m, _p, params) => {
          const spec = (params.degrees_of_freedom_spec as { creative_features_spec: Record<string, unknown> }).creative_features_spec;
          if ("video_filtering" in spec) throw metaError("Invalid parameter: video_filtering is not supported");
          return { id: "cr1" };
        },
      }),
    );
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(rec.totals.adsCreated).toBe(2);
    expect(graph.calls.filter((c) => c.path.endsWith("/adcreatives")).length).toBe(3); // 1 rejected + 2 ok
    expect(rec.warnings.join()).toMatch(/video_filtering/);
  });

  it("refuses to create the ad if Meta rejects opt-outs without naming the key", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1)]);
    const graph = new FakeGraph(
      happyHandler({
        "/adcreatives": () => {
          throw metaError("Invalid degrees_of_freedom_spec");
        },
      }),
    );
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(rec.totals.adsCreated).toBe(0);
    expect(rec.adsets[0].ads[0].error).toMatch(/no enhancement was left on/);
    expect(graph.calls.some((c) => c.path.endsWith("/ads"))).toBe(false);
  });

  it("flags enhancements that come back ON after creation", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1)]);
    const graph = new FakeGraph(
      happyHandler({
        cr: () => ({}),
      }),
    );
    // creative read-back returns an OPT_IN feature
    const original = graph.get.bind(graph);
    graph.get = (async (path: string, params: Record<string, unknown> = {}) => {
      if (params.fields === "degrees_of_freedom_spec,contextual_multi_ads") {
        return { degrees_of_freedom_spec: { creative_features_spec: { inline_comment: { enroll_status: "OPT_IN" } } } };
      }
      return original(path, params);
    }) as typeof graph.get;
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(rec.adsets[0].ads[0].warnings.join()).toMatch(/inline_comment/);
  });

  it("an ad set failure skips its ads but the rest continue", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1), makeAsset(2)]);
    let sets = 0;
    const graph = new FakeGraph(
      happyHandler({
        "/adsets": () => {
          sets += 1;
          if (sets === 1) throw metaError("Budget too low", 100);
          return { id: "set2" };
        },
      }),
    );
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(rec.adsets[0].error).toMatch(/Budget too low/);
    expect(rec.adsets[0].ads[0].error).toMatch(/Skipped/);
    expect(rec.adsets[1].ads[0].id).toBeTruthy();
    expect(rec.totals).toEqual({ adsetsCreated: 1, adsCreated: 1, failed: 1 });
  });

  it("does not create an empty ad set when its media failed", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1), makeAsset(2)]);
    let images = 0;
    const graph = new FakeGraph(
      happyHandler({
        "/adimages": () => {
          images += 1;
          if (images === 1) throw metaError("Image too small");
          return { images: { bytes: { hash: "h" } } };
        },
      }),
    );
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(graph.calls.filter((c) => c.path.endsWith("/adsets")).length).toBe(1);
    expect(rec.adsets[0].error).toMatch(/no empty ad set/);
    expect(rec.adsets[0].ads[0].error).toMatch(/Image too small/);
    expect(rec.totals).toEqual({ adsetsCreated: 1, adsCreated: 1, failed: 1 });
  });

  it("stops if the campaign fails", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1)]);
    const graph = new FakeGraph(
      happyHandler({
        "/campaigns": () => {
          throw metaError("No permission", 200);
        },
      }),
    );
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(rec.campaign.error).toMatch(/No permission/);
    expect(graph.calls.length).toBe(1);
  });

  it("waits for video processing and reports a processing error", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1, { kind: "video", mime: "video/mp4" })]);
    let polls = 0;
    const graph = new FakeGraph((method, path, params) => {
      if (method === "GET" && params.fields === "status") {
        polls += 1;
        return { status: { video_status: polls < 3 ? "processing" : "error" } };
      }
      return { id: "x" };
    });
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", emit: () => {}, sleep: noSleep });
    expect(polls).toBe(3);
    expect(rec.adsets[0].ads[0].error).toMatch(/could not process/);
  });

  it("dry run records calls and touches nothing", async () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1)]);
    const graph = new RecordingGraph();
    const rec = await executePlan({ graph, media, plan, accountId: "act_123", dryRun: true, emit: () => {}, sleep: noSleep });
    expect(rec.totals.adsCreated).toBe(1);
    expect(graph.calls.map((c) => c.path)).toEqual(["/act_123/campaigns", "/act_123/adimages", "/act_123/adsets", "/act_123/adcreatives", "/act_123/ads"]);
    expect(JSON.stringify(graph.calls)).toContain("the image file, base64");
  });
});

describe("GraphClient", () => {
  it("encodes objects as JSON, retries transient errors, hides the token", async () => {
    const seen: { url: string; body: string; auth?: string }[] = [];
    let n = 0;
    const fetchImpl = (async (url: string, init: RequestInit) => {
      seen.push({ url, body: String(init.body ?? ""), auth: (init.headers as Record<string, string>)?.authorization });
      n += 1;
      if (n === 1) return new Response(JSON.stringify({ error: { message: "Please reduce the amount", code: 17 } }), { status: 400 });
      return new Response(JSON.stringify({ id: "c1" }), { status: 200 });
    }) as unknown as typeof fetch;
    const g = new GraphClient({ token: "SECRET", version: "v25.0", base: "https://graph.test", fetchImpl, sleep: noSleep, appSecret: "s" });
    const res = await g.post<{ id: string }>("/act_1/campaigns", { name: "x", special_ad_categories: [] });
    expect(res.id).toBe("c1");
    expect(n).toBe(2);
    expect(seen[1].url).toBe("https://graph.test/v25.0/act_1/campaigns");
    const body = new URLSearchParams(seen[1].body);
    expect(body.get("special_ad_categories")).toBe("[]");
    expect(body.get("appsecret_proof")).toMatch(/^[0-9a-f]{64}$/);
    expect(body.get("access_token")).toBeNull();
    expect(seen[1].url).not.toContain("SECRET");
    expect(seen[1].auth).toBe("Bearer SECRET");
  });

  it("throws a readable MetaApiError without the token", async () => {
    const fetchImpl = (async () =>
      new Response(
        JSON.stringify({ error: { message: "Invalid parameter", code: 100, error_subcode: 1885183, error_user_title: "Ads creative post was created by an app in development mode", fbtrace_id: "T1" } }),
        { status: 400 },
      )) as unknown as typeof fetch;
    const g = new GraphClient({ token: "SECRET", version: "v25.0", base: "https://graph.test", fetchImpl, sleep: noSleep });
    const err = await g.get("/me").catch((e) => e);
    expect(err).toBeInstanceOf(MetaApiError);
    expect(err.describe()).toMatch(/development mode.*code 100, subcode 1885183.*trace T1/);
    expect(err.describe()).not.toContain("SECRET");
  });
});
