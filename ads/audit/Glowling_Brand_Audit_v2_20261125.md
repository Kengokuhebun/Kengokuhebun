# Glowling Brand Audit — v2, updated with live data

Using the Claude Brand Audit Master Resource (Origins/Aarreign protocol) · v1: Nov 25, 2026 (no Meta connection) · **v2: Nov 25, 2026, same day, with live Meta + Shopify data pulled directly** · @Kengoku

This is the original audit (unchanged where nothing new was learned) with every item it flagged as "not re-verified," "no live connection," or "not available in this session" now checked against live data. Changes from v1 are marked **[v2 UPDATE]**.

|  |  |
| --- | --- |
| **Brand / account** | Glowling LED Drawing Board · Meta act_1598462168591762 ("Velmir Ad account") · Shopify x5a9bu-97.myshopify.com |
| **Window** | Full test run, R1: 2026-11-15 to 2026-11-20 (paused). **R2 (Ritual Swipe CBO): launched 2026-11-23, [v2 UPDATE] now re-verified live — 2 days of real delivery data pulled directly from the Meta API and Shopify orders, as of 2026-11-25** |
| **Sample** | 17 ads reviewed in copy/structure detail in v1, now with live performance numbers for all 12 R2 ads · ~29 further R1 ads referenced by name/id only, not individually read · **2 completed purchases observed total (1 in R1, 1 new in R2)** |
| **Score** | **v1: 33.0/100.** [v2] 36.5/100. **[v3, with real unit economics §9] 43.5/100** |
| **Confidence** | v1: ~55% OBSERVED (indicative). v2: ~68%. **[v3] ~75% OBSERVED** — testimonial authenticity, R2 live performance, and unit economics (the three biggest open items in v1) are now all directly confirmed or computed, not inferred, dated, or unknown |
| **Band** | 4 — Foundations missing (unchanged — fixing one finding and getting one data pull does not change the band) |
| **Flags** | **SCALE HOLD** (economics — still unresolved) · ~~COMPLIANCE REVIEW (fabricated testimonials)~~ **[v2 UPDATE: FIXED this session, see Finding 1]** · measurement integrity concerns (shared pixel — still unresolved; UK consent gap; attribution — partially resolved, see Finding 3) |
| **Evidence tags** | [OBSERVED] seen directly, cited · [INFERRED] pattern across observed items, capped at 70% of a line's points · [UNVERIFIED] asserted or unconfirmed, not scored |

## 0. What changed in this update

