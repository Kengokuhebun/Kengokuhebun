"use client";
import { CheckCircle2, CircleDashed, XCircle } from "lucide-react";
import { Badge, Button, Callout, Card, Spinner } from "@/components/ui";
import { AppConfig, MeResponse, useApi } from "@/lib/client/api";

function Row({ ok, label, children }: { ok: boolean | null; label: string; children?: React.ReactNode }) {
  return (
    <div className="flex items-start gap-3 border-b py-3 last:border-0">
      {ok === null ? (
        <CircleDashed className="mt-0.5 h-4 w-4 text-muted-foreground" />
      ) : ok ? (
        <CheckCircle2 className="mt-0.5 h-4 w-4 text-success" />
      ) : (
        <XCircle className="mt-0.5 h-4 w-4 text-danger" />
      )}
      <div className="min-w-0 flex-1 text-sm">
        <div className="font-medium">{label}</div>
        {children ? <div className="mt-0.5 text-muted-foreground">{children}</div> : null}
      </div>
    </div>
  );
}

export default function SetupPage() {
  const cfg = useApi<AppConfig>("/api/config");
  const me = useApi<MeResponse>(cfg.data?.metaConfigured ? "/api/meta/me" : null);
  const c = cfg.data;

  return (
    <div className="mx-auto max-w-3xl space-y-5">
      <div>
        <h1 className="text-lg font-semibold">Setup</h1>
        <p className="text-sm text-muted-foreground">Connection status and the one-time steps to connect your Meta ad account.</p>
      </div>

      <Card className="px-5 py-2">
        <Row ok={c ? c.metaConfigured : null} label="Meta access token">
          {c?.metaConfigured ? "Found in the server environment. It is never sent to the browser." : "Not set. Follow the steps below."}
        </Row>
        <Row ok={c?.metaConfigured ? (me.error ? false : me.data ? true : null) : null} label="Token works">
          {me.loading ? (
            <span className="inline-flex items-center gap-2">
              <Spinner className="h-3 w-3" /> Checking with Meta
            </span>
          ) : me.error ? (
            <span className="text-danger">{me.error}</span>
          ) : me.data ? (
            <>
              Connected as <b className="text-foreground">{me.data.user.name ?? me.data.user.id}</b>. {me.data.accounts.length} ad account(s) available.
            </>
          ) : (
            "Waiting for a token."
          )}
          {c?.metaConfigured ? (
            <div className="mt-2">
              <Button size="sm" variant="outline" onClick={me.reload} disabled={me.loading}>
                Test again
              </Button>
            </div>
          ) : null}
        </Row>
        <Row ok={c ? true : null} label="Graph API version">
          {c?.apiVersion} <span className="text-xs">(change with META_API_VERSION)</span>
        </Row>
        <Row ok={c ? true : null} label="Media storage">
          {c?.storage === "supabase" ? (
            <>
              Supabase Storage, bucket <code>{c.bucket}</code>.
            </>
          ) : (
            <>
              Local folder on this computer (<code>.data/uploads</code>). Fine for running locally. Add Supabase keys to host it online.
            </>
          )}
        </Row>
        <Row ok={c ? true : null} label="appsecret_proof">
          {c?.appSecretProof ? "On (META_APP_SECRET is set)." : "Off. Optional: set META_APP_SECRET for extra protection."}
        </Row>
      </Card>

      <Card className="p-5">
        <h2 className="font-semibold">Connect Meta (one time, about 10 minutes)</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          This uses a <b>System User token</b> from your Business Manager. It does not expire like a login token does and needs no Meta App Review, because the tool only manages your own ad
          accounts.
        </p>
        <ol className="mt-4 list-decimal space-y-3 pl-5 text-sm leading-relaxed">
          <li>
            Go to <b>developers.facebook.com</b>, then My Apps, then Create App. Choose the <b>Business</b> type (or &quot;Other&quot; then Business), and connect it to your Business portfolio.
            Add the <b>Marketing API</b> product.
          </li>
          <li>
            In the app&apos;s basic settings, add a privacy policy URL (your store&apos;s policy page works) and switch the app to <b>Live</b>. Meta rejects ad creatives made by an app in
            development mode.
          </li>
          <li>
            Open <b>business.facebook.com/settings</b>, then Users, then <b>System users</b>. Add one with the <b>Admin</b> role.
          </li>
          <li>
            Click <b>Assign assets</b> on that system user and give it full control of: your <b>ad account</b>, your <b>Facebook Page</b>, and your <b>pixel / dataset</b>. Also add the app
            under Apps.
          </li>
          <li>
            Click <b>Generate new token</b>, choose your app, set expiry to <b>Never</b>, and tick: <code>ads_management</code>, <code>ads_read</code>, <code>business_management</code>,{" "}
            <code>pages_show_list</code>, <code>pages_read_engagement</code>, <code>pages_manage_ads</code>. Copy the token.
          </li>
          <li>
            In the <code>ads-launcher</code> folder, copy <code>.env.example</code> to <code>.env.local</code> and paste the token after <code>META_ACCESS_TOKEN=</code>. Optional: paste the
            app secret (App settings, Basic) after <code>META_APP_SECRET=</code>.
          </li>
          <li>
            Restart the app (<code>npm run dev</code>), reload this page and check that &quot;Token works&quot; is green.
          </li>
        </ol>
        <Callout tone="amber" className="mt-4" title="Keep the token secret">
          It can create and edit ads on your account. Never paste it into a chat, a screenshot or a file you commit. <code>.env.local</code> is already ignored by git.
        </Callout>
      </Card>

      <Card className="p-5">
        <h2 className="font-semibold">If you host it online</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Running on your own computer needs nothing else. To run it on Vercel or similar, set <code>APP_PASSWORD</code> so the site asks for a password, and add Supabase so creatives are
          stored in the cloud. Steps are in the README.
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          <Badge>APP_PASSWORD</Badge>
          <Badge>NEXT_PUBLIC_SUPABASE_URL</Badge>
          <Badge>NEXT_PUBLIC_SUPABASE_ANON_KEY</Badge>
          <Badge>SUPABASE_SERVICE_ROLE_KEY</Badge>
        </div>
      </Card>
    </div>
  );
}
