"use client";
import Link from "next/link";
import { useMemo } from "react";
import { MediaSection } from "@/components/launch/media-section";
import { LaunchPanel, PlanPreview, usePlan } from "@/components/launch/review";
import {
  AdvantageSection,
  AudienceSection,
  CampaignSection,
  CopySection,
  IdentitySection,
  OptimizationSection,
  StructureSection,
} from "@/components/launch/settings-sections";
import { Callout } from "@/components/ui";
import { AccountData, AppConfig, useApi } from "@/lib/client/api";
import { validateLaunch } from "@/lib/launch/plan";
import { useStore } from "@/lib/store";

export default function LaunchPage() {
  const appConfig = useApi<AppConfig>("/api/config");
  const account = useStore((s) => s.account);
  const config = useStore((s) => s.config);
  const assets = useStore((s) => s.assets);
  const accountData = useApi<AccountData>(account ? `/api/meta/account?id=${account.id}` : null);
  const plan = usePlan();
  const validation = useMemo(() => validateLaunch(config, assets), [config, assets]);

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
      <div className="min-w-0 space-y-5">
        {appConfig.data && !appConfig.data.metaConfigured ? (
          <Callout tone="amber" title="Meta is not connected yet">
            Add your access token in <code>.env.local</code>, then restart. <Link href="/setup" className="underline">Open Setup</Link> for the steps. You can still upload creatives and do dry runs.
          </Callout>
        ) : null}
        {appConfig.data?.metaConfigured && !account ? (
          <Callout tone="blue" title="Choose an ad account">
            Pick the ad account at the top right to load your Pages, pixels, audiences and campaigns.
          </Callout>
        ) : null}
        {accountData.error ? (
          <Callout tone="red" title="Could not load the ad account">
            {accountData.error}
          </Callout>
        ) : null}

        <MediaSection appConfig={appConfig.data} />
        <IdentitySection data={accountData.data} loading={accountData.loading} />
        <CampaignSection data={accountData.data} />
        <AudienceSection data={accountData.data} />
        <OptimizationSection data={accountData.data} />
        <CopySection />
        <AdvantageSection />
        <StructureSection />
        <PlanPreview plan={plan} />
      </div>
      <aside className="lg:sticky lg:top-20 lg:self-start">
        <LaunchPanel plan={plan} validation={validation} />
      </aside>
    </div>
  );
}
