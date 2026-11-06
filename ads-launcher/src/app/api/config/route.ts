import { NextResponse } from "next/server";
import { env, supabaseEnabled } from "@/lib/server/env";

export const dynamic = "force-dynamic";

/** Public, non-secret configuration for the browser. */
export async function GET() {
  return NextResponse.json({
    metaConfigured: Boolean(env.metaToken),
    appSecretProof: Boolean(env.metaAppSecret),
    apiVersion: env.metaApiVersion,
    storage: supabaseEnabled() ? "supabase" : "local",
    supabaseUrl: supabaseEnabled() ? env.supabaseUrl : "",
    supabaseAnonKey: supabaseEnabled() ? env.supabaseAnonKey : "",
    bucket: env.supabaseBucket,
  });
}
