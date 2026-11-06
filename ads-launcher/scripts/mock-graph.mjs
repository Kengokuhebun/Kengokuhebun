#!/usr/bin/env node
/**
 * A fake Meta Graph API for testing the app end to end without a real ad
 * account. NOT used in normal running.
 *
 *   node scripts/mock-graph.mjs            # listens on :4010
 *   META_GRAPH_BASE=http://localhost:4010 META_ACCESS_TOKEN=test npm run dev
 *
 * It mimics the endpoints the app calls, stores what it receives, and echoes
 * creatives back with every enhancement OPT_OUT (or OPT_IN for one key when
 * MOCK_FLIP=1, to test the read-back warning). GET /__calls lists all calls.
 */
import http from "node:http";

const PORT = Number(process.env.PORT || 4010);
const calls = [];
const objects = new Map();
let n = 1000;
const id = () => String(++n);

async function readBody(req) {
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const buf = Buffer.concat(chunks);
  const type = req.headers["content-type"] || "";
  if (type.startsWith("application/x-www-form-urlencoded")) return Object.fromEntries(new URLSearchParams(buf.toString()));
  if (type.startsWith("multipart/form-data")) {
    const form = await new Request("http://x", { method: "POST", headers: { "content-type": type }, body: buf }).formData();
    const fields = {};
    for (const [k, v] of form.entries()) fields[k] = typeof v === "string" ? v : `<file ${v.name}, ${v.size} bytes>`;
    return fields;
  }
  return {};
}

const parse = (v) => {
  try {
    return JSON.parse(v);
  } catch {
    return v;
  }
};

function send(res, status, body) {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  if (url.pathname === "/__calls") return send(res, 200, calls);
  const path = url.pathname.replace(/^\/v\d+\.\d+/, "");
  const params = req.method === "GET" ? Object.fromEntries(url.searchParams) : await readBody(req);
  const token = params.access_token;
  delete params.access_token;
  delete params.appsecret_proof;
  calls.push({ method: req.method, path, params });
  if (token !== (process.env.MOCK_TOKEN || "test-token")) {
    return send(res, 400, { error: { message: "Invalid OAuth access token.", type: "OAuthException", code: 190, fbtrace_id: "MOCK" } });
  }

  if (req.method === "GET") {
    if (path === "/me") return send(res, 200, { id: "999", name: "Mock System User" });
    if (path === "/me/adaccounts")
      return send(res, 200, {
        data: [
          { id: "act_111", name: "Ninu US", account_status: 1, currency: "GBP", timezone_name: "Europe/London", business: { name: "Ninu" } },
          { id: "act_222", name: "Old account", account_status: 2, currency: "USD", timezone_name: "America/Los_Angeles" },
        ],
      });
    if (path.endsWith("/promote_pages") || path === "/me/accounts")
      return send(res, 200, { data: [{ id: "p_1", name: "Ninu", instagram_business_account: { id: "ig_1", username: "tryninu" } }] });
    if (path.endsWith("/adspixels")) return send(res, 200, { data: [{ id: "px_1", name: "Ninu Pixel", last_fired_time: "2026-11-05T10:00:00+0000" }] });
    if (path.endsWith("/customaudiences"))
      return send(res, 200, { data: [{ id: "ca_1", name: "Purchasers 180d", subtype: "WEBSITE", approximate_count_lower_bound: 1000 }] });
    if (path.endsWith("/campaigns"))
      return send(res, 200, { data: [{ id: "c_old", name: "Existing CBO campaign", objective: "OUTCOME_SALES", effective_status: "PAUSED", daily_budget: "5000" }] });
    if (path.endsWith("/thumbnails")) return send(res, 200, { data: [{ uri: "https://mock.thumb/1.jpg", is_preferred: true }] });
    const obj = objects.get(path.slice(1));
    if (obj?.kind === "video") return send(res, 200, { status: { video_status: "ready" } });
    if (obj?.kind === "creative") {
      const spec = parse(obj.params.degrees_of_freedom_spec ?? "{}");
      if (process.env.MOCK_FLIP && spec.creative_features_spec) spec.creative_features_spec.inline_comment = { enroll_status: "OPT_IN" };
      return send(res, 200, { id: obj.id, degrees_of_freedom_spec: spec, contextual_multi_ads: parse(obj.params.contextual_multi_ads ?? "null") });
    }
    if (obj?.kind === "adset") return send(res, 200, { id: obj.id, targeting: parse(obj.params.targeting) });
    return send(res, 404, { error: { message: `Unsupported get request ${path}`, code: 100 } });
  }

  // POST
  const kind = path.split("/").pop();
  if (kind === "adimages") return send(res, 200, { images: { bytes: { hash: `hash_${id()}`, url: "https://mock/img.jpg" } } });
  const newId = id();
  const map = { campaigns: "campaign", adsets: "adset", adcreatives: "creative", ads: "ad", advideos: "video" };
  if (!map[kind]) return send(res, 400, { error: { message: `Unsupported post ${path}`, code: 100 } });
  if (kind === "adsets" && !params.campaign_id) return send(res, 400, { error: { message: "campaign_id required", code: 100 } });
  if (kind === "adcreatives" && process.env.MOCK_REJECT_KEY) {
    const spec = parse(params.degrees_of_freedom_spec ?? "{}");
    if (spec.creative_features_spec?.[process.env.MOCK_REJECT_KEY]) {
      return send(res, 400, { error: { message: `Invalid parameter: ${process.env.MOCK_REJECT_KEY} is not a valid creative feature`, code: 100 } });
    }
  }
  objects.set(newId, { id: newId, kind: map[kind], params });
  return send(res, 200, { id: newId });
});

server.listen(PORT, () => console.log(`Mock Graph API on http://localhost:${PORT}`));
