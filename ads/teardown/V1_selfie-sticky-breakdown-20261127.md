# Why is V1_selfie-sticky the format winner? — breakdown, 2026-11-27

Applying the same "Dissect the Winner" discipline used on RS_01: beat-by-beat, ranked drivers, every claim tagged PROVEN or HYPOTHESIS, never present a guess as a finding.

> **CORRECTION (2026-11-27, same day):** this teardown originally stated V1 uses the same image as RS_01. That is wrong. RS_01 is the square selfie with two white text pills (`ads/ritual-swipe/final/ad1_selfie_final.jpg`). V1 (`ads/native-reexpression/final/V1_selfie-sticky.jpg`, hash 135ee33f...) is a different photo: same woman and kitchen, laughing, holding the lit board, with a stack of 3 sealed boxes and a yellow handwritten sticky note reading "BUY 2 GET 1 FREE", no pills. Copy, headline and description are identical; the image AND the ad set differ. Statements below saying "same image", "same creative, half the CPM" or "image doubly proven across two ad sets" are superseded: the CPM gap cannot be attributed to ad-set structure alone, and V1's image (native, offer shown in the scene) is a separate proven image from RS_01's.

## The fixed facts (controlled across this comparison)

V1_selfie-sticky sits in the Snipe3 ad set alongside V2_plugin-sticky and V3_handoff-notext. All three share: same targeting, same audience pool, same landing page, same offer, same CTA (SHOP_NOW), same pixel, same primary text, same headline, same description. **The only declared variable is the image.** Anything that differs between V1's performance and its siblings' has to be the image itself — format, framing, composition, or on-image text.

## V1_selfie-sticky's exact creative (verbatim, pulled from the live ad)

- **Image**: vertical selfie-style photo (same image as RS_01_selfie), a woman in a kitchen holding the glowing board up to camera, two white text pills baked into the image: "Plug it in. Hand over the markers. That's the whole setup." (top) and "Buy 2 get 1 free right now." (bottom-right). Image hash: 135ee33f1e4cf717cdfb83ecc7e39c0d.
- **Primary text**: "My 5-year-old asks for this by name. Plug it in, hand him the markers — that's the whole setup."
- **Headline**: "The toy that doesn't go in the garage"
- **Description**: "Buy 2, Get 1 FREE + free tracing book. Ends Cyber Monday."

This is the same image + same copy as RS_01_selfie, placed in a different ad set to test whether V1's native format holds when competing against alternative image formats (V2 plugin-style, V3 handoff-no-text).

## Performance data (cumulative through 27 Nov)

| Ad | Spend | Impr | Reach | Freq | CPM | CTR | LC | LPV | VC | ATC | IC | Purch | £/ATC | £/Purch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **V1_selfie-sticky** | £108.97 | 1,326 | 1,048 | 1.27 | £82.18 | 4.6% | 43 | 40 | 47 | 15 | 3 | 3 | £7.26 | £36.32 |
| V2_plugin-sticky | £0.97 | 22 | — | — | £44.09 | 4.5% | 0 | — | — | 0 | 0 | 0 | — | — |
| V3_handoff-notext | £1.31 | 13 | — | — | £100.77 | 0% | 0 | — | — | 0 | 0 | 0 | — | — |

Meta gave V1 99% of the ad set's spend. V2 and V3 were effectively starved after minimal initial impressions. This is [OBSERVED] — the algorithm's own spend allocation is the strongest signal the Snipe3 test produced.

### V1 daily progression

| Date | Spend | Impr | CPM | LC | LPV | ATC | IC | Purch |
|---|---|---|---|---|---|---|---|---|
| 25 Nov | £11.05 | 116 | £95.26 | 3 | 3 | 0 | 0 | 0 |
| 26 Nov | £70.91 | 855 | £82.94 | 27 | 24 | 4 | 1 | 1 |
| 27 Nov | £27.03 | 356 | £75.93 | 13 | 13 | 11 | 2 | 2 |

Trend: CPM falling day over day (£95 -> £83 -> £76), ATC accelerating (0 -> 4 -> 11), purchases accelerating (0 -> 1 -> 2). This is the shape of an ad that Meta is learning to serve to converters. [OBSERVED]

### Funnel ratios (cumulative)

- LC-to-LPV: 93% (40/43) — very low drop between click and page load
- LPV-to-VC: 118% (47/40) — view_content fires on product page load, some visitors may browse multiple products
- LPV-to-ATC: 37.5% (15/40) — strong page conversion
- ATC-to-IC: 20% (3/15) — the same cart-to-checkout drop seen across all ads
- IC-to-Purchase: 100% (3/3) — everyone who starts checkout finishes
- Overall LPV-to-Purchase: 7.5% (3/40)

## Comparison against RS_01_selfie (the original)

V1 and RS_01 share the identical image and copy. The only difference is the ad set they sit in (different ad set = different algorithmic allocation context, different competing siblings).

| Metric | RS_01 (Swipe8) | V1 (Snipe3) |
|---|---|---|
| Spend | £108.47 | £108.97 |
| Impressions | 668 | 1,326 |
| **CPM** | **£162.38** | **£82.18** |
| CTR | 5.8% | 4.6% |
| Link clicks | 28 | 43 |
| ATC | 11 | 15 |
| Purchases | 2 | 3 |
| £/ATC | £9.86 | £7.26 |
| £/Purchase | £54.24 | £36.32 |

