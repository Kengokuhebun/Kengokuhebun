/**
 * Advantage+ override.
 *
 * Source: Meta Marketing API "Advantage+ creative / get started" page, read
 * 2026-11-06. Each creative feature is opted out individually with
 *   degrees_of_freedom_spec.creative_features_spec.<key>.enroll_status = "OPT_OUT".
 * The old single "standard_enhancements" bundle was deprecated in v22.0, so we
 * do NOT rely on it.
 *
 * Meta adds and retires keys between API versions. If Meta rejects a key, the
 * executor drops just that key, retries, and reports it, then reads the
 * creative back and flags anything that came back OPT_IN.
 */

export const CREATIVE_FEATURE_KEYS = [
  "adapt_to_placement",
  "add_text_overlay",
  "creative_stickers",
  "description_automation",
  "enhance_cta",
  "image_animation",
  "image_background_gen",
  "image_brightness_and_contrast",
  "image_templates",
  "image_text_translation",
  "image_touchups",
  "image_uncrop",
  "inline_comment",
  "media_type_automation",
  "pac_relaxation",
  "product_extensions",
  "reveal_details_over_time",
  "text_optimizations",
  "text_translation",
  "translate_voiceover",
  "video_auto_crop",
  "video_filtering",
  "video_uncrop",
] as const;

/** Plain-English labels for the UI. */
export const FEATURE_LABELS: Record<string, string> = {
  adapt_to_placement: "Adapt to placement (auto-crop/resize per placement)",
  add_text_overlay: "Add text overlays",
  creative_stickers: "Creative stickers",
  description_automation: "Auto descriptions",
  enhance_cta: "Enhance CTA",
  image_animation: "Image animation (AI)",
  image_background_gen: "AI background generation",
  image_brightness_and_contrast: "Brightness and contrast",
  image_templates: "Image templates / frames (AI)",
  image_text_translation: "Translate text in images",
  image_touchups: "Visual touch-ups",
  image_uncrop: "Image expansion / uncrop (AI)",
  inline_comment: "Relevant comments",
  media_type_automation: "Turn images into video",
  pac_relaxation: "Placement asset relaxation",
  product_extensions: "Product extensions (catalog items)",
  reveal_details_over_time: "Reveal details over time",
  text_optimizations: "Text improvements / multiple text variations",
  text_translation: "Translate text",
  translate_voiceover: "Translate voiceover",
  video_auto_crop: "Video auto-crop",
  video_filtering: "Video filters",
  video_uncrop: "Video expansion (AI)",
  contextual_multi_ads: "Multi-advertiser ads",
  advantage_audience: "Advantage+ audience (ad set)",
  music: "Auto-added music",
};

export function buildCreativeAdvantageFields(
  disableAll: boolean,
  rejectedKeys: ReadonlySet<string> = new Set(),
): Record<string, unknown> {
  if (!disableAll) return {};
  const creative_features_spec: Record<string, { enroll_status: "OPT_OUT" }> = {};
  for (const key of CREATIVE_FEATURE_KEYS) {
    if (!rejectedKeys.has(key)) creative_features_spec[key] = { enroll_status: "OPT_OUT" };
  }
  const fields: Record<string, unknown> = {
    degrees_of_freedom_spec: { creative_features_spec },
  };
  if (!rejectedKeys.has("contextual_multi_ads")) {
    fields.contextual_multi_ads = { enroll_status: "OPT_OUT" };
  }
  return fields;
}

/**
 * If a Meta error message names one of our keys, return it so the caller can
 * drop it and retry. Returns null if the error is about something else.
 */
export function findRejectedFeatureKey(
  errorText: string,
  alreadyRejected: ReadonlySet<string>,
): string | null {
  const text = errorText.toLowerCase();
  // Longest first so "image_uncrop" is not matched inside a longer key.
  const candidates = [...CREATIVE_FEATURE_KEYS, "contextual_multi_ads"]
    .filter((k) => !alreadyRejected.has(k))
    .sort((a, b) => b.length - a.length);
  for (const key of candidates) {
    if (text.includes(key)) return key;
  }
  // Common singular/plural mismatch noted in Meta's own docs.
  if (text.includes("image_template") && !alreadyRejected.has("image_templates")) {
    return "image_templates";
  }
  if (text.includes("degrees_of_freedom_spec") || text.includes("creative_features_spec")) {
    return "__unknown_feature__";
  }
  return null;
}

type FeatureSpec = Record<string, { enroll_status?: string } | undefined>;

/**
 * Read-back check. Given the creative as Meta returns it, list every
 * enhancement that is switched on.
 */
export function findEnabledEnhancements(creative: {
  degrees_of_freedom_spec?: { creative_features_spec?: FeatureSpec };
  contextual_multi_ads?: { enroll_status?: string };
}): string[] {
  const on: string[] = [];
  const spec = creative.degrees_of_freedom_spec?.creative_features_spec ?? {};
  for (const [key, value] of Object.entries(spec)) {
    // standard_enhancements may still be echoed back; Meta says it is not
    // applied unless OPT_IN, so we check it like any other key.
    if (value?.enroll_status === "OPT_IN") on.push(key);
  }
  if (creative.contextual_multi_ads?.enroll_status === "OPT_IN") on.push("contextual_multi_ads");
  return on;
}
