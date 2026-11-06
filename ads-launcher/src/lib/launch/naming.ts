/**
 * Dynamic naming. Templates accept tokens in either {curly} or [Square]
 * form, case-insensitive, e.g. "[Date] - {audience} - {creative}".
 * Unknown tokens are left exactly as typed so a typo is visible in the preview.
 */

export const NAMING_TOKENS = [
  { token: "date", help: "Launch date, e.g. 2026-11-07" },
  { token: "campaign", help: "Campaign label (or existing campaign name)" },
  { token: "objective", help: "Sales, Traffic, Leads or Awareness" },
  { token: "audience", help: "Audience label" },
  { token: "country", help: "Countries, e.g. US+CA" },
  { token: "adset", help: "Ad set group: creative name or Set 1, Set 2" },
  { token: "creative", help: "Creative name (file name without extension)" },
  { token: "ratio", help: "1x1, 4x5, 9x16" },
  { token: "type", help: "IMG or VID" },
  { token: "n", help: "Running number within the launch, 01, 02" },
] as const;

export type NamingContext = Partial<Record<(typeof NAMING_TOKENS)[number]["token"], string>>;

const TOKEN_RE = /\{([a-z]+)\}|\[([a-z]+)\]/gi;

export function renderName(template: string, ctx: NamingContext): string {
  const out = template.replace(TOKEN_RE, (match, a?: string, b?: string) => {
    const key = (a ?? b ?? "").toLowerCase() as keyof NamingContext;
    const value = ctx[key];
    return value === undefined ? match : value;
  });
  // Collapse whitespace and dangling separators caused by empty tokens.
  return out
    .replace(/\s+/g, " ")
    .replace(/(\s*[-|_]\s*){2,}/g, (m) => (m.includes("|") ? " | " : m.includes("_") ? "_" : " - "))
    .replace(/^\s*[-|_]\s*|\s*[-|_]\s*$/g, "")
    .trim()
    .slice(0, 400);
}

export function objectiveLabel(objective: string): string {
  return (
    {
      OUTCOME_SALES: "Sales",
      OUTCOME_TRAFFIC: "Traffic",
      OUTCOME_LEADS: "Leads",
      OUTCOME_AWARENESS: "Awareness",
    } as Record<string, string>
  )[objective] ?? objective;
}

export function ratioToken(ratio: string): string {
  return ratio === "other" ? "custom" : ratio.replace(":", "x");
}

export function stripExtension(fileName: string): string {
  return fileName.replace(/\.[a-z0-9]+$/i, "");
}

export function pad(n: number, width = 2): string {
  return String(n).padStart(width, "0");
}
