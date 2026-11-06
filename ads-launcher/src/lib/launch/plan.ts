/**
 * Turns the form state into an exact list of Meta API payloads.
 * Pure and isomorphic: used by the browser for the live preview and by the
 * server for the real launch, so what you review is what gets sent.
 */
import { buildCreativeAdvantageFields } from "./advantage";
import { NamingContext, objectiveLabel, pad, ratioToken, renderName } from "./naming";
import {
  Asset,
  GOALS_BY_OBJECTIVE,
  LaunchConfig,
  launchConfigSchema,
} from "./schema";

export interface CreativeTemplate {
  name: string;
  kind: "image" | "video";
  pageId: string;
  instagramUserId: string;
  message: string;
  headline: string;
  description: string;
  link: string;
  cta: string;
  urlTags: string;
  advantageDisabled: boolean;
}

export interface PlannedAd {
  key: string;
  name: string;
  asset: Asset;
  creative: CreativeTemplate;
}

export interface PlannedAdSet {
  key: string;
  name: string;
  /** Everything except campaign_id, which is only known at launch time. */
  payload: Record<string, unknown>;
  ads: PlannedAd[];
}

export interface Plan {
  campaign:
    | { mode: "new"; name: string; payload: Record<string, unknown> }
    | { mode: "existing"; id: string; name: string };
  adsets: PlannedAdSet[];
  counts: { adsets: number; ads: number; images: number; videos: number };
}

const ZERO_DECIMAL = new Set(["JPY", "KRW", "VND", "CLP", "ISK", "PYG"]);

/** Meta budgets are integers in the account currency's minor unit. */
export function toMinorUnits(amount: number, currency: string): number {
  const factor = ZERO_DECIMAL.has(currency.toUpperCase()) ? 1 : 100;
  return Math.round(amount * factor);
}

export function campaignUsesCampaignBudget(config: LaunchConfig): boolean {
  return config.campaign.mode === "existing"
    ? config.campaign.existingHasCampaignBudget
    : config.campaign.budgetLevel === "campaign";
}

export function buildTargeting(config: LaunchConfig): Record<string, unknown> {
  const t = config.targeting;
  const targeting: Record<string, unknown> = {
    geo_locations: { countries: t.countries },
    age_min: t.ageMin,
    age_max: t.ageMax,
    targeting_automation: { advantage_audience: config.advantage.disableAll ? 0 : 1 },
  };
  if (t.genders === "male") targeting.genders = [1];
  if (t.genders === "female") targeting.genders = [2];
  if (t.customAudienceIds.length) targeting.custom_audiences = t.customAudienceIds.map((id) => ({ id }));
  if (t.excludedAudienceIds.length) {
    targeting.excluded_custom_audiences = t.excludedAudienceIds.map((id) => ({ id }));
  }
  if (config.placements.mode === "manual") {
    const platforms: string[] = [];
    if (config.placements.facebook.length) {
      platforms.push("facebook");
      targeting.facebook_positions = config.placements.facebook;
    }
    if (config.placements.instagram.length) {
      platforms.push("instagram");
      targeting.instagram_positions = config.placements.instagram;
    }
    targeting.publisher_platforms = platforms;
  }
  return targeting;
}

function budgetFields(config: LaunchConfig): Record<string, unknown> {
  const minor = toMinorUnits(config.budget.amount, config.currency);
  return {
    [config.budget.type === "daily" ? "daily_budget" : "lifetime_budget"]: minor,
    bid_strategy: "LOWEST_COST_WITHOUT_CAP",
  };
}

export function buildCampaignPayload(config: LaunchConfig, name: string): Record<string, unknown> {
  const payload: Record<string, unknown> = {
    name,
    objective: config.campaign.objective,
    status: "PAUSED",
    special_ad_categories: [],
  };
  if (config.campaign.budgetLevel === "campaign") {
    Object.assign(payload, budgetFields(config));
  } else {
    // Required by the API when the campaign has no campaign budget.
    payload.is_adset_budget_sharing_enabled = false;
  }
  return payload;
}

export function buildAdSetPayload(config: LaunchConfig, name: string): Record<string, unknown> {
  const goal = config.optimization.goal;
  const payload: Record<string, unknown> = {
    name,
    status: "PAUSED",
    billing_event: "IMPRESSIONS",
    optimization_goal: goal,
    targeting: buildTargeting(config),
  };
  if (goal === "OFFSITE_CONVERSIONS" || goal === "LANDING_PAGE_VIEWS" || goal === "LINK_CLICKS") {
    payload.destination_type = "WEBSITE";
  }
  if (goal === "OFFSITE_CONVERSIONS") {
    payload.promoted_object = {
      pixel_id: config.optimization.pixelId,
      custom_event_type: config.optimization.event,
    };
  }
  if (!campaignUsesCampaignBudget(config)) Object.assign(payload, budgetFields(config));
  if (config.schedule.startTime) payload.start_time = config.schedule.startTime;
  if (config.schedule.endTime) payload.end_time = config.schedule.endTime;
  return payload;
}

