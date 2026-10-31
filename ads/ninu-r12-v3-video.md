# R12: v3 of the 3D sung ad, rebuilt from the v2 retention data

Output: `ninu-3d-sung-ad-v3.mp4`, 720x1280, 51.0s, about 17 MB (not in the repo).
Scripts: `creatives/build-r12-song-v3.py`, `creatives/build-r12-assemble.py`. Cost: 13 credits (song, 2 takes); no new shots.

## What the v2 numbers said (3DVid_1, 739 impressions)

- Hook rate 36% (256 three-second plays), cost per 3s play £0.079: the hook works.
- Time watched (read off the chart, approximate): 83% at 1s, 52% at 2s, 36% at 3s, 18% at 5s, 9% at 10s, 5% at 20s, 2% at 56s.
  About 75% of the 3-second viewers were gone by 10s. There is no single cliff, a smooth decay.
- Only about 3.5% of impressions reached the dispenser (34s) and about 1% the offer (62s).
- Link CTR 1.08%, link CPC £2.53 (Hook3 static: 2.81% and £1.09).
- Correction made along the way: v2's picture cut away at 3.4s while the hook question was still being sung (it ends about 4.5s).

## Changes in v3 and why

| Change | v2 | v3 | Reason |
|---|---|---|---|
| Hook card and shot held until the question is sung | cut at 3.4s mid-word | held to 3.87s | the question is finished on screen |
| Answer arrives immediately | about 20s | 4.0s ("Because, mama, oil poured on your hair mostly stays on your hair") | the curiosity gap is paid off while most viewers are still there |
| Talking-bottle intro, baby/shampoo/yourself montage, Sunday calendar | 3.4 to 17.9s | removed | the stretch where about 75% of the 3-second viewers left, and it delayed the answer |
| Product enters | 34.35s (46% of runtime) | 16.8s (33%) | fewer viewers had seen the product |
| Permission and villain | 26 to 32s | 9 to 17s | earlier |
| Runtime | 74.1s | 51.0s | |
| Song | 112 BPM, autocorr 0.57 | 111 BPM, autocorr 0.47 (same style prompt, new lyrics) | new lyrics needed a new take |

Kept: the hook shot and card, the cross-section shot, the relief shot (retimed so the eyes open on "Oh"), the hook callback, the offer card
(price, free shipping, 30-day guarantee), no deadline text in the video (the primary text carries "ends Nov 10", so the video does not expire).
Dropped: "baby", the Sunday refrain (from the Ad C story), the bottle intro. "mama" now lands at 4.4s.

## Things not verified

- I cannot hear the song. Take 0 was chosen on word timing, steadier pulse and a faster-flowing first line. Listen for "Nee-noo",
  "U.S." and "thirty days".
- The first 3 seconds of audio differ from v2 (new take), so hook rate may move for reasons other than the picture.
- The retention chart was read by eye.

## How to judge v3 against v2 (same copy, same audience, FB and Instagram only)

Wait for about 1,000 impressions, then compare: hook rate (v2 36%), share of 3-second viewers still there at 10s (v2 about 25%),
15-second ThruPlay rate (v2 5.7% of impressions), link CTR (v2 1.08%), link CPC (v2 £2.53). Keep the usual spend checkpoints
(£14/0 link clicks, £28/0 add-to-cart, £42/0 checkout, £54/0 purchases).
