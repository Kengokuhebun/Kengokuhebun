# Ritual Swipe launch — 2026-11-23

Request: "go ahead and activate" (following structure confirmed in `ads/ritual-swipe/prompts.md`).

## Live structure

- **Campaign**: `Glowling_R2_BF26_RitualSwipe_CBO` — id `120252790764970104` — ACTIVE
  - Objective OUTCOME_SALES, buying_type AUCTION, CBO daily budget £60.00 (6000), bid_strategy LOWEST_COST_WITHOUT_CAP
  - Pixel 1736160617626618, custom_event_type PURCHASE, optimization OFFSITE_CONVERSIONS, billing IMPRESSIONS, attribution 7-day click / 1-day view
  - Targeting: age 28-65+, no interest targeting, geo CA+US+AU+NZ combined (one geo list, not split per market), FB+IG feed/story/reels, mobile+desktop
  - Link on every ad: `https://x5a9bu-97.myshopify.com/products/glowling-led-drawing-board`, url_tags `utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{placement}}`

- **Ad set "Swipe8"** — id `120252790767220104` — ACTIVE — 8 ads (recreated Ritual Labs swipe set, our product/copy)
  - RS_01_selfie `120252790778870104`
  - RS_02_bin `120252790779160104`
  - RS_03_offerposter `120252790779890104`
  - RS_04_reframe `120252790780930104`
  - RS_05_checklist `120252790781600104`
  - RS_06_5pmipad `120252790783170104`
  - RS_07_by5pm `120252790784180104`
  - RS_08_hourglass `120252790784380104`

- **Ad set "Gradient4"** — id `120252790767540104` — ACTIVE — 4 ads (gradient text-post hooks, full dinner-ledger longform body reused, only paragraph 1 swapped per cell)
  - RS_G_A_control `120252790785690104`
  - RS_G_H1_number `120252790786500104`
  - RS_G_H2_item `120252790787180104`
  - RS_G_H3_result `120252790788060104`

All 12 confirmed `status: ACTIVE`, `effective_status: ACTIVE`, no `issues_info` (no disapprovals) as of this check.

## Everything else untouched

All 5 other campaigns on the account remain PAUSED: `Glowling_R1_BF26_VIDEO_TEST`, `Glowling_R1_BF26_UK_ABO`, `Glowling_R1_BF26_CBO`, `R1_Velmir`, `R1_Velmir – Copy`.

## Copy and creative source

Full ad-by-ad copy table (primary text, headline, description) is in `ads/ritual-swipe/prompts.md`. Images: `ads/ritual-swipe/final/` and `ads/ritual-swipe/generated/`.

## Notes / open items

- This is a new campaign (R2), separate from the paused R1 campaigns — lifetime spend ladder tracking for R1 (£444 at last check, step B £600, hard stop £800) does not cover this campaign; treat R2 spend separately until told otherwise.
- NZ pricing/shipping was set up and verified 2026-11-21 (`ads/launch/nz-market-setup-20261121.md`); NZ free-ship threshold and holiday cutoff date on the PDP are still placeholders copied from AU, not independently confirmed.
- Build note: hit Meta rate limit (code 17) twice during the build (after the 12 image uploads/creates, and again right after the first activation pass) — each time I waited and re-verified with a single read rather than retrying blind, which is why this confirms status explicitly rather than assuming the earlier activation POSTs succeeded.
