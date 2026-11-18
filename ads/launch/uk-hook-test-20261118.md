# UK hook test (2026-11-18)

New ad set inside the existing UK campaign `Glowling_R1_BF26_UK_ABO` (120252690007440104):
`Glowling_R1_BF26_UK_HookTest_28-65plus` (120252703003530104), £30/day, ACTIVE. Settings copied from the existing UK ad set and verified identical: GB only, 28-65+, Advantage audience off, same placements, Purchase optimization on the pixel, 7d click / 1d view, lowest-cost bidding.
The existing UK ad set (120252690007540104, £30/day, banded-image ads included) is untouched.

| Ad | Ad id | Creative id | Paragraph 1 |
|---|---|---|---|
| UK_HT_A_control | 120252703004380104 | 990270260312745 | original (45 words) |
| UK_HT_H1_number | 120252703004780104 | 1453629950302697 | number-first (37 words) |
| UK_HT_H2_item | 120252703004880104 | 1643384734153470 | item-first (41 words) |
| UK_HT_H3_result | 120252703005040104 | 2038063816874046 | result-first (43 words) |

Verified: paragraphs 2-31, image (fixed 4:5, hash b24ce687...), headline, description, button, link and UTMs identical in all four. Hook texts: `ads/hook-test-dinner-ledger.md`.
Meta picks the winner inside the one ad set (no per-ad minimum spend exists). Read per-ad impressions, CTR, CPC; no verdict for an ad under about 300 impressions after 48h. 24-hour checkpoint: flag any hook under ~100 impressions while others exceed 500, and offer to move it to its own small ad set. Orders per cell: Shopify `utm_content` carries the ad name.

## Budget and ladder
Pace: main CBO £40 + old UK set £30 + hook test £30 = about £100/day. Lifetime spend at launch: £303.44.
User chose "raise ladder" instead of offsetting. New flag-only checkpoints (proposed by Claude, user to correct): step B £400 -> £600 (a 3-day test at this pace reaches about £600), hard stop £600 -> £800. Nothing auto-pauses; the 3-hour check reports against these numbers.
