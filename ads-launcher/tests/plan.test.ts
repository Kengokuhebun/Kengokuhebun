import { describe, expect, it } from "vitest";
import { buildCreativeAdvantageFields, CREATIVE_FEATURE_KEYS, findEnabledEnhancements, findRejectedFeatureKey } from "@/lib/launch/advantage";
import { renderName } from "@/lib/launch/naming";
import { buildCreativePayload, buildPlan, toMinorUnits, validateLaunch } from "@/lib/launch/plan";
import { makeAsset, makeConfig } from "./helpers";

describe("naming", () => {
  it("replaces curly and square tokens, case-insensitive", () => {
    expect(renderName("[Date] - {audience} - {CREATIVE}", { date: "2026-11-07", audience: "Broad US", creative: "Hook1" })).toBe(
      "2026-11-07 - Broad US - Hook1",
    );
  });
  it("leaves unknown tokens visible and collapses empty separators", () => {
    expect(renderName("{date} - {oops}", { date: "d" })).toBe("d - {oops}");
    expect(renderName("{date} - {audience} - {creative}", { date: "d", audience: "", creative: "c" })).toBe("d - c");
  });
});

describe("budgets", () => {
  it("converts to minor units", () => {
    expect(toMinorUnits(20, "GBP")).toBe(2000);
    expect(toMinorUnits(12.345, "USD")).toBe(1235);
    expect(toMinorUnits(1000, "JPY")).toBe(1000);
  });
});

describe("buildPlan", () => {
  it("one ad set per creative, ABO, Advantage+ off", () => {
    const plan = buildPlan(makeConfig(), [makeAsset(1), makeAsset(2), makeAsset(3, { included: false })]);
    expect(plan.counts).toEqual({ adsets: 2, ads: 2, images: 2, videos: 0 });
    expect(plan.campaign.mode).toBe("new");
    if (plan.campaign.mode !== "new") throw new Error();
    expect(plan.campaign.name).toBe("2026-11-07 - Sales - Ninu R17");
    expect(plan.campaign.payload).toMatchObject({ status: "PAUSED", is_adset_budget_sharing_enabled: false, special_ad_categories: [] });
    expect(plan.campaign.payload).not.toHaveProperty("daily_budget");
    const s = plan.adsets[0];
    expect(s.name).toBe("2026-11-07 - Broad US 18-65 - Creative 1");
    expect(s.payload).toMatchObject({
      status: "PAUSED",
      daily_budget: 2000,
      optimization_goal: "OFFSITE_CONVERSIONS",
      promoted_object: { pixel_id: "px1", custom_event_type: "PURCHASE" },
      targeting: { targeting_automation: { advantage_audience: 0 }, geo_locations: { countries: ["US"] } },
    });
    expect(s.ads[0].name).toBe("2026-11-07 - Broad US 18-65 - Creative 1");
  });

  it("CBO puts budget on the campaign, not ad sets; chunks group creatives", () => {
    const plan = buildPlan(
      makeConfig((c) => {
        c.campaign.budgetLevel = "campaign";
        c.structure = { mode: "chunks", chunkSize: 2 };
      }),
      [1, 2, 3, 4, 5].map((i) => makeAsset(i)),
    );
    if (plan.campaign.mode !== "new") throw new Error();
    expect(plan.campaign.payload).toMatchObject({ daily_budget: 2000, bid_strategy: "LOWEST_COST_WITHOUT_CAP" });
    expect(plan.adsets.map((s) => s.ads.length)).toEqual([2, 2, 1]);
    expect(plan.adsets[2].name).toContain("Set 3");
    expect(plan.adsets[0].payload).not.toHaveProperty("daily_budget");
    expect(plan.adsets[2].ads[0].name).toContain("Creative 5");
  });

  it("existing campaign with campaign budget: no ad set budget", () => {
    const plan = buildPlan(
      makeConfig((c) => {
        c.campaign.mode = "existing";
        c.campaign.existingId = "c9";
        c.campaign.existingName = "Old";
        c.campaign.existingHasCampaignBudget = true;
        c.structure.mode = "single";
      }),
      [makeAsset(1)],
    );
    expect(plan.campaign).toEqual({ mode: "existing", id: "c9", name: "Old" });
    expect(plan.adsets[0].payload).not.toHaveProperty("daily_budget");
  });

  it("manual placements and per-asset overrides", () => {
    const plan = buildPlan(
      makeConfig((c) => {
        c.placements = { mode: "manual", facebook: [], instagram: ["stream", "reels"] };
        c.targeting.genders = "female";
      }),
      [makeAsset(1, { overrides: { primaryText: "Override body", link: "https://x.test/a" } })],
    );
    expect(plan.adsets[0].payload.targeting).toMatchObject({
      publisher_platforms: ["instagram"],
      instagram_positions: ["stream", "reels"],
      genders: [2],
    });
    expect(plan.adsets[0].payload.targeting).not.toHaveProperty("facebook_positions");
    const t = plan.adsets[0].ads[0].creative;
    expect(t.message).toBe("Override body");
    expect(t.link).toBe("https://x.test/a");
    expect(t.headline).toBe("Headline");
  });
});

