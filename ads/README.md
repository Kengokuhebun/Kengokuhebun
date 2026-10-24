# Ninu Round 1 test: Meta Ads Manager files

**Approved structure:** 1 campaign (ABO), 1 ad set at $100/day, 3 ads. $300 to the kill checkpoint (3 days), max exposure $500.

| File | What it is |
|---|---|
| `ninu-r1-test-ads.md` | R1 short-form primary text, headline, creative direction, Kitsch swipe mapping |
| `ninu-r1-long-form.md` | R1 long-form primary text (chiefed against AARREIGN protocol) |
| `ninu-r1-validation.csv` | R1 bulk import: 1 campaign, 1 ad set, 3 ads (A short, B short, C short), all PAUSED |
| `ninu-r2-hook-test.md` | R2 hook isolation test: angle + desire extraction, 6 hooks (control + 5 variants), shared body, kill rules, next-phase roadmap |
| `ninu-r2-hook-test.csv` | R2 bulk import: same campaign, new ad set, 6 ads @ $150/day, all PAUSED |
| `ninu-r3-cpm-refinement.md` | R3: color-test ad set (orange/purple/green, larger text) + advertorial-destination test, no new copy |
| `ninu-r4-new-creative-set.md` | R4: new ad set, 4 ads — 1 Kitsch swipe reproduction + 3 original natives, same proven DNA, full copy + image prompts |

The earlier 5-ad-set CBO file was removed because it didn't match the approved structure.

## Import steps

1. Check the open items at the bottom of `ninu-r1-test-ads.md` (first-person leads, oil bottle branding, URL).
2. Confirm the Meta Pixel fires `Purchase` and that you've placed a real test order.
3. Ads Manager, then Import, then upload the CSV. Everything imports paused.
4. Attach the creative for each ad, then turn the campaign on.

## During the test

- Don't edit anything for the 3 days.
- Report link CTR and link CPC separately from "all" CTR and CPC.
- Per ad: spend, CPM, link CTR, link CPC, landing page views, sessions, ATC, initiate checkout, purchases, with the rate at each step.
- End of Day 3 with 0 purchases: pause and take the data to your mentor. With 1+ purchases: open a second avatar ad set and start collecting real reviews.
