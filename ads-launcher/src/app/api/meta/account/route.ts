import { NextRequest, NextResponse } from "next/server";
import { MetaApiError } from "@/lib/meta/graph";
import { errorResponse, getGraph } from "@/lib/server/meta";

export const dynamic = "force-dynamic";

interface Page {
  id: string;
  name: string;
  instagram_business_account?: { id: string; username?: string };
}

function why(r: PromiseSettledResult<unknown>): string | null {
  if (r.status === "fulfilled") return null;
  return r.reason instanceof MetaApiError ? r.reason.describe() : String((r.reason as Error)?.message ?? r.reason);
}

/** Pages, Instagram accounts, pixels, audiences and campaigns for one ad account. */
export async function GET(req: NextRequest) {
  const id = req.nextUrl.searchParams.get("id") ?? "";
  if (!/^act_\d+$/.test(id)) return NextResponse.json({ error: "Invalid ad account id" }, { status: 400 });
  try {
    const graph = getGraph();
    const pageFields = "id,name,instagram_business_account{id,username}";
    const [promote, mine, pixels, audiences, campaigns] = await Promise.allSettled([
      graph.getAll<Page>(`/${id}/promote_pages`, { fields: pageFields }),
      graph.getAll<Page>("/me/accounts", { fields: pageFields }),
      graph.getAll<{ id: string; name: string; last_fired_time?: string }>(`/${id}/adspixels`, {
        fields: "id,name,last_fired_time",
      }),
      graph.getAll<{ id: string; name: string; subtype?: string; approximate_count_lower_bound?: number }>(
        `/${id}/customaudiences`,
        { fields: "id,name,subtype,approximate_count_lower_bound" },
      ),
      graph.getAll<{
        id: string;
        name: string;
        objective: string;
        effective_status: string;
        daily_budget?: string;
        lifetime_budget?: string;
      }>(`/${id}/campaigns`, {
        fields: "id,name,objective,effective_status,daily_budget,lifetime_budget",
        effective_status: ["ACTIVE", "PAUSED", "IN_PROCESS", "WITH_ISSUES"],
      }),
    ]);

    const pages = new Map<string, Page>();
    for (const r of [promote, mine]) if (r.status === "fulfilled") for (const p of r.value) pages.set(p.id, p);

    const warnings = [
      why(promote) && why(mine) ? `Pages: ${why(promote)}` : null,
      why(pixels) && `Pixels: ${why(pixels)}`,
      why(audiences) && `Audiences: ${why(audiences)}`,
      why(campaigns) && `Campaigns: ${why(campaigns)}`,
    ].filter(Boolean);

    return NextResponse.json({
      pages: [...pages.values()].map((p) => ({
        id: p.id,
        name: p.name,
        instagram: p.instagram_business_account
          ? { id: p.instagram_business_account.id, username: p.instagram_business_account.username ?? "" }
          : null,
      })),
      pixels: pixels.status === "fulfilled" ? pixels.value : [],
      audiences:
        audiences.status === "fulfilled"
          ? audiences.value.map((a) => ({
              id: a.id,
              name: a.name,
              subtype: a.subtype ?? "",
              size: a.approximate_count_lower_bound ?? null,
            }))
          : [],
      campaigns:
        campaigns.status === "fulfilled"
          ? campaigns.value.map((c) => ({
              id: c.id,
              name: c.name,
              objective: c.objective,
              status: c.effective_status,
              hasCampaignBudget: Boolean(Number(c.daily_budget) || Number(c.lifetime_budget)),
            }))
          : [],
      warnings,
    });
  } catch (err) {
    return errorResponse(err);
  }
}