describe("creative payload", () => {
  const plan = buildPlan(makeConfig((c) => (c.instagramUserId = "ig1")), [makeAsset(1)]);
  const t = plan.adsets[0].ads[0].creative;

  it("image creative with every enhancement opted out", () => {
    const p = buildCreativePayload(t, { imageHash: "h1" });
    expect(p.object_story_spec).toMatchObject({
      page_id: "p1",
      instagram_user_id: "ig1",
      link_data: { image_hash: "h1", link: "https://tryninu.store/products/kit", message: "Body", name: "Headline", call_to_action: { type: "SHOP_NOW" } },
    });
    const spec = (p.degrees_of_freedom_spec as { creative_features_spec: Record<string, { enroll_status: string }> }).creative_features_spec;
    expect(Object.keys(spec).sort()).toEqual([...CREATIVE_FEATURE_KEYS].sort());
    expect(Object.values(spec).every((v) => v.enroll_status === "OPT_OUT")).toBe(true);
    expect(p.contextual_multi_ads).toEqual({ enroll_status: "OPT_OUT" });
    expect(p).not.toHaveProperty("asset_feed_spec");
    expect(p.url_tags).toContain("utm_source=facebook");
  });

  it("video creative", () => {
    const p = buildCreativePayload({ ...t, kind: "video" }, { videoId: "v1", thumbnailUrl: "https://t/1.jpg" });
    expect(p.object_story_spec).toMatchObject({ video_data: { video_id: "v1", image_url: "https://t/1.jpg", title: "Headline" } });
  });

  it("omits Advantage fields when the switch is off, drops rejected keys", () => {
    expect(buildCreativeAdvantageFields(false)).toEqual({});
    const f = buildCreativeAdvantageFields(true, new Set(["music_x", "image_uncrop", "contextual_multi_ads"]));
    expect((f.degrees_of_freedom_spec as { creative_features_spec: object }).creative_features_spec).not.toHaveProperty("image_uncrop");
    expect(f).not.toHaveProperty("contextual_multi_ads");
  });
});

describe("advantage helpers", () => {
  it("finds the rejected key, longest match first", () => {
    expect(findRejectedFeatureKey("Invalid parameter: video_uncrop is not a valid feature", new Set())).toBe("video_uncrop");
    expect(findRejectedFeatureKey("(#100) Param degrees_of_freedom_spec[creative_features_spec][image_template] is not valid", new Set())).toBe(
      "image_templates",
    );
    expect(findRejectedFeatureKey("Invalid creative_features_spec", new Set())).toBe("__unknown_feature__");
    expect(findRejectedFeatureKey("Page not found", new Set())).toBeNull();
  });
  it("reports enhancements that came back on", () => {
    expect(
      findEnabledEnhancements({
        degrees_of_freedom_spec: { creative_features_spec: { image_touchups: { enroll_status: "OPT_IN" }, inline_comment: { enroll_status: "OPT_OUT" } } },
        contextual_multi_ads: { enroll_status: "OPT_IN" },
      }),
    ).toEqual(["image_touchups", "contextual_multi_ads"]);
  });
});

describe("validateLaunch", () => {
  it("passes a good config", () => {
    expect(validateLaunch(makeConfig(), [makeAsset(1)]).errors).toEqual([]);
  });
  it("catches the common mistakes", () => {
    const v = validateLaunch(
      makeConfig((c) => {
        c.optimization.pixelId = "";
        c.targeting.ageMin = 50;
        c.targeting.ageMax = 30;
        c.budget.type = "lifetime";
        c.placements = { mode: "manual", facebook: [], instagram: [] };
      }),
      [makeAsset(1, { included: false })],
    );
    expect(v.errors.join(" ")).toMatch(/at least one creative/);
    expect(v.errors.join(" ")).toMatch(/Minimum age/);
    expect(v.errors.join(" ")).toMatch(/lifetime budget/);
    expect(v.errors.join(" ")).toMatch(/pixel/);
    expect(v.errors.join(" ")).toMatch(/tick at least one placement/);
  });
  it("reports schema errors in plain words", () => {
    const v = validateLaunch(makeConfig((c) => (c.copy.link = "tryninu.store")), [makeAsset(1)]);
    expect(v.errors[0]).toMatch(/full website URL/);
  });
});
