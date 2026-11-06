import "server-only";
import { NextResponse } from "next/server";
import { GraphClient, MetaApiError } from "../meta/graph";
import { env } from "./env";

export class ConfigError extends Error {}

export function getGraph(): GraphClient {
  if (!env.metaToken) {
    throw new ConfigError("META_ACCESS_TOKEN is not set. Add it to .env.local and restart the app (see README).");
  }
  return new GraphClient({
    token: env.metaToken,
    version: env.metaApiVersion,
    base: env.metaGraphBase,
    appSecret: env.metaAppSecret || undefined,
  });
}

export function errorResponse(err: unknown, status = 500) {
  if (err instanceof ConfigError) return NextResponse.json({ error: err.message, config: true }, { status: 400 });
  if (err instanceof MetaApiError) {
    return NextResponse.json({ error: err.describe(), code: err.code }, { status: err.status >= 400 ? err.status : 502 });
  }
  return NextResponse.json({ error: err instanceof Error ? err.message : String(err) }, { status });
}
