# Video test (2026-11-17)

Campaign `Glowling_R1_BF26_VIDEO_TEST` 120252690625940104 (OUTCOME_SALES, ABO). Canada only, ages 28-65+, same audience/placement settings as the main campaign, ad sets end 2026-11-20 21:30 UTC.

| Video | Ad set | Ad | Video id |
|---|---|---|---|
| V2 gift/birthday (baseline) | 120252690626460104 | 120252690628900104 | 2332631197523179 |
| V4 last-chance urgency | 120252690629130104 | 120252690631110104 | 2070299686986161 |
| V5 creativity-led | 120252690631200104 | 120252690631710104 | 1214660444584964 |

£10/day per ad set (£30/day, about £90 over 72h). Files: ads/video/final/V{2,4,5}_remake_v2.mp4.
Decide on: hook rate (3s views/impressions), link CTR, cost per landing page view; ATC only as tiebreaker. Canada has no consent banner so page views are measured properly.
Flag-only: hook < 15% after 1,000 imp; link CTR < 0.7% after 1,500 imp. Nothing is paused automatically.
Readout: `python3 ads/launch/vtcheck.py`.
After 72h: top two go into the main campaign and the UK ad set; the rest are paused, not deleted.
Not yet checked: Meta may ask for an AI-content label on these videos.
