import { z } from "zod";

/**
 * Shared launch types. This file is imported by both the browser and the
 * server, so it must not import anything Node-only.
 */

export const OBJECTIVES = [
  "OUTCOME_SALES",
  "OUTCOME_TRAFFIC",
  "OUTCOME_LEADS",
  "OUTCOME_AWARENESS",
] as const;
export type Objective = (typeof OBJECTIVES)[number];

export const OPTIMIZATION_GOALS = [
  "OFFSITE_CONVERSIONS",
  "LANDING_PAGE_VIEWS",
  "LINK_CLICKS",
  "REACH",
  "IMPRESSIONS",
] as const;
export type OptimizationGoal = (typeof OPTIMIZATION_GOALS)[number];

/** Which optimisation goals make sense for each objective (first = default). */
export const GOALS_BY_OBJECTIVE: Record<Objective, OptimizationGoal[]> = {
  OUTCOME_SALES: ["OFFSITE_CONVERSIONS", "LANDING_PAGE_VIEWS", "LINK_CLICKS"],
  OUTCOME_TRAFFIC: ["LANDING_PAGE_VIEWS", "LINK_CLICKS", "REACH", "IMPRESSIONS"],
  OUTCOME_LEADS: ["OFFSITE_CONVERSIONS", "LANDING_PAGE_VIEWS", "LINK_CLICKS"],
  OUTCOME_AWARENESS: ["REACH", "IMPRESSIONS"],
};

export const CONVERSION_EVENTS = [
  "PURCHASE",
  "ADD_TO_CART",
  "INITIATED_CHECKOUT",
  "ADD_PAYMENT_INFO",
  "LEAD",
  "COMPLETE_REGISTRATION",
  "CONTENT_VIEW",
  "SEARCH",
  "SUBSCRIBE",
  "START_TRIAL",
] as const;

export const CTA_TYPES = [
  "SHOP_NOW",
  "LEARN_MORE",
  "ORDER_NOW",
  "BUY_NOW",
  "GET_OFFER",
  "SIGN_UP",
  "SUBSCRIBE",
  "CONTACT_US",
  "DOWNLOAD",
  "SEE_MORE",
] as const;

export const FACEBOOK_POSITIONS = [
  "feed",
  "story",
  "facebook_reels",
  "marketplace",
  "video_feeds",
  "search",
  "profile_feed",
] as const;
export const INSTAGRAM_POSITIONS = [
  "stream",
  "story",
  "reels",
  "explore",
  "explore_home",
  "profile_feed",
] as const;

export const RATIOS = ["1:1", "4:5", "9:16", "other"] as const;
export type Ratio = (typeof RATIOS)[number];

export const assetSchema = z.object({
  id: z.string().min(1),
  storageKey: z.string().regex(/^[0-9a-f-]{36}\.(jpg|jpeg|png|mp4|mov)$/),
  /** Display / creative name used in naming templates. */
  name: z.string().min(1).max(200),
  fileName: z.string().max(300),
  kind: z.enum(["image", "video"]),
  mime: z.string(),
  width: z.number().int().nonnegative(),
  height: z.number().int().nonnegative(),
  size: z.number().int().nonnegative(),
  ratio: z.enum(RATIOS),
  included: z.boolean(),
  overrides: z
    .object({
      primaryText: z.string().max(5000).optional(),
      headline: z.string().max(255).optional(),
      description: z.string().max(255).optional(),
      link: z.string().optional(),
    })
    .default({}),
});
export type Asset = z.infer<typeof assetSchema>;

export const launchConfigSchema = z.object({
  accountId: z.string().regex(/^act_\d+$/, "Pick an ad account"),
  currency: z.string().min(3).max(3),
  pageId: z.string().min(1, "Pick a Facebook Page"),
  instagramUserId: z.string().optional().default(""),
  launchDate: z.string().min(1),
  campaign: z.object({
    mode: z.enum(["new", "existing"]),
    existingId: z.string().optional().default(""),
    existingName: z.string().optional().default(""),
    existingHasCampaignBudget: z.boolean().optional().default(false),
    label: z.string().max(200).default(""),
    objective: z.enum(OBJECTIVES),
    budgetLevel: z.enum(["campaign", "adset"]),
  }),
  budget: z.object({
    type: z.enum(["daily", "lifetime"]),
    amount: z.number().positive("Budget must be above 0"),
  }),
  schedule: z.object({
    /** ISO 8601 with offset, or empty for "start now". */
    startTime: z.string().optional().default(""),
    endTime: z.string().optional().default(""),
  }),
  optimization: z.object({
    goal: z.enum(OPTIMIZATION_GOALS),
    pixelId: z.string().optional().default(""),
    event: z.enum(CONVERSION_EVENTS).default("PURCHASE"),
  }),
  targeting: z.object({
    countries: z.array(z.string().regex(/^[A-Z]{2}$/)).min(1, "Add at least one country"),
    ageMin: z.number().int().min(13).max(65),
    ageMax: z.number().int().min(13).max(65),
    genders: z.enum(["all", "male", "female"]),
    customAudienceIds: z.array(z.string()).default([]),
    excludedAudienceIds: z.array(z.string()).default([]),
    audienceLabel: z.string().max(200).default(""),
  }),
  placements: z.object({
    mode: z.enum(["advantage", "manual"]),
    facebook: z.array(z.enum(FACEBOOK_POSITIONS)).default([]),
    instagram: z.array(z.enum(INSTAGRAM_POSITIONS)).default([]),
  }),
  advantage: z.object({
    /** The strict "turn everything Advantage+ off" switch. */
    disableAll: z.boolean(),
  }),
  copy: z.object({
    primaryText: z.string().max(5000).default(""),
    headline: z.string().max(255).default(""),
    description: z.string().max(255).default(""),
    link: z.string().url("Enter a full website URL, starting with https://"),
    cta: z.enum(CTA_TYPES),
    urlTags: z.string().max(1000).default(""),
  }),
  structure: z.object({
    mode: z.enum(["single", "per_creative", "chunks"]),
    chunkSize: z.number().int().min(1).max(50),
  }),
  naming: z.object({
    campaign: z.string().min(1).max(400),
    adset: z.string().min(1).max(400),
    ad: z.string().min(1).max(400),
  }),
});
export type LaunchConfig = z.infer<typeof launchConfigSchema>;

export const launchRequestSchema = z.object({
  config: launchConfigSchema,
  assets: z.array(assetSchema).min(1).max(200),
  dryRun: z.boolean(),
});
export type LaunchRequest = z.infer<typeof launchRequestSchema>;
