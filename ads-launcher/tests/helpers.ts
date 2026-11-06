import { defaultConfig } from "@/lib/launch/defaults";
import type { Asset, LaunchConfig } from "@/lib/launch/schema";

export function makeAsset(i: number, over: Partial<Asset> = {}): Asset {
  return {
    id: `a${i}`,
    storageKey: `00000000-0000-0000-0000-00000000000${i}.${over.kind === "video" ? "mp4" : "jpg"}`,
    name: `Creative ${i}`,
    fileName: `creative-${i}.jpg`,
    kind: "image",
    mime: "image/jpeg",
    width: 1080,
    height: 1080,
    size: 1000,
    ratio: "1:1",
    included: true,
    overrides: {},
    ...over,
  };
}

export function makeConfig(over: (c: LaunchConfig) => void = () => {}): LaunchConfig {
  const c = defaultConfig();
  c.accountId = "act_123";
  c.currency = "GBP";
  c.pageId = "p1";
  c.launchDate = "2026-11-07";
  c.optimization.pixelId = "px1";
  c.copy.link = "https://tryninu.store/products/kit";
  c.copy.primaryText = "Body";
  c.copy.headline = "Headline";
  c.campaign.label = "Ninu R17";
  over(c);
  return c;
}

