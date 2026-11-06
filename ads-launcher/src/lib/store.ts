"use client";
import { useEffect, useState } from "react";
import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { defaultConfig, todayISO } from "./launch/defaults";
import type { Asset, LaunchConfig } from "./launch/schema";

export interface AccountInfo {
  id: string;
  name: string;
  currency: string;
  timezone: string;
}

export interface Preset {
  name: string;
  savedAt: string;
  config: LaunchConfig;
}

interface State {
  account: AccountInfo | null;
  config: LaunchConfig;
  assets: Asset[];
  presets: Preset[];
  setAccount: (a: AccountInfo | null) => void;
  update: (fn: (draft: LaunchConfig) => void) => void;
  resetConfig: () => void;
  addAsset: (a: Asset) => void;
  updateAsset: (id: string, patch: Partial<Asset>) => void;
  removeAsset: (id: string) => void;
  clearAssets: () => void;
  setAllIncluded: (v: boolean) => void;
  savePreset: (name: string) => void;
  loadPreset: (name: string) => void;
  deletePreset: (name: string) => void;
}

function clearAccountBound(c: LaunchConfig) {
  c.pageId = "";
  c.instagramUserId = "";
  c.optimization.pixelId = "";
  c.targeting.customAudienceIds = [];
  c.targeting.excludedAudienceIds = [];
  c.campaign.mode = "new";
  c.campaign.existingId = "";
  c.campaign.existingName = "";
  c.campaign.existingHasCampaignBudget = false;
}

export const useStore = create<State>()(
  persist(
    (set, get) => ({
      account: null,
      config: defaultConfig(),
      assets: [],
      presets: [],
      setAccount: (a) =>
        set((s) => {
          const config = structuredClone(s.config);
          if (s.account?.id !== a?.id) clearAccountBound(config);
          config.accountId = a?.id ?? "";
          config.currency = a?.currency ?? "USD";
          return { account: a, config };
        }),
      update: (fn) =>
        set((s) => {
          const draft = structuredClone(s.config);
          fn(draft);
          return { config: draft };
        }),
      resetConfig: () =>
        set((s) => {
          const c = defaultConfig();
          c.accountId = s.account?.id ?? "";
          c.currency = s.account?.currency ?? "USD";
          return { config: c };
        }),
      addAsset: (a) => set((s) => ({ assets: [...s.assets, a] })),
      updateAsset: (id, patch) => set((s) => ({ assets: s.assets.map((a) => (a.id === id ? { ...a, ...patch } : a)) })),
      removeAsset: (id) => set((s) => ({ assets: s.assets.filter((a) => a.id !== id) })),
      clearAssets: () => set({ assets: [] }),
      setAllIncluded: (v) => set((s) => ({ assets: s.assets.map((a) => ({ ...a, included: v })) })),
      savePreset: (name) =>
        set((s) => ({
          presets: [
            { name, savedAt: new Date().toISOString(), config: structuredClone(s.config) },
            ...s.presets.filter((p) => p.name !== name),
          ],
        })),
      loadPreset: (name) => {
        const p = get().presets.find((x) => x.name === name);
        if (!p) return;
        const s = get();
        const c = { ...defaultConfig(), ...structuredClone(p.config) };
        c.launchDate = todayISO();
        if (s.account && c.accountId !== s.account.id) {
          clearAccountBound(c);
          c.accountId = s.account.id;
          c.currency = s.account.currency;
        }
        set({ config: c });
      },
      deletePreset: (name) => set((s) => ({ presets: s.presets.filter((p) => p.name !== name) })),
    }),
    {
      name: "ads-launcher-v1",
      version: 1,
      storage: createJSONStorage(() => localStorage),
      skipHydration: true,
      // Always start a new day with today's date for {date}.
      merge: (persisted, current) => {
        const p = (persisted ?? {}) as Partial<State>;
        const config = { ...current.config, ...(p.config ?? {}), launchDate: todayISO() };
        return { ...current, ...p, config };
      },
    },
  ),
);

/** Rehydrate from localStorage on the client and report when done. */
export function useHydrated(): boolean {
  const [done, setDone] = useState(false);
  useEffect(() => {
    if (useStore.persist.hasHydrated()) {
      setDone(true);
      return;
    }
    const unsub = useStore.persist.onFinishHydration(() => setDone(true));
    void useStore.persist.rehydrate();
    return unsub;
  }, []);
  return done;
}
