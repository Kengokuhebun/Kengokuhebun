# UK ring-fence (2026-11-17)

Why: GB requires cookie consent (Shopify consentPolicy GB=true; AU/CA/US=false), so UK visits are under-counted by the pixel and Shopify analytics (63 clicks vs ~15 sessions). Meta's optimizer under-values UK; the UK cannot be judged on LPV/ATC/Purchase.

Created (live):
- Campaign `Glowling_R1_BF26_UK_ABO` 120252690007440104, OUTCOME_SALES, ABO
- Ad set `Glowling_R1_BF26_UK_Broad_28-65plus` 120252690007540104, GB only, 28-65+, £30/day, OFFSITE_CONVERSIONS on Purchase, 7d click / 1d view
- Ads (existing creatives reused, same UTMs): UK_C5-S1-gift-ledger, UK_C2-S1-shower-ledger, UK_C3-S2-wfh-714am

Changed: GB removed from ad sets P (120252679147450104) and G (120252679147800104); both now US, CA, AU.

Judge UK by Shopify orders with UTMs only (utm_campaign=Glowling_R1_BF26_UK_ABO).
Stop rule (flag-only): £60 UK spend with 0 orders -> flag for pause; 1 order -> continue to £120 before deciding.

## Update 2026-11-18
Added two more ads to the UK ad set (existing creatives reused, same UTMs, ACTIVE, in Meta review):
- `UK_C1-S1-dinner-ledger` (Meta credited the Nov 17 purchase to this ad)
- `UK_C2-S4-shower-moon_v2` (Shopify UTMs show order #1001 came from this ad)
UK ad set budget unchanged at £30/day, now 5 ads.