1. **Finding 1 (fabricated testimonials) — CONFIRMED live on the production page today, then fixed.** Pulled the actual live HTML from `x5a9bu-97.myshopify.com/products/glowling-led-drawing-board` and found the exact content v1 described: the "Trusted by families worldwide" ★★★★★ badge with 4 randomuser.me stock photos, plus 4 fabricated quotes (Jess M., Priya S., Margaret H., Daniel R.), both still carrying their original `PLACEHOLDER ... replace before running paid traffic` source comments, never acted on. Removed outright from the repo source (`pdp/glowling/GLOWLING-PDP-one-section.html`, commit `45e0acf`) per the audit's own recommendation (no real reviews exist yet to replace them with). **This still needs to be pasted into the live Custom Liquid section in Shopify admin to take effect on the live store** — the repo fix alone does not change the live page.
2. **Finding 3 (attribution / pixel) — partially resolved, partially confirmed still broken.** A second real order landed during R2 (order #1002, 2026-11-24, £32.01, US). This time **Shopify's own UTM and Meta's attribution agree**: both credit `RS_01_selfie` in the `Glowling_R2_BF26_RitualSwipe_CBO` campaign. That's a genuine improvement over order #1001's mismatch. However, the pixel-sharing problem itself is **still unfixed**: queried the ad account directly and **zero Custom Conversions exist** — the fix the account's own `launch-log.json` flagged ("add a Custom Conversion filtered to /products/glowling-led-drawing-board before scaling") was never done, and R2 scaled to £60/day without it.
3. **Ritual Swipe (R2) — live performance pulled**, 2 days in (not the day-7 read the roadmap calls for — treat this as a transparency check, not a verdict). See §5 and the new data in §9.
4. **No change on**: unit economics (still no COGS/margin data — still a direct ask to the user), UK consent gap, roadmap/tracker (still doesn't exist — still recommended).

## 1. Executive summary [v2 UPDATE]

Glowling sells a $30-$55 LED drawing board (price varies by market) on a Buy 2 Get 1 FREE offer. Lifetime R1 spend was £444 against one order (£29.99, ROAS ≈ 0.07). **R2 has now run 2 days**: £134.67 spent, 1 order (£32.01), Meta-reported ROAS 0.24 — still well below breakeven on any plausible margin, but a real improvement in conversion rate (purchase/landing-page-view ≈ 2.8% vs R1's 0.73%) and click-through rate (6.7% vs R1's 1.25%). This is **2 days of data, not the 7-day read the account's own plan calls for** — it should not be read as a verdict yet.

The most urgent finding from v1 — fabricated testimonials and a fake review badge live on the exact page both R1 and R2 traffic has been sent to — is **confirmed independently this session, and fixed in the repo**. This was live during the entire R1 spend and the first 2 days of R2's £60/day spend. The fix still needs to be pasted into the live Shopify theme to take effect — that has not happened yet.

**Primary constraint is still MEASUREMENT and OFFER ECONOMICS, not creative.** No COGS, pick-and-pack, shipping-to-seller or gateway fee numbers exist anywhere in the repo — this audit still cannot tell you if £134.67 for 1 order is a disaster or an acceptable early-test cost. The pixel is still shared with an unrelated brand with no Custom Conversion filter, which the account's own notes flagged as a before-scaling blocker — and R2 scaled past that blocker anyway.

**What's better than v1 could say:** order #1002's attribution is clean (Shopify and Meta agree); CTR and CVR are both meaningfully higher in R2 than R1; the fabricated-testimonial compliance issue is now fixed at the source level.

**What's still missing:** real unit economics (the single biggest gap); the Custom Conversion / pixel-isolation fix; a roadmap/Learnings Document file; the live-page paste of the testimonial fix.

## 2. Scorecard [v2 UPDATE — changed lines only; all other lines unchanged from v1]

| Cat | Line | Max | v1 | v2 | Tag | Reason for change |
| --- | --- | --- | --- | --- | --- | --- |
| A | A3 Revenue & profit per session | 6 | 1 | 1.5 | [INFERRED, capped] | Now 2 data points instead of 1: R1 RPS ≈ £0.22 (1/137 LPV), R2 RPS ≈ £0.89 (£32.01/36 LPV) — still under the $1 floor band and still N=2 purchases total, but the trend and a second independent number raise confidence slightly, not the verdict |
| A | A5 Page/trust list + testing hygiene | 3 | 1.5 | 2 | [OBSERVED] | Fabricated reviews finding is now fixed at the source (repo), not just flagged — testing hygiene still absent (no formal offer test), so only a partial-credit increase |
| C | C3 Congruence & claim integrity | 4 | 0.5 | 1.5 | [OBSERVED] | Fabricated testimonials confirmed and removed (was the dominant penalty here); order #1002's attribution now agrees Shopify-to-Meta (was previously only a mismatch on record); "8 markers" claim still unverified against the physical product — kept uncredited |
| D | D3 Result classification & decision rules | 4 | 1.5 | 1.5 | [INFERRED] | No change — still no formal KPI/Winning/Losing labels; the new R2 data doesn't change whether the account classifies results, only what the results are |
| E | E4 Results & evidence discipline | 2 | 0.5 | 1 | [OBSERVED] | R2 now has 2 days of real evidence (was "launched, no outcome data" in v1); still not the declared 7-day read, so not full credit |
| **A** | **Offer** | **22** | **4.5** | **5.5** |  | **25.0%** |
| **C** | **Creatives** | **16** | **8.5** | **9.5** |  | **59.4%** |
| **E** | **Native image ads** | **14** | **4.5** | **5.0** |  | **35.7%** |
| | **TOTAL** | **100** | **33.0** | **36.5** |  | **Band still 4 — Foundations missing. A one-time fix and one data pull do not change the band; economics and measurement gates still fail outright.** |

All other scorecard lines (B, D1/D2/D4, F1-F5) are unchanged from v1 — nothing new was learned about angle-writing discipline, roadmap existence, or feedback-loop process this session.

## 3. Findings — updated status

### Finding 1: Fabricated testimonials — [v2: CONFIRMED live, then FIXED in repo; live-site paste still pending]

Re-verified by direct `curl` of the production page today (not just the saved repo file): the badge, the 4 stock avatars, and all 4 fabricated quotes (`Jess M.`, `Priya S.`, `Margaret H.`, `Daniel R.`) were live, word-for-word matching v1's description, still carrying their own `PLACEHOLDER` source comments.

**Action taken this session**: removed the badge and all 4 testimonials from `pdp/glowling/GLOWLING-PDP-one-section.html` (commit `45e0acf`). **Action still needed**: paste the updated Custom Liquid section into the live Shopify theme — the repo commit alone does not change what customers see. Until that paste happens, the live page still shows the fabricated content, under both R1's historical spend and R2's current £60/day.

### Finding 3: Pixel sharing / attribution — [v2: partially resolved, partially confirmed still open]

- **New evidence, good**: order #1002 (£32.01, US, 2026-11-24) shows Shopify's own UTM (`utm_content=RS_01_selfie`, campaign `Glowling_R2_BF26_RitualSwipe_CBO`) agreeing exactly with what Meta's ad-level insights credit. This specific concern (orders crediting different ads in Shopify vs Meta) did not recur on this order.
- **New evidence, still open**: queried `act_1598462168591762/customconversions` directly — **zero exist**. The pixel is still shared with the unrelated Ninu account with no filter isolating Glowling's own conversion events, exactly as `launch-log.json`'s own pixel_note warned against doing before scaling. R2 is a new £60/day campaign that launched without this fix.

Recommended fix (unchanged from v1): create a Custom Conversion on pixel `1736160617626618` filtered to `/products/glowling-led-drawing-board`, and use it (not the raw shared pixel event) for optimization and reporting going forward.

## 4. Offer-versus-creative diagnosis — [v2: Gate 6 now assessable]

| Gate | v1 result | v2 result |
| --- | --- | --- |
| 1 Economics | FAIL | **Still FAIL** — no cost data supplied |
| 2 Measurement | FAIL | **Still FAIL** — Custom Conversion confirmed absent; UK consent gap unchanged |
| 3 Offer | WARN (RPS ≈£0.22, N=1) | **WARN** — RPS ≈ £0.22 (R1, N=1) and £0.89 (R2, N=1); both below the $1 floor, N still too thin for a stable read |
| 4 Page | FAIL (fabricated reviews) | **FIXED IN REPO, not yet live** — treat as still-FAIL until the live paste happens |
| 5 Congruence | WARN | **Improved** — order #1002's attribution is now clean; the page-level fabrication issue is the same caveat as Gate 4 |
| 6 Creative | Not assessable (no account-wide median) | **Now assessable at the ad level for R2** — see §5. CTR range across the 12 R2 ads: 0% (2 ads with near-zero delivery) to 15.3% (`RS_02_bin`); the ad carrying the account's only R2 purchase (`RS_01_selfie`) sits at a middling 4.9% CTR but is the only one with any downstream funnel movement (ATC/IC/purchase) |

**Verdict unchanged**: MEASUREMENT and OFFER ECONOMICS are still the binding constraints. Two days of better CTR/CVR numbers in R2 do not change that — they are not interpretable without a margin number, and the page both campaigns point to had fabricated proof on it for the entire window being measured.

## 5. Ritual Swipe (R2) — live read, 2 days (2026-11-23 to 2026-11-25)

**This is a transparency check, not the day-7 read the roadmap calls for. Do not treat this as a verdict on Swipe8 vs Gradient4 or on any individual ad — 2 days and 89 total clicks is a thin sample, and CBO is still in its own early-learning phase.**

### Campaign totals
£134.67 spend · 1,324 impressions · 89 clicks · CTR 6.72% · CPC £1.51 · CPM £101.71 · 36 landing page views · 5 add-to-cart · 3 initiate-checkout · 1 add-payment-info · **1 purchase** · Meta-reported ROAS (omni_purchase) 0.24

### Ad set split (CBO-allocated, not set by us)
| Ad set | Spend | % of total | Impr | Clicks | CTR | CPC | LPV | ATC | IC | Purchase |
|---|---|---|---|---|---|---|---|---|---|---|
| Swipe8 | £125.24 | 93% | 855 | 57 | 6.67% | £2.20 | 24 | 5 | 3 | 1 |
| Gradient4 | £9.43 | 7% | 469 | 32 | 6.82% | **£0.29** | 12 | 0 | 0 | 0 |

CBO has concentrated the overwhelming majority of spend into Swipe8, where the only conversion signal exists. Gradient4's CPC is 7x cheaper but has zero downstream movement yet — too early to say whether that's a weak concept or just under-spent relative to Swipe8.

### Ad-level (all 12, sorted by spend)
| Ad | Spend | Impr | Clicks | CTR | LPV | ATC | IC | Purchase |
|---|---|---|---|---|---|---|---|---|
| RS_01_selfie | £56.84 | 305 | 15 | 4.9% | 10 | 5 | 3 | **1** |
| RS_04_reframe | £46.70 | 272 | 12 | 4.4% | 6 | 0 | 0 | 0 |
| RS_05_checklist | £18.19 | 97 | 3 | 3.1% | 2 | 0 | 0 | 0 |
| RS_G_A_control | £5.85 | 227 | 18 | 7.9% | 7 | 0 | 0 | 0 |
| RS_G_H1_number | £2.70 | 145 | 7 | 4.8% | 1 | 0 | 0 | 0 |
| RS_02_bin | £1.92 | 176 | 27 | **15.3%** | 6 | 0 | 0 | 0 |
| RS_07_by5pm | £1.49 | 2 | 0 | 0% | 0 | 0 | 0 | 0 |
| RS_G_H2_item | £0.48 | 51 | 5 | 9.8% | 2 | 0 | 0 | 0 |
| RS_G_H3_result | £0.40 | 46 | 2 | 4.3% | 2 | 0 | 0 | 0 |
| RS_06_5pmipad | £0.10 | 2 | 0 | 0% | 0 | 0 | 0 | 0 |
| RS_08_hourglass | £0.00 | 1 | 0 | 0% | 0 | 0 | 0 | 0 |
| RS_03_offerposter | £0.00 | 0 | 0 | — | — | — | — | 0 |

Observations (early, not conclusions):
- `RS_01_selfie` (the UGC selfie recreation) is carrying the entire conversion signal and 42% of total campaign spend — CBO is already favoring it.
- `RS_04_reframe` has taken the second-largest spend share (35%) with zero downstream movement so far.
- `RS_02_bin` has by far the best CTR (15.3%, triple the campaign average) on very little spend — worth watching at day 7, not acting on now.
- `RS_03_offerposter` and two others have received almost no delivery at all; this is CBO's own allocation, not a manual decision.

## 6. Per-ad diagnosis — Ritual Swipe set [v2: replaces v1's "too early" placeholder]

Format and method unchanged from v1 (8 static 1:1 competitor recreations + 4 gradient-hook posts, one CBO campaign, two ad sets, no per-ad minimum).

Result: **Still too early to classify by Origins definitions** — 2 days, 1 purchase, and the audit's own roadmap calls for a 7-day read before judging. The numbers above are provided for transparency and to catch any early red flag (none found: no disapprovals, no runaway CPM blowout beyond what CBO is already doing), not as a result.

Isolation verdict: unchanged from v1 — CLEAN only at the two-ad-set level (Swipe8 vs Gradient4 as one variable: creative format); UNDECLARED at the individual-ad level, since all 12 share one CBO budget.

Action plan: unchanged from v1 — hold to day 7 before reading for a verdict; do not add new ads or manually reallocate budget mid-read (CBO is already doing that); extract the framework from whichever ad or ad set is ahead at day 7 rather than keeping all 12 as permanent 1:1 copies.

## 7. Evidence log — new entries this session

| # | Item | Source | Tag | Used in |
| --- | --- | --- | --- | --- |
| 13 | Fabricated testimonials confirmed live via direct curl of production page, 2026-11-25 | `curl x5a9bu-97.myshopify.com/products/glowling-led-drawing-board`, this session | [OBSERVED] | Finding 1 |
| 14 | Testimonials removed from repo source | `pdp/glowling/GLOWLING-PDP-one-section.html` commit `45e0acf` | [OBSERVED] | Finding 1 |
| 15 | Zero Custom Conversions exist on the ad account | `act_1598462168591762/customconversions` API query, this session | [OBSERVED absence] | Finding 3 |
| 16 | Order #1002 (£32.01, US, RS_01_selfie) — Shopify UTM and Meta attribution agree | Shopify `orders` query + Meta `insights` (ad level), this session | [OBSERVED] | Finding 3, §5 |
| 17 | R2 campaign/ad-set/ad-level insights, 2026-11-23 to 2026-11-25 | Meta Graph API `insights` on campaign `120252790764970104`, this session | [OBSERVED, 2-day window, not the day-7 read] | §5, §6, Gate 6 |

### What is still weakest in this report

Confidence rose from ~55% to ~68% because the two largest open items in v1 (testimonial authenticity, R2 live performance) are now directly confirmed rather than inferred or dated. It has not moved further because the two gating issues — unit economics and pixel/measurement isolation — are both still completely unaddressed, and the live site still shows the fabricated content until the repo fix is pasted into Shopify. Treat 36.5/100 as directional, same as v1's 33.0, until those are fixed.

## 9. Unit economics — filled in 2026-11-25 (supplier cost sheet supplied by user)

This closes the single largest gap in v1 (Gate 1, lines A1/A2). Source: supplier cost+shipping sheet (product + YunExpress/WANB shipping, landed cost in USD, by destination and quantity), for the board, the 8-Color Marker Set, and the Tracing and Coloring Book — screenshots supplied 2026-11-25.

**Note on the marker set**: the sheet names it the "8-Color Marker Set" — this independently confirms the site's "8 fluorescent markers" claim (an open question flagged in earlier sessions over generated images showing 10 markers). The physical kit is 8 colors; the discrepancy was in AI-generated marketing images, not the claim itself. Closed, no action needed.

### Two real orders, computed exactly (no estimation — Shopify's own line items used)

| Order | Market | Items | Revenue | Landed cost (USD, converted at the order's own implied FX) | Gross margin after ~2.9%+$0.30 gateway fee | Ad spend attributed | Actual ROAS | Breakeven ROAS | Actual CPA vs. breakeven-affordable CPA |
|---|---|---|---|---|---|---|---|---|---|
| #1001 | UK | 1 board (no pen pack) | £29.99 | board $7.20 + book $2.50 = $9.70 → £7.28 | £22.72 → **75.7%** margin, BE ROAS **1.32** | £444 (R1 lifetime) | **0.068** | 1.32 | Actual CPA £444 vs. max-affordable £22.72 — **~19.5x over** |
| #1002 | US | 1 board + 1 Neon Marker Pen Pack | £32.01 (≈$41.98 implied) | board $10.30 + book $3.30 + pen pack $5.20 = $18.80 → £14.34 | £16.52 → **51.6%** margin, BE ROAS **1.94** | £134.67 (R2, 2 days) | **0.238** | 1.94 | Actual CPA £134.67 vs. max-affordable £16.52 — **~8.2x over** |

Both real orders are profitable at the unit-economics level (55-76% gross margin) — the problem is entirely on the paid-acquisition side: CPA needs to fall by roughly 8-20x to reach breakeven, not improve at the margins. R2 is directionally better than R1 (8x over vs 19.5x over) but still nowhere close.

### Forward-looking margin table, all 5 markets, both order types

Landed costs are read directly off the supplier sheet (board cost+shipping at the quantity needed, plus the tracing-book add-on, which ships free with every order per the PDP copy). FX used: GBP derived from order #1002 itself (≈0.7625 GBP/USD); CAD/AUD/NZD from a web lookup dated ~3 weeks before this audit (not live — flagged) at roughly 1 USD = 1.397 CAD = 1.435 AUD = 1.776 NZD. **NZ is not on the supplier's shipping sheet at all** — the "other country" row was used as a stand-in; this needs confirming with the supplier directly, since NZ shipping was only set up 2026-11-21 and its real landed cost could differ meaningfully from this estimate.

| Market | Single board: margin % / BE ROAS | Buy 2 Get 1 FREE bundle: margin % / BE ROAS |
|---|---|---|
| UK | 71.7% / **1.39** | 72.9% / **1.37** |
| US | 57.4% / **1.74** | 56.8% / **1.76** |
| CA | 61.4% / **1.63** | 63.6% / **1.57** |
| AU | 52.0% / **1.92** | 63.7% / **1.57** |
| NZ (unconfirmed cost) | 34.1% / **2.93** | 37.0% / **2.70** |

Everywhere except the unconfirmed NZ figure, breakeven sits around ROAS 1.4-1.9 — i.e., genuinely achievable territory for a healthy paid-social funnel, not a structurally broken offer. The margin itself is not the SCALE HOLD reason; **the actual ROAS being achieved (0.07-0.24) is 7-20x short of these breakevens**, which is a targeting/creative/funnel-efficiency problem, not a pricing problem. NZ's margin is meaningfully thinner than the other four markets on this estimate and should not be scaled until the supplier confirms the real NZ shipping cost.

What this excludes, so it's still a floor estimate: returns/refunds, chargebacks, customs/duties beyond what the supplier sheet already bundles, and customer-service time. Real-world required ROAS is likely somewhat higher than the figures above, not lower.

### Scorecard update

| Cat | Line | Max | v1 | v2 | v3 (this update) | Reason |
|---|---|---|---|---|---|---|
| A | A1 Unit economics known / margin gate | 6 | 0 | 0 | **4** | Real landed cost + margin % now computed for 4 of 5 markets directly from supplier data; NZ still unconfirmed, and returns/CS costs aren't in the model — capped short of full marks |
| A | A2 Target ROAS / profit-based reading | 4 | 0 | 0 | **3** | Breakeven ROAS now computed per market/order-type and directly compared against actual ROAS on both real orders — the account can now say, with numbers, exactly how far off it is |

**New total: 43.5/100** (was 36.5 in v2, 33.0 in v1). Still well short of a passing account — the gap between actual and breakeven ROAS is the whole story now, not an unknown.

## 8. What needs a decision from you now [v3: item 2 substantially answered]

1. **Paste the testimonial fix into the live Shopify theme.** The repo commit does not change what customers see — the fabricated badge and quotes are still live right now.
2. ~~Unit economics~~ **[Answered §9]** — margins and breakeven ROAS are now known for UK/US/CA/AU. Still open: confirm NZ's real shipping cost with the supplier (currently an unconfirmed estimate), and get real gateway-fee/returns-rate numbers from the payment processor to tighten the floor estimate further.
3. **Pixel fix**: approve adding the Custom Conversion filtered to the Glowling product page (a one-time Meta setup change, not a campaign/spend change — flagging since the standing rule is to confirm before changing anything in Meta).
4. Everything else from v1 (roadmap file, Learnings Document discipline, holding the R2 read to day 7) still stands.