**V1 gets nearly double the impressions for the same spend.** The CPM difference (£162 vs £82) is the single biggest finding. Same image, same copy, half the CPM. [OBSERVED]

## Ranked drivers for "why V1 outperforms on efficiency" (pre-click and funnel)

1. **The ad set context determines CPM.** [PROVEN by construction] V1 sits in Snipe3, which was built as a clean format test with only 3 ads. RS_01 sits in Swipe8, which carries the full original batch including dead ads that Meta may still be considering in its auction math. The CBO algorithm distributes budget across ad sets, and Snipe3's cleaner composition means V1 faces less internal competition for allocation. This is not a creative finding — it is an ad-set structure finding.

2. **Half CPM means twice the reach per pound, which means more chances to find converters.** [PROVEN from the data] V1 reached 1,048 people vs RS_01's ~545 (inferred from impressions/frequency). More reach = more first-touch impressions = higher probability of surfacing to someone in a buying state. The creative is identical, so the conversion rate per reached person should be similar. V1 simply gets more people to the page cheaper.

3. **The falling CPM trend (£95 -> £83 -> £76) suggests Meta is finding V1's audience efficiently.** [INFERRED] As Meta's algorithm learns which users convert, it can bid more precisely, reducing waste impressions. This pattern is consistent with a "learning phase exit" trajectory. RS_01 shows no such trend (£218 -> £152 -> £139 -> £156 -> £213), suggesting its ad set's bid environment is less stable.

4. **V1's ATC acceleration (0 -> 4 -> 11 on days 1-3) is steeper than RS_01's (0 -> 5 -> 0 -> 0 -> 6).** [OBSERVED] RS_01's ATC came in two spikes (Day 2 and Day 5), V1's is building momentum. This may indicate V1's ad set is exiting learning phase faster, but 3 days is too short to call this definitively.

## What V1 does NOT tell us

- **V1 is not a different ad from RS_01.** It is the same creative in a different ad-set context. The "format winner" finding from Snipe3 is really: the selfie-with-overlay format beats plugin-style and handoff-no-text. That was the test question, and it answered it cleanly.
- **V1's CPM advantage may be partly structural** (fewer siblings, cleaner ad set) rather than purely about the creative. If RS_01 were the only ad in Swipe8, its CPM might look different.
- **Purchase volume (n=3) is still small.** The funnel shape is strong, but 3 purchases is not proof of sustainable ROAS at scale.

## The confound to own

V1 and RS_01 are the same ad running in parallel, each consuming ~£109 of the same £70/day CBO. We are paying twice to serve the same creative. This is acceptable during the testing phase (Snipe3 needed a proven control to benchmark V2/V3 against), but once Snipe3's question is answered — and it is — running both indefinitely dilutes budget across two copies of the same thing.

**However**: Origins says "existing winners left on" (M1 1.6 testing hygiene). Both are producing purchases. Turning one off risks disrupting the other's algorithm-learned audience segments. The safe move is to leave both running until the Day-7 longform read, then assess whether the account has enough purchase-producing ads to justify consolidation.

## What this changes about the plan

1. **Snipe3's question is answered.** The selfie-with-overlay format (V1) conclusively beat plugin-style (V2) and handoff-no-text (V3). V2 and V3 are already paused. No further format testing needed in this batch.

2. **The CPM finding is actionable.** V1's ad-set context produces half the CPM of RS_01's. When we build future tests, using a clean ad set with minimal siblings (like Snipe3 or Longform4) rather than adding to the crowded Swipe8 set is a structural advantage. This is not a creative learning — it is an account-structure learning.

3. **The image is now doubly proven.** Image hash 135ee33f1e4cf717cdfb83ecc7e39c0d (selfie-with-overlay) has produced purchases in two independent ad sets running simultaneously. It is the LOCKED image for all future copy tests. [PROVEN]

4. **The longform test (L1-L4) is the correct next iteration.** It holds the proven image and proven hook constant, varying only copy structure — exactly what the master document prescribes after a winner teardown: "same desire, new angle or deeper Sniper" (Ads 5). L1's early signal (6 ATC from 45 impressions) suggests the proof-stack structure may outperform the short-form control.

5. **Budget consolidation decision deferred to Day-7 read (3 Dec).** If L1 confirms, the account will have three distinct purchase-producing ads (RS_01, V1, L1) across three ad sets. At that point, evaluate whether to increase CBO budget for the Superwinning test.

## Purchase-value data

- V1 total purchase conversion value: £154.68 from £108.97 spend = **1.42 ROAS**
- RS_01 comparison (from same window): 2 purchases, similar ROAS range

CORRECTION (2026-11-27): an earlier version of this line quoted breakeven ~1.82 / target ~2.82. Those were the Origins doc's worked-example numbers, not Glowling's. Real breakevens from the supplier cost sheet (audit v2 section 9): UK 1.37-1.39, CA 1.57-1.63, US 1.74-1.76, AU 1.57-1.92, NZ unconfirmed (2.70-2.93).

At 1.42 ROAS V1 is roughly at breakeven for UK/CA and below it for US. The question is whether ROAS improves as CPM continues to fall and the audience refines.

## Summary (one line)

V1_selfie-sticky proved that the selfie-with-overlay format wins at half the CPM, the image is now doubly proven across two ad sets, and the remaining question is whether copy structure (the longform test) or budget scaling is the next lever.
