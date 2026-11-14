# Winning Long-Form Ad Specs — Index & Comparison

Ten winning long-form ads, each taken apart with the **Dissect Winner** protocol from the Master Document (one ad per file, nothing inferred, every spec cited by paragraph). This page compares the ten spec cards so the shared structure is visible.

## How this folder works

| Path | What it is |
|---|---|
| `sources/<ad>.txt` | The ad exactly as pasted. Every non-empty line is one paragraph (¶). |
| `templates/<ad>.md` | The hand-written analysis with `{{…}}` placeholders and the beat ranges. |
| `ad-spec-<ad>.md` | The finished spec: template + measured sections (paragraph index, baseline counts, line-level counts, rhythm map, beat word budgets). |
| `tools/measure.py`, `tools/extra.py`, `tools/build_spec.py` | Scripts that do all counting, so no number is estimated by eye. |

To add an ad: save it to `sources/`, write `templates/<ad>.md` (first line `<!-- BEATS: 1-5:Hook | 6-12:… -->`), then run
`python3 tools/build_spec.py sources/<ad>.txt templates/<ad>.md ad-spec-<ad>.md` — it fails loudly if any paragraph is unassigned or double-counted.

## The ten specs

| # | Spec | Product | Narrator | Avatar addressed | Lead | Awareness | Stage |
|---|---|---|---|---|---|---|---|
| 1 | [Vibriance — "Linda"](ad-spec-vibriance-super-c-linda.md) | Vitamin C serum | 66-y/o best friend of the sufferer | Women 50+ with returning spots, and those who love them | Story (aftermath open) | Solution Aware | 3 |
| 2 | [Noverly Nattokinase — "First date"](ad-spec-noverly-nattokinase-first-date.md) | Nattokinase supplement | Single man | Men who blame porn for ED | Story (mid-failure open) | Problem Aware | 3 |
| 3 | [AirVex — "Mark Ellis"](ad-spec-airvex-pro-mark-ellis.md) | Sleep-apnoea mouthpiece | NHS CPAP therapist turned patient | People who failed CPAP | Story (reverse-instruction open) | Solution Aware | 3 |
| 4 | [Belly band — "Grandmother's $549"](ad-spec-colic-belly-band-grandmother.md) | Warm colic belly band | 63-y/o grandmother (buyer, not user) | Relatives buying for a pregnant/new mother | Promise → Story | Unaware | 3 |
| 5 | [GoodGrove — "Posy"](ad-spec-goodgrove-tart-cherry-posy.md) | Tart cherry capsules | 57-y/o grandmother | Grandmothers with back arthritis they call "my age" | Story (relationship-loss open) | Problem Aware | 5 |
| 6 | [Noverly Magnesium — "GLP-1 sisters"](ad-spec-noverly-magnesium-glp1-sisters.md) | Magnesium complex | 56-y/o woman with a control-case sister | Women regaining after GLP-1 | Story (secret-tease open) | Problem Aware | 4 |
| 7 | [Pointex — "Patty"](ad-spec-pointex-knee-replacement-patty.md) | Pen-sized pulse device | 66-y/o, two knee replacements | First 6 months after knee replacement | Story (two-runs open) | Problem Aware | 3 |
| 8 | [Resia — "Lisa Hart"](ad-spec-resia-ceylon-cinnamon-lisa-hart.md) | Ceylon cinnamon softgels | Newly diagnosed type 2, signed | Newly diagnosed type 2 on metformin | Story (reverse-instruction open) | Solution Aware | 4 |
| 9 | [Zyara — "Anna"](ad-spec-zyara-denture-reliner-anna.md) | Denture reliner gel | 64-y/o widow dating again | Denture wearers using cream | Story (shock open) | Solution Aware | 3 |
| 10 | [Tulas — "Dr. Megan"](ad-spec-tulas-skinny-jade-ring-megan.md) | 4mm jade ring | 34-y/o family doctor | Women who never keep a ring on; gift-givers | Story (forced-removal cold open) | Solution Aware | 5 |

## Measured comparison

| Ad | Words | ¶ | Avg words/sentence | % one-sentence ¶ | ! | Questions | you/100w | Brand at | Price at |
|---|---|---|---|---|---|---|---|---|---|
| Vibriance | 5,561 | 256 | 9.4 | 44% | 0 | 12 | 1.0 | 70% | — |
| Noverly Nattokinase | 1,543 | 98 | 11.0 | 70% | 0 | 5 | 1.5 | 58% | — |
| AirVex | 2,330 | 115 | 6.5 | 32% | 0 | 2 | 1.3 | 65% | 63% |
| Belly band | 899 | 32 | 10.5 | 41% | 0 | 1 | 1.6 | never named | 37% |
| GoodGrove | 3,461 | 134 | 9.7 | 40% | 0 | 8 | 2.7 | 54% | — |
| Noverly Magnesium | 3,000 | 116 | 9.1 | 26% | 0 | 10 | 2.8 | 60% | 34% |
| Pointex | 1,728 | 91 | 8.0 | 37% | 0 | 9 | 2.6 | 67% | — |
| Resia | 1,055 | 48 | 7.1 | 21% | 0 | 2 | 1.8 | 0% | 87% |
| Zyara | 2,471 | 116 | 9.7 | 32% | 0 | 9 | 2.0 | 63% | — |
| Tulas | 2,740 | 133 | 9.6 | 35% | 0 | 10 | 1.5 | 50% | 92% |

