# Ninu — Kill criteria (draft, pending mentor's metric doc)

Everything below is ready to use now. The one open slot is your mentor's specific
thresholds — swap them in wherever this says "placeholder" and the rest doesn't change.

**Account currency: GBP.** All USD figures below are converted at an approximate
1 GBP ≈ $1.30 USD. This is a rough rate, not a live quote — close enough for kill
thresholds, not precise enough for anything accounting-related.

---

## 1. Break-even CAC (the number everything else hangs off)

**Kit price:** $49.99
**Landed COGS (dispenser + bonnet + 60ml oil, WANB-US shipping):**

| Order qty | Per-unit COGS |
|---|---|
| 1 | $13.50 |
| 2 | $11.90 |
| 3 | $11.37 |
| 4 | $11.10 |
| 5 | $10.94 |
| 6 | $10.83 |

**Payment processing (Shopify Payments, ~2.9% + $0.30):** $1.75 on a $49.99 order

**Break-even CAC = Price − COGS − processing fee**

| Order qty | Break-even CAC |
|---|---|
| 1 (worst case) | **$34.74** |
| 3 | $36.87 |
| 6 (best case) | $37.41 |

**Use $34.74 / £26.72 as your working number** until you tell me which order-quantity tier you're actually buying at — it's the safe/conservative end, so you won't accidentally scale an ad that's actually unprofitable.

