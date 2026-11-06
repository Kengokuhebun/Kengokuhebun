"use client";
import { History, Rocket, Settings2 } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { AppConfig, MeResponse, useApi } from "@/lib/client/api";
import { useHydrated, useStore } from "@/lib/store";
import { Badge, cn, Select, Spinner } from "./ui";

const NAV = [
  { href: "/", label: "Launch", icon: Rocket },
  { href: "/history", label: "History", icon: History },
  { href: "/setup", label: "Setup", icon: Settings2 },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const hydrated = useHydrated();
  return (
    <div className="flex min-h-screen">
      <aside className="sticky top-0 hidden h-screen w-56 shrink-0 flex-col border-r bg-card md:flex">
        <div className="flex h-14 items-center gap-2 border-b px-4">
          <span className="flex h-7 w-7 items-center justify-center rounded-md bg-foreground text-background">
            <Rocket className="h-4 w-4" />
          </span>
          <span className="font-semibold tracking-tight">Ads Launcher</span>
        </div>
        <nav className="flex flex-col gap-0.5 p-2">
          {NAV.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground",
                pathname === href && "bg-muted text-foreground",
              )}
            >
              <Icon className="h-4 w-4" />
              {label}
            </Link>
          ))}
        </nav>
        <div className="mt-auto border-t p-4 text-xs leading-relaxed text-muted-foreground">
          Personal tool. Every campaign, ad set and ad is created <b className="text-foreground">paused</b>.
        </div>
      </aside>
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="sticky top-0 z-20 flex h-14 items-center justify-between gap-3 border-b bg-card/90 px-4 backdrop-blur md:px-6">
          <div className="flex items-center gap-1 md:hidden">
            {NAV.map(({ href, label, icon: Icon }) => (
              <Link key={href} href={href} className={cn("rounded-md p-2 text-muted-foreground", pathname === href && "bg-muted text-foreground")} aria-label={label}>
                <Icon className="h-4 w-4" />
              </Link>
            ))}
          </div>
          <div className="hidden text-sm font-medium md:block">{NAV.find((n) => n.href === pathname)?.label ?? ""}</div>
          {hydrated ? <AccountSwitcher /> : <div className="h-9 w-64 animate-pulse rounded-md bg-muted" />}
        </header>
        <main className="mx-auto w-full max-w-[1400px] flex-1 p-4 md:p-6">
          {hydrated ? (
            children
          ) : (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Spinner /> Loading
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

function AccountSwitcher() {
  const cfg = useApi<AppConfig>("/api/config");
  const me = useApi<MeResponse>(cfg.data?.metaConfigured ? "/api/meta/me" : null);
  const account = useStore((s) => s.account);
  const setAccount = useStore((s) => s.setAccount);

  if (cfg.data && !cfg.data.metaConfigured) {
    return (
      <Link href="/setup">
        <Badge tone="amber" className="px-3 py-1 text-xs">
          Meta not connected. Open Setup
        </Badge>
      </Link>
    );
  }
  if (me.error) {
    return (
      <Link href="/setup" title={me.error}>
        <Badge tone="red" className="px-3 py-1 text-xs">
          Meta token problem. Open Setup
        </Badge>
      </Link>
    );
  }
  const accounts = me.data?.accounts ?? [];
  return (
    <div className="flex items-center gap-2">
      <span className="hidden text-xs text-muted-foreground sm:inline">Ad account</span>
      <Select
        aria-label="Ad account"
        className="w-72 max-w-[60vw]"
        value={account?.id ?? ""}
        disabled={me.loading || !accounts.length}
        onChange={(e) => {
          const a = accounts.find((x) => x.id === e.target.value);
          setAccount(a ? { id: a.id, name: a.name, currency: a.currency, timezone: a.timezone } : null);
        }}
      >
        <option value="">{me.loading ? "Loading accounts" : accounts.length ? "Choose an ad account" : "No ad accounts found"}</option>
        {accounts.map((a) => (
          <option key={a.id} value={a.id}>
            {a.name} · {a.currency} · {a.id.replace("act_", "")}
            {a.active ? "" : ` (${a.status})`}
          </option>
        ))}
        {account && !accounts.some((a) => a.id === account.id) && !me.loading ? (
          <option value={account.id}>{account.name} (saved)</option>
        ) : null}
      </Select>
    </div>
  );
}
