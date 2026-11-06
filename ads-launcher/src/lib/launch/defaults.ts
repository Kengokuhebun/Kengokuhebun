import type { LaunchConfig } from "./schema";

export function todayISO(d = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

export const DEFAULT_URL_TAGS =
  "utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.id}}";

/** Editable form state; account fields are filled from the account picker. */
export function defaultConfig(): LaunchConfig {
  return {
    accountId: "",
    currency: "USD",
    pageId: "",
    instagramUserId: "",
    launchDate: todayISO(),
    campaign: {
      mode: "new",
      existingId: "",
      existingName: "",
      existingHasCampaignBudget: false,
      label: "",
      objective: "OUTCOME_SALES",
      budgetLevel: "adset",
    },
    budget: { type: "daily", amount: 20 },
    schedule: { startTime: "", endTime: "" },
    optimization: { goal: "OFFSITE_CONVERSIONS", pixelId: "", event: "PURCHASE" },
    targeting: {
      countries: ["US"],
      ageMin: 18,
      ageMax: 65,
      genders: "all",
      customAudienceIds: [],
      excludedAudienceIds: [],
      audienceLabel: "",
    },
    placements: { mode: "advantage", facebook: ["feed", "story", "facebook_reels"], instagram: ["stream", "story", "reels"] },
    advantage: { disableAll: true },
    copy: { primaryText: "", headline: "", description: "", link: "", cta: "SHOP_NOW", urlTags: DEFAULT_URL_TAGS },
    structure: { mode: "per_creative", chunkSize: 3 },
    naming: {
      campaign: "{date} - {objective} - {campaign}",
      adset: "{date} - {audience} - {adset}",
      ad: "{date} - {audience} - {creative}",
    },
  };
}
