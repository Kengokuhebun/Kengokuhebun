import "server-only";
import path from "node:path";

/** Server-only configuration. Secrets never leave this module's callers. */
export const env = {
  metaToken: process.env.META_ACCESS_TOKEN?.trim() || "",
  metaAppSecret: process.env.META_APP_SECRET?.trim() || "",
  metaApiVersion: process.env.META_API_VERSION?.trim() || "v25.0",
  metaGraphBase: (process.env.META_GRAPH_BASE?.trim() || "https://graph.facebook.com").replace(/\/$/, ""),
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL?.trim() || "",
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY?.trim() || "",
  supabaseServiceKey: process.env.SUPABASE_SERVICE_ROLE_KEY?.trim() || "",
  supabaseBucket: process.env.SUPABASE_BUCKET?.trim() || "creatives",
  dataDir: path.resolve(process.env.DATA_DIR?.trim() || ".data"),
};

export const supabaseEnabled = () =>
  Boolean(env.supabaseUrl && env.supabaseAnonKey && env.supabaseServiceKey);
