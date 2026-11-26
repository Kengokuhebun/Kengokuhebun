# Longform hook test — launched 2026-11-26

Declared single variable: copy structure (longform body framework). Everything else — hook, image, headline, CTA, offer, targeting, destination — held identical across all 4 variants and against the RS_01_selfie/V1_selfie-sticky control pair.

## What changed

### Paused (7 ads)
- RS_02_bin (120252790779160104) — cheap clicks, zero ATC, pattern proven twice
- RS_G_A_control (120252790785690104) — gradient format, 0 ATC, superseded by this test
- RS_G_H1_number (120252790786500104) — gradient format, 0 ATC
- RS_G_H2_item (120252790787180104) — gradient format, 0 ATC
- RS_G_H3_result (120252790788060104) — gradient format, 0 ATC
- V2_plugin-sticky (120252836514740104) — £0.95 spent, 0 link clicks, Meta not serving
- V3_handoff-notext (120252836515070104) — £1.31 spent, 0 clicks, Meta not serving

### Active (6 ads, same £70/day CBO)
- RS_01_selfie (120252790778870104) — proven control, 5 ATC, 1 purchase
- V1_selfie-sticky (120252836514350104) — snipe winner, 2 ATC at £81.50 CPM
- L1_proof-stack (120252852892030104) — NEW
- L2_immersion (120252852892820104) — NEW
- L3_reverse-instruction (120252852893400104) — NEW
- L4_identity (120252852893860104) — NEW

### New ad set
`Glowling_R2_RS_Longform4` (120252852890980104), ACTIVE, same campaign (`Glowling_R2_BF26_RitualSwipe_CBO`, £70/day CBO).

## Test design

| Element | Value | Locked? |
|---|---|---|
| Hook (paragraph 1) | "My 5-year-old asks for this by name. Plug it in, hand him the markers — that's the whole setup." | Locked — purchase-proven |
| Image | V1_selfie-sticky (native format, hash 135ee33f1e4cf717cdfb83ecc7e39c0d) | Locked — half-CPM winner |
| Headline | The toy that doesn't go in the garage | Locked |
| Description | Buy 2, Get 1 FREE + free tracing book. Ends Cyber Monday. | Locked |
| Primary text body | 4 structural variants (see below) | **THE VARIABLE** |

### Copy structure variants

| Ad | Structure | Borrowed from | Key difference | Words |
|---|---|---|---|---|
| L1_proof-stack | Hook → ledger list → friend text → mechanism → result → offer → callback | Belly Band (C1 dinner) | The LIST is the engine, $847 accumulates line by line | ~780 |
| L2_immersion | Hook → present-tense 5:51pm scene → failed toys from the scene → friend → mechanism → absolution → result → offer | Nattokinase (C2 shower) | Reader lives INSIDE the moment, present tense, sensory | ~800 |
| L3_reverse-instruction | Hook → "Do not buy another kit" → ledger as evidence → friend → mechanism → absolution → result → offer → callback instruction | AirVex (C3 WFH) | Authority voice, tells you NOT to do X, then proves why | ~720 |
| L4_identity | Hook → "I had become the iPad mum" → failed toys as evidence of trying → friend → mechanism → identity payoff → offer → identity callback | GoodGrove (C5 gift) | About WHO SHE IS, not what she spent | ~820 |

## Read plan

Compare L1-L4 against RS_01_selfie (short copy, 2 sentences) and V1_selfie-sticky (same image, same short copy):
- If any L variant produces ATC at a lower cost/ATC than RS_01/V1 → longform structure wins, that framework advances
- If all L variants get clicks but no ATC → the problem is downstream of the ad (page/offer), copy structure is not the lever
- CPM comparison: V1's native format at £81.50 is the benchmark, all L variants use the same image so CPM should be similar

If CVR does not improve → next test is offer variations using Origins/Master Doc learnings, with the best-performing ad from this batch as the base.

Full copy in `ads/longform-hook-test/copy-drafts.md`.