**Target CAC (20% margin buffer, so a "scale" decision isn't just break-even):**
$34.74 × 0.8 = **$27.79 / £21.38**

---

## 2. Reading your metrics (soft rules, until the mentor doc lands)

- **Link CTR, link CPC** — always read these, never "all" CTR/CPC.
- **CPM** — compare to your own account average for this audience, not an outside benchmark.

## 3. Spend-gated checkpoints (kill before you even have a purchase read)

| Checkpoint | Spend trigger (USD) | Spend trigger (GBP) | What it means |
|---|---|---|---|
| 0 link clicks | $14 (0.5× target CAC) | £10.77 | Creative isn't stopping the scroll |
| 0 Add to Cart | $28 (1× target CAC) | £21.54 | Landing page or offer mismatch |
| 0 Initiate Checkout | $42 (1.5× target CAC) | £32.31 | Price objection or trust gap |
| 0 Purchases | $70 (2.5× target CAC) | £53.85 | Hard stop, regardless of upper funnel |

**Important caveat as of Day 1 (2026-10-25):** these checkpoints assume the ad-level
"0 Add to Cart / 0 Purchases" reading is real. It might not be — see the Day 1 log below.
Confirm per-ad attribution via Shopify order source before killing anything on checkpoint
B, C, or D. Checkpoint A (0 link clicks) is safe to act on immediately since it doesn't
depend on attribution at all — a click either happened or it didn't.

(Multiples are a draft, same spirit as your R2/R3 rule of killing around 2–2.5× target with zero sales. Adjust once the mentor doc gives real numbers.)

## 4. Once a purchase lands

- Need 2+ purchases before judging CAC off one data point.
- **CAC ≤ $27.79 (target)** → keep / scale
- **$27.79 < CAC ≤ $34.74 (break-even)** → watch, don't add budget yet
- **CAC > $34.74** → kill

---

## 5. What I still need from you

- Which order-quantity tier you're actually paying (changes break-even CAC by about $2.70 across the range above)
- Your mentor's doc, to replace the placeholder thresholds in sections 2–3

---

## 6. Day 1 log — R4 new creative set (2026-10-25)

Account-wide, confirmed healthy: Meta Pixel fully active (PageView, ViewContent, ATC, IC,
Purchase all firing, Purchase match quality 9.0/10). Shopify shows 4 orders, $336 total
sales, 1.73% conversion rate today. The site and pixel are not the problem.

What's unresolved: whether any of today's 4 orders came from these 4 new ads specifically,
or from the already-proven orange/purple variants still running. Meta's ad-level breakdown
can lag the account-wide numbers by a few hours. **Check Shopify Orders → each of today's
4 orders → conversion/referring source (UTM) to settle this directly**, rather than waiting
on Meta's attribution to catch up.

| Ad | Spend | Impr. | CPM | Link clicks | Link CTR | Link CPC | LPV (ad-level) | Purchases (ad-level) |
|---|---|---|---|---|---|---|---|---|
| A1_Swipe | £16.60 | 52 | £319.23 | 1 | 1.92% | £16.60 | 0 | 0 |
| A2_Pillow | £15.74 | 700 | £22.49 | 22 | 3.14% | £0.72 | 0 | 0 |
| A3_CribHair | £23.74 | 1,147 | £20.70 | 31 | 2.70% | £0.77 | 0 | 0 |
| A4_The Scarf | £0.55 | 32 | £17.19 | 2 | 6.25% | £0.28 | 0 | 0 |

**Reads:**
- **A1_Swipe:** CPM is 15–20x the other three on very little delivery (52 impressions). This is independent of the attribution question — a CPM this far outside its siblings in the same ad set usually means a delivery restriction or quality flag, not a creative problem yet. Check the ad's delivery diagnostics before judging the creative itself.
- **A2_Pillow and A3_CribHair:** strong top-funnel numbers — good CPM, solid link CTR, cheap link clicks. Worth protecting. Don't act on their "0 Purchases" until attribution is confirmed via Shopify order source.
- **A4_The Scarf:** too little spend to read yet (£0.55).

**Action order:**
1. Check Shopify order sources for today's 4 orders — settles the attribution question directly
2. Check A1_Swipe's delivery diagnostics for a policy/quality flag
3. Nothing here has cleanly hit a kill checkpoint with reliable data yet — hold spend as is pending #1

---

## 7. LPV mystery — solved

R3 color-test data (below) shows real purchases, with real CAC, on ads that still read
0 Landing Page Views. That settles it: **LPV at the ad level is unreliable here, not
broken tracking.** Almost certainly Purchase is landing via Shopify's server-side
Conversions API (robust, hard to block) while LPV depends on the client-side browser
pixel, which a meaningful share of traffic blocks (ad blockers, Safari ITP, iOS tracking
restrictions). Trust Purchase and CAC numbers at the ad level. Ignore LPV reading 0 —
it doesn't mean the ad isn't converting.

## 8. Day 1 log — R3 color test (2026-10-25)

Ad set holds the three large-text color refinements plus the **original R1-winning ad as
a control** (the "no before baseline" gap flagged when this test was built), plus a
separate advertorial-destination test on the orange creative.

| Ad | Role | Spend | Impr. | CPM | Link clicks | Link CTR | Link CPC | Purchases | CAC |
|---|---|---|---|---|---|---|---|---|---|
| **Copy 2-OG** | Control — original R1 winner, small text, PDP direct | £9.02 | 96 | £93.96 | 1 | 1.04% | £9.02 | 0 | — |
| **Orange_Textincrease** | Refined — large text, orange, PDP direct | £31.41 | 100 | £314.10 | 4 | 4.00% | £7.85 | 1 | £31.41 (above £26.72 break-even) |
| **Purple_Textincrease** | Refined — large text, purple, PDP direct | £27.70 | 216 | £128.24 | 5 | 2.31% | £5.54 | 1 | £27.70 (just above break-even) |
| **Green_Textincrease** | Refined — large text, green, PDP direct | £17.56 | 143 | £122.80 | 3 | 2.10% | £5.85 | 0 | too early |
| **Copy 3-OG** | Refined — large text, orange, points to the **advertorial** instead of PDP | £30.34 | 188 | £161.38 | 11 | 5.85% | £2.76 | 0 | too early |

**This accounts for 2 of today's 4 Shopify orders** (Orange, Purple). The other 2 are
still unattributed — check against R4's ads next, or other sources.

**Reads:**

- **Meta's own delivery is already voting for the large-text refinement.** All four
  refined/advertorial variants combined pulled £106.99 in spend; the original small-text
  control pulled £9.02 — roughly an 11:1 ratio, in the same ad set, same audience, same
  auction. Meta's algorithm predicts the refined versions perform better and is spending
  accordingly, before you've even looked at conversion data. That's a real signal in
  favor of the text-size change, independent of the sales so far.
- **Control also has the worst link CTR of the group by a wide margin** (1.04% vs 2.10–5.85%
  on the refined versions) — consistent with "bigger text, better thumb-stop," though its
  sample (1 link click) is too small to lean on heavily yet.
- Orange and Purple each converted once. 1 purchase isn't enough to judge CAC against
  break-even (see section 4's minimum-purchases rule) — hold, don't kill, watch whether
  the next sale pulls the average up or down.
- **Advertorial (Copy 3-OG) vs PDP-direct (Orange_Textincrease), same creative:** the
  advertorial got nearly double the impressions for similar spend, half the CPM, a better
  CTR, and link clicks at a third of the cost. No purchases yet, but 11 clicks is too few
  to read a conversion rate off. Worth comparing cost-per-purchase between these two once
  Copy 3-OG gets its first sale — the advertorial trades a cheaper click for an extra hop
  before checkout, which can cut either way.
- Both Orange ads (PDP-direct and advertorial) show a high CPM on low impression volume,
  same pattern as A1_Swipe in the R4 set — increasingly looks like a general
  early-delivery-phase spike across the account rather than a flag on one specific
  creative, but still worth a glance at delivery diagnostics if it doesn't settle as
  spend increases.
- **Leave the control running as-is.** Its low spend isn't a problem to fix — it's Meta
  telling you something. Don't force extra budget into it; let the natural delivery
  split keep being a data point.

---

## 9. Day 1 log — Hook isolation test (ad set now off, 2026-10-25)

Control = the original converting hook ("I actually do my scalp oil every night now...").
4 challenger hooks, body/mechanism/close held identical. Ad set has since been turned off.

| Ad | Hook concept | Spend | Impr. | CPM | Link clicks | Link CPC | Purchases | CAC |
|---|---|---|---|---|---|---|---|---|
| Control | — | £88.62 | 649 | £136.55 | 21 | £4.22 | 1 | £88.62 |
| HookB | Shelf-Confession *(unconfirmed)* | £32.39 | 687 | £47.15 | 18 | £1.80 | 0 | — |
| HookC | Habit-Death-Moment *(unconfirmed)* | £2.24 | 76 | £29.47 | 3 | £0.75 | 0 | — |
| HookD | **Social-Compare** *(confirmed via ad preview screenshot)* | £37.41 | 1,657 | £22.58 | 44 | £0.85 | 0 | — |
| HookE | Dialogue-Sister *(unconfirmed)* | £12.89 | 161 | £80.06 | 8 | £1.61 | 0 | — |

**Correction:** HookD was previously logged as the "Timestamp-Evidence" hook from a
different, earlier hook test built for a different angle. The ad preview confirms it's
actually **Social-Compare**, from the later Ad-C-angle hook set
(`creatives/build-r2-adC-variants.js`). Two separate hook sets built at different points in
this account collided on the same B/C/D/E letters — B/C/E above are relabeled by that same
later set's naming pattern but not yet confirmed by screenshot text.

**Read:** the control "won" the only sale, but at a CAC (£88.62) more than 3x break-even,
and at a CPM/CPC 2-6x worse than every challenger. That's a fatigue signal at least as much
as a persuasiveness signal — this hook has now run across R1, R2, every R3 color variant,
and this round. No challenger reached comparable spend before the set was turned off, so
their 0-purchase reads aren't meaningful yet. HookD/Social-Compare stands out: cheapest
CPM, by far the most volume (44 link clicks on £37.41), no sale yet but never given a
comparable chance. **Don't treat this as "the hook is settled, stop testing hooks."** See
the corrected Fixed vs Swappable section in `ninu-dissect-winner-adC.md`.

## 10. HookD/Social-Compare retest (in progress)

Corrected plan: reactivate the existing hook-test ad set, pause HookB/C/E, leave the
existing **A1_C_HookD ad untouched** (same copy, same image — no need to rebuild anything),
set ad set daily budget to **£15/day**. Checkpoints scaled from section 3: £10.77 (0 link
clicks) / £21.54 (0 ATC) / £32.31 (0 IC) / £53.85 (0 purchases, hard stop, ~3.6 days at
£15/day). Ceiling: ~4-5 days / £60-75 total before a final call either way.

## 11. Mid-day log — advertorial (Copy 3-OG) killed (2026-10-26)

| Ad | Spend | Impr. | CPM | Reach | Freq. | Link clicks | Link CTR | Link CPC | Purchases |
|---|---|---|---|---|---|---|---|---|---|
| A1_C_Messyroutine – Copy 3-OG (advertorial) | £58.48 | 298 | £196.24 | 272 | 1.10 | 19 | 6.38% | £3.08 | 0 |

**Hard stop breached:** spend (£58.48) has passed the £53.85 checkpoint (2.5× target CAC, 0
purchases) from section 3. Trust this read — it's a Purchase count, not an LPV number, and
section 7 already established Purchase/CAC is reliable at the ad level in this account.
**Decision: kill this ad.**

CTR is genuinely good (7.05% all / 6.38% link) — the creative isn't the problem. The CPM
(£196.24) is the problem, and it got worse as spend increased (was £161.38 at £30.34 spend in
section 8, now £196.24 at £58.48), so this isn't an early-delivery blip settling out — it's a
consistently expensive lane, most likely a thin/expensive audience-placement combo for this
specific ad, not a creative-quality signal from Meta.

Same creative as PDP-direct (**Orange_Textincrease**, section 8) already converted once at
£31.41. Not a clean paired test yet, but directionally this favors PDP-direct over the
advertorial hop for this creative — the extra page isn't earning its keep so far.

**Action:** turn this ad off, let the freed budget flow to the HookD retest (section 10) or
back toward Orange/Purple, which have both already proven they can convert.

## 12. Mid-day log — R3 color set, Purple scales, Green paused (2026-10-26)

| Ad | Spend | Impr. | CPM | Reach | Freq. | Link clicks | Link CTR | Link CPC | Purchases | CAC |
|---|---|---|---|---|---|---|---|---|---|---|
| **Purple_Textincrease** | £41.81 | 363 | £115.18 | 319 | 1.14 | 16 | 4.41% | £2.61 | 2 | **£20.91** |
| **Orange_Textincrease** | £52.42 | 214 | £244.95 | 175 | 1.22 | 7 | 3.27% | £7.49 | 2 | £26.21 |
| **Green_Textincrease** | £31.85 | 256 | £124.41 | 180 | 1.42 | 6 | 2.34% | £5.31 | 0 | — |
| Copy 2-OG (control) | low (historic, see section 8) | — | — | — | — | — | — | — | 0 | — |

**Purple clears target CAC (£21.38) with 2 purchases — this is now the clean scale signal in
this ad set.** Meta's own delivery already agrees: 363 impressions vs Orange's 214 on
comparable spend, same ad set, same auction — the algorithm is already favoring Purple before
we touch anything.

**Orange sits between target (£21.38) and break-even (£26.72) — watch, don't push extra
budget at it specifically.** Its link CPC (£7.49) is ~3x Purple's (£2.61) for the same 2
purchases — it's converting, just working harder and costing more to get there. Both CAC
numbers are still noisy on an n of 2, so not a kill, just not the one to chase.

**Green: no checkpoint technically breached (£31.85 spent, hard stop is £53.85), but it's the
weakest ad in the set on every comparable metric** — worst link CTR (2.34% vs 4.41%/3.27%),
second-worst CPC, zero purchases. With budget thin, no case for continuing to fund the set's
laggard just to let it reach its own checkpoint on principle.

**Decision:**
1. Pause Green now.
2. Leave Copy 2-OG running as is — already starved of spend by Meta's own allocation, costs
   nothing to leave alone.
3. Raise the ad set's daily budget by 20% (safe increment, won't reset learning phase) —
   sequenced *after* pausing Green, so the increase flows into a cleaner pool (mostly Purple,
   some Orange) rather than also re-funding the proven laggard.

## 13. Mid-day log — R4 new creative set, A3_CribHair killed (2026-10-26)

| Ad | Spend | Impr. | CPM | Link clicks | Link CTR | Link CPC | Clicks (all) | Purchases |
|---|---|---|---|---|---|---|---|---|
| A2_Pillow | £19.74 | 939 | £21.02 | 28 | 2.98% | £0.71 | 122 | 0 |
| A3_CribHair | £63.48 | 4,826 | £13.15 | 104 | 2.15% | £0.61 | 1,588 | 0 |
| A4_The Scarf | £8.04 | 74 | £108.65 | 3 | 4.05% | £2.68 | 6 | 0 |
| A1_Swipe | not reported this round | — | — | — | — | — | — | — |

**A3_CribHair — hard stop breached and killed.** £63.48 spent, past the £53.85 checkpoint
(2.5× target CAC), 0 purchases. Notably this ad has the best CPM of the set by far (£13.15,
improved from £20.70 at the section 6 check) and the most volume, but none of that cheap
traffic has converted. Flag worth a quick look, not a blocker to the kill: "Clicks (all)" is
1,588 against only 104 link clicks — most engagement on this post isn't clicking through at
all. Worth a scroll through the comments to rule out people reacting to the "husband finds hair
near the crib" framing rather than genuinely curious about the product (this was already flagged
as the one risk in this creative's pre-launch check in `creatives/r4-image-prompts.md`), but the
spend decision doesn't wait on that — kill it now regardless.

**A2_Pillow is the strongest performer in this set right now, sale or not.** Cheapest CPM with
a meaningful sample (£21.02), solid link CTR (2.98%), link clicks at £0.71 — nowhere near any
checkpoint. No action, let it keep running.

**A4_The Scarf** — too little spend (£8.04) to read anything yet. Watch.

**A1_Swipe** — missing from this check-in. Last known reading (section 6) had its CPM at
£319.23, 15-20x its siblings on very little delivery — flagged then as a possible delivery
restriction or quality flag. Get current numbers on this one next.