"—" = no price number anywhere in the copy. Range 899–5,561 words; median ≈ 2,400.

## What all ten have in common (counted across the specs)

1. **Zero exclamation marks.** 0 in 25,000+ words across all ten ads.
2. **First-person story, every time.** 10/10 use a Story lead. The opening device varies (aftermath, mid-failure, reverse instruction, shock line, cold open, control comparison), but the body is always one person's story.
3. **Short sentences.** Averages run 6.5–11 words per sentence; 9 of 10 sit between 7 and 10.5.
4. **The discovery comes from a peer or insider, never an ad.** 10/10: a stranger's sister on Facebook, a forum guy, a colleague, a daughter on Reddit, a sister (×2), a 51-year PT, a diabetes educator, a friend at the Y, a swimmer at the pool.
5. **Problem mechanism before the product.** In 9/10 the mechanism enters at 32–49% and the brand at 50–70%. Resia is the exception: brand in the hook, mechanism after the results.
6. **The narrator fails with the standard fix first.** 10/10 list what they already tried, usually with a price or a number (protocol $1,340; CPAP 3.1 hrs/night; $549 of gifts; $740 mattress; $64 + $9 rings).
7. **An absolution line.** 8/10 tell the reader it isn't their fault, e.g. AirVex "It wasn't you. It was the machine.", Zyara "It was never you.", Pointex "And it wasn't you."
8. **The ending calls back the opening.** 10/10 close the opening loop with the same object or scene: the photo, the CPAP in the corner, the kneel, the empty pill slots, the plastic cup, "Big weekend again?"
9. **Risk reversal.** 9/10 have a money-back or trial guarantee (30 nights to 1 year). Tulas is the exception: a certificate and a lifetime craftsmanship warranty.
10. **Price is downplayed.** 5/10 never state a price number. The other five state it late (Resia 87%, Tulas 92%) or anchor it against a bigger failed spend (AirVex vs £1,500 dentist; belly band vs $549; magnesium vs $1,100/month).
11. **Scarcity is optional.** Only 3/10 use sell-out or stock language (Vibriance, Nattokinase, Noverly Magnesium) and Resia uses a reverse "don't buy it" version. 5/10 use no scarcity at all.

## Where they differ (the choices to make per product)

| Choice | Options seen | Ads |
|---|---|---|
| Who narrates | The sufferer / the buyer for someone else / a professional who became the patient | most / Vibriance, Belly band / AirVex, Tulas |
| Opening device | Aftermath; mid-failure; reverse instruction; buyer callout + promise; relationship loss; control comparison; two runs of the same ordeal; shock line; forced removal | 1; 2; 3, 8; 4; 5; 6; 7; 9; 10 |
| Claim strength | Strong mechanism claims / self-limited claims + disclaimers | 1-3, 6-9 / 5, 10 |
| Where the click goes | Product page / article pre-sell / platform button | most / Noverly Magnesium / Resia ("Tap Learn More.") |
| Gift framing | Present (buy one for her, get three, send her the link) | 1, 4, 6, 7, 10 |

## Most relevant to the LED drawing board (recommendation, not part of the specs)

The drawing board is bought as a **gift**, often by **grandparents**, and the angle we're testing is screen time. Three specs match that situation most closely:

- **Belly band** ([spec](ad-spec-colic-belly-band-grandmother.md)): written to the gift-buyer, not the user. Its structure is a priced ledger of beautiful gifts that failed, then the cheap one that solved the real problem, then "That is the gift." This maps directly onto *"I've bought $___ of toys that lasted ten minutes; the iPad still wins."*
- **GoodGrove** ([spec](ad-spec-goodgrove-tart-cherry-posy.md)): a grandparent losing time with a grandchild, the family excused rather than blamed, and a payoff that returns exactly what the hook took. A screen-time version: *the grandkids only want the iPad at my house*.
- **Tulas** ([spec](ad-spec-tulas-skinny-jade-ring-megan.md)): gift close ("get the three"), a sensory test the reader can picture, and a sceptical professional who refuses folklore claims. Useful if we use a teacher or OT narrator and need to stay away from unprovable claims.

**Noverly Magnesium's control comparison** ("same drug, different outcome") is also worth testing: two kids the same age, one glued to the tablet, one drawing.

We should pick the structure only after the deep-research report confirms the avatar.
