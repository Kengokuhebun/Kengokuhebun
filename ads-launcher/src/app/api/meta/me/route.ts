import { NextResponse } from "next/server";
import { errorResponse, getGraph } from "@/lib/server/meta";

export const dynamic = "force-dynamic";

const ACCOUNT_STATUS: Record<number, string> = {
  1: "Active",
  2: "Disabled",
  3: "Unsettled",
  7: "Pending risk review",
  8: "Pending settlement",
  9: "In grace period",
  100: "Pending closure",
  101: "Closed",
  201: "Any active",
  202: "Any closed",
};

/** Checks the token and lists the ad accounts it can manage. */
export async function GET() {
  try {
    const graph = getGraph();
    const me = await graph.get<{ id: string; name?: string }>("/me", { fields: "id,name" });
    const accounts = await graph.getAll<{
      id: string;
      name: string;
      account_status: number;
      currency: string;
      timezone_name: string;
      business?: { name?: string };
    }>("/me/adaccounts", { fields: "id,name,account_status,currency,timezone_name,business{name}" });
    return NextResponse.json({
      user: me,
      accounts: accounts.map((a) => ({
        id: a.id,
        name: a.name,
        currency: a.currency,
        timezone: a.timezone_name,
        business: a.business?.name ?? "",
        status: ACCOUNT_STATUS[a.account_status] ?? String(a.account_status),
        active: a.account_status === 1,
      })),
    });
  } catch (err) {
    return errorResponse(err);
  }
}
