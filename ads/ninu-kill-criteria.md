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

| Ad | Spend | Impr. | CPM | Link clicks | Link CTR | Link CPC | Purchases | CAC |
|---|---|---|---|---|---|---|---|---|
| Orange_Textincrease | £31.41 | 100 | £314.10 | 4 | 4.00% | £7.85 | 1 | £31.41 (above £26.72 break-even) |
| Purple_Textincrease | £27.70 | 216 | £128.24 | 5 | 2.31% | £5.54 | 1 | £27.70 (just above break-even) |
| Green_Textincrease | £17.56 | 143 | £122.80 | 3 | 2.10% | £5.85 | 0 | too early |
| "Copy 2-OG" (stray, not part of the intended test) | £9.02 | 96 | £93.96 | 1 | 1.04% | £9.02 | 0 | — |

**This accounts for 2 of today's 4 Shopify orders** (Orange, Purple). The other 2 are
still unattributed — check against R4's ads next, or other sources.

**Reads:**
- Orange and Purple each converted once. 1 purchase is not enough to judge CAC against
  break-even (see section 4's minimum-purchases rule) — hold, don't kill, watch whether
  the next sale pulls the average up or down.
- Both show very high CPM on very low impression volume, same pattern as A1_Swipe in the
  R4 set. Increasingly looks like a general early-delivery-phase CPM spike (small
  accounts/new edits often see expensive early impressions before the algorithm settles)
  rather than a specific flag on one creative — but still worth a glance at delivery
  diagnostics if it doesn't settle down after more spend.
- **"Copy 2-OG" is not part of the deliberate color-test structure.** It reads like a
  leftover duplicate from building the variants. Check what it's actually running and
  pause it if it's unintentional — it's not telling you anything new and it's spending.