/** The creative payload, once the uploaded media is known. */
export function buildCreativePayload(
  t: CreativeTemplate,
  media: { imageHash: string } | { videoId: string; thumbnailUrl: string },
  rejectedKeys?: ReadonlySet<string>,
): Record<string, unknown> {
  const call_to_action = { type: t.cta, value: { link: t.link } };
  const object_story_spec: Record<string, unknown> = { page_id: t.pageId };
  if (t.instagramUserId) object_story_spec.instagram_user_id = t.instagramUserId;

  if ("imageHash" in media) {
    const link_data: Record<string, unknown> = {
      image_hash: media.imageHash,
      link: t.link,
      message: t.message,
      call_to_action,
    };
    if (t.headline) link_data.name = t.headline;
    if (t.description) link_data.description = t.description;
    object_story_spec.link_data = link_data;
  } else {
    const video_data: Record<string, unknown> = {
      video_id: media.videoId,
      image_url: media.thumbnailUrl,
      message: t.message,
      call_to_action,
    };
    if (t.headline) video_data.title = t.headline;
    if (t.description) video_data.link_description = t.description;
    object_story_spec.video_data = video_data;
  }

  const payload: Record<string, unknown> = {
    name: t.name,
    object_story_spec,
    ...buildCreativeAdvantageFields(t.advantageDisabled, rejectedKeys),
  };
  if (t.urlTags) payload.url_tags = t.urlTags.replace(/^\?/, "");
  return payload;
}

function chunk<T>(items: T[], size: number): T[][] {
  const out: T[][] = [];
  for (let i = 0; i < items.length; i += size) out.push(items.slice(i, i + size));
  return out;
}

export function defaultAudienceLabel(config: LaunchConfig): string {
  const t = config.targeting;
  const who = t.customAudienceIds.length ? "Custom" : "Broad";
  const g = t.genders === "all" ? "" : t.genders === "female" ? " F" : " M";
  return `${who} ${t.countries.join("+")} ${t.ageMin}-${t.ageMax}${g}`;
}

export function buildPlan(config: LaunchConfig, assets: Asset[]): Plan {
  const included = assets.filter((a) => a.included);
  const audience = config.targeting.audienceLabel.trim() || defaultAudienceLabel(config);
  const baseCtx: NamingContext = {
    date: config.launchDate,
    objective: objectiveLabel(config.campaign.objective),
    audience,
    country: config.targeting.countries.join("+"),
  };

  const campaignName =
    config.campaign.mode === "existing"
      ? config.campaign.existingName || config.campaign.existingId
      : renderName(config.naming.campaign, { ...baseCtx, campaign: config.campaign.label.trim() });
  baseCtx.campaign = config.campaign.mode === "existing" ? campaignName : config.campaign.label.trim();

  const groups =
    config.structure.mode === "single"
      ? [included]
      : config.structure.mode === "per_creative"
        ? included.map((a) => [a])
        : chunk(included, config.structure.chunkSize);

  let n = 0;
  const adsets: PlannedAdSet[] = groups
    .filter((g) => g.length)
    .map((group, gi) => {
      const groupLabel =
        config.structure.mode === "per_creative"
          ? group[0].name
          : config.structure.mode === "single"
            ? "All creatives"
            : `Set ${gi + 1}`;
      const first = group[0];
      const adsetName = renderName(config.naming.adset, {
        ...baseCtx,
        adset: groupLabel,
        creative: config.structure.mode === "per_creative" ? first.name : groupLabel,
        ratio: config.structure.mode === "per_creative" ? ratioToken(first.ratio) : "",
        type: config.structure.mode === "per_creative" ? (first.kind === "video" ? "VID" : "IMG") : "",
        n: pad(gi + 1),
      });
      const ads: PlannedAd[] = group.map((asset) => {
        n += 1;
        const ctx: NamingContext = {
          ...baseCtx,
          adset: groupLabel,
          creative: asset.name,
          ratio: ratioToken(asset.ratio),
          type: asset.kind === "video" ? "VID" : "IMG",
          n: pad(n),
        };
        const name = renderName(config.naming.ad, ctx);
        const o = asset.overrides ?? {};
        return {
          key: `ad-${gi}-${asset.id}`,
          name,
          asset,
          creative: {
            name: `${name} | creative`,
            kind: asset.kind,
            pageId: config.pageId,
            instagramUserId: config.instagramUserId ?? "",
            message: (o.primaryText?.trim() || config.copy.primaryText).trim(),
            headline: (o.headline?.trim() || config.copy.headline).trim(),
            description: (o.description?.trim() || config.copy.description).trim(),
            link: (o.link?.trim() || config.copy.link).trim(),
            cta: config.copy.cta,
            urlTags: config.copy.urlTags.trim(),
            advantageDisabled: config.advantage.disableAll,
          },
        };
      });
      return { key: `adset-${gi}`, name: adsetName, payload: buildAdSetPayload(config, adsetName), ads };
    });

  return {
    campaign:
      config.campaign.mode === "existing"
        ? { mode: "existing", id: config.campaign.existingId, name: campaignName }
        : { mode: "new", name: campaignName, payload: buildCampaignPayload(config, campaignName) },
    adsets,
    counts: {
      adsets: adsets.length,
      ads: adsets.reduce((s, a) => s + a.ads.length, 0),
      images: included.filter((a) => a.kind === "image").length,
      videos: included.filter((a) => a.kind === "video").length,
    },
  };
}

