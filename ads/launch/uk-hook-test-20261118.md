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

## Update 2026-11-19: old UK ad set paused, hook test budget raised
User: "Pause uk ad set and keep hook test on bump budget by £10".
- Old UK ad set `Glowling_R1_BF26_UK_Broad_28-65plus` (120252690007540104) set to PAUSED, including `UK_C2-S4-shower-moon_v2` (the ad Shopify's UTMs credit), `UK_C5-S1-gift-ledger`, `UK_C2-S1-shower-ledger`, `UK_C3-S2-wfh-714am` and `UK_C1-S1-dinner-ledger_fix`. Nothing deleted.
- Hook test ad set (120252703003530104) daily budget £30 -> £40; all four ads stay ACTIVE.
- Main campaign (CBO) already paused; video test paused. The UK hook-test ad set is now the only thing running: £40/day.
- UK stop rule (flag at £60 with 0 orders): not restarted explicitly by the user; proposed count from the hook-test launch (2026-11-18 14:51 UTC) is £15.26 spent at the time of this change. Lifetime spend about £400; ladder step B £600, hard stop £800.