export interface Validation {
  errors: string[];
  warnings: string[];
}

function isHttpUrl(s: string): boolean {
  try {
    const u = new URL(s);
    return u.protocol === "https:" || u.protocol === "http:";
  } catch {
    return false;
  }
}

export function validateLaunch(raw: unknown, assets: Asset[]): Validation {
  const errors: string[] = [];
  const warnings: string[] = [];
  const parsed = launchConfigSchema.safeParse(raw);
  if (!parsed.success) {
    for (const issue of parsed.error.issues) {
      const where = issue.path.join(".");
      const msg = issue.message.startsWith("Invalid") || issue.message.startsWith("Too") ? `${where}: ${issue.message}` : issue.message;
      if (!errors.includes(msg)) errors.push(msg);
    }
    return { errors, warnings };
  }
  const c = parsed.data;
  const included = assets.filter((a) => a.included);

  if (!included.length) errors.push("Upload at least one creative and keep it ticked.");
  if (c.targeting.ageMin > c.targeting.ageMax) errors.push("Minimum age is above maximum age.");
  if (c.budget.type === "lifetime" && !c.schedule.endTime) errors.push("A lifetime budget needs an end date.");
  if (c.schedule.startTime && c.schedule.endTime && new Date(c.schedule.endTime) <= new Date(c.schedule.startTime)) {
    errors.push("End date must be after start date.");
  }
  if (c.schedule.startTime && new Date(c.schedule.startTime).getTime() < Date.now() - 5 * 60_000) {
    warnings.push("Start date is in the past. Meta will start the ad sets as soon as you switch them on.");
  }
  if (!GOALS_BY_OBJECTIVE[c.campaign.objective].includes(c.optimization.goal)) {
    errors.push("That optimisation goal does not fit the campaign objective.");
  }
  if (c.optimization.goal === "OFFSITE_CONVERSIONS" && !c.optimization.pixelId) {
    errors.push("Conversion optimisation needs a pixel. Pick one in Optimisation.");
  }
  if (c.placements.mode === "manual" && !c.placements.facebook.length && !c.placements.instagram.length) {
    errors.push("Manual placements: tick at least one placement.");
  }
  if (c.campaign.mode === "existing" && !c.campaign.existingId) errors.push("Pick the existing campaign.");
  if (c.budget.amount < 1) warnings.push("Budget under 1.00 is likely below Meta's minimum.");
  if (!c.copy.primaryText.trim() && included.some((a) => !a.overrides?.primaryText?.trim())) {
    warnings.push("Primary text is empty for some ads.");
  }
  for (const a of included) {
    const link = a.overrides?.link?.trim();
    if (link && !isHttpUrl(link)) errors.push(`"${a.name}": the link override is not a full URL.`);
  }
  const odd = included.filter((a) => a.ratio === "other");
  if (odd.length) {
    warnings.push(`${odd.length} creative(s) are not 1:1, 4:5 or 9:16: ${odd.map((a) => a.name).join(", ")}.`);
  }
  if (c.advantage.disableAll && c.placements.mode === "advantage") {
    warnings.push("Advantage+ placements is still on. Choose Manual placements if you want that off too.");
  }
  if (!c.advantage.disableAll && c.targeting.ageMax < 65) {
    warnings.push("With Advantage+ audience on, Meta treats the age range as a suggestion.");
  }
  if (c.advantage.disableAll && c.campaign.mode === "new" && c.campaign.budgetLevel === "campaign") {
    warnings.push("Campaign budget (Advantage campaign budget) is on. Choose ad set budget to turn it off.");
  }
  const plan = buildPlan(c, assets);
  if (plan.counts.adsets > 50) warnings.push(`This creates ${plan.counts.adsets} ad sets. That is a lot for one launch.`);
  return { errors, warnings };
}
