# R11: v2 of the 3D sung ad, rebuilt from the R10 teardown

Built from `ninu-r10-reference-teardown-vs-ours.md` section 7. Same character (Maya), same product, same Sunday
story as v1 (`ninu-r9b-3d-sung-ad-scene-breakdown.md`). What changed is the structure: the hook, a problem-mechanism
and permission block, the avatar in the words, and a faster steady pulse.

Output: `ninu-3d-sung-ad-v2.mp4`, 720x1280, 74.1s, about 25 MB (not in the repo). Scripts: `creatives/build-r11-song.py`,
`creatives/build-r11-v2-shots.py`, `creatives/build-r11-assemble.py`.

## 0. What I could and could not check

- I checked frames, cut timing, caption timing and the sung-word timestamps. I cannot hear the audio. Before it runs
  as an ad, listen for "Nee-noo" (printed as NINU in captions), "U.S." and "thirty days".
- The bottle's mouth is not lip-synced. In a cartoon this reads as talking, but look at the first 9 seconds on a phone.
- None of this proves it converts. The reference ad is a confirmed delivery winner (R10 section 0b), not a proven sales
  winner, and this ad has had no spend. The zero-orders-since-Oct-26 funnel gate in R9b section 9 still applies.

## 1. What changed, and why (each tied to R10)

| R10 finding | v1 | v2 |
|---|---|---|
| Hook scored 0 of 8 | "I actually do my scalp oil every night now" (success claim, calm face, first caption 1.64s) | Frame 0: white text card "WHY IS MY HAIR OIL NOT DOING ANYTHING??" over a wide-eyed, distressed Maya with oil running down her neck. A talking oil bottle interrupts at 3.4s: "Hey mama, it's me." |
| No problem mechanism | solution only | 9.2-34.35s (33.9%): blame stack, "I never reached your scalp", "it wasn't you", "it was the dropper", "hair doesn't drink oil, skin does" |
| No permission device | none | "It wasn't you. It was never you." |
| Avatar not in the words (2nd person 1.1 per 100) | no "mama", "baby", "you" | "Hey mama" at 4.6s, "baby" at 9.7s, 2nd person 10.4 per 100 words (reference 9.5) |
| 4 scene changes in 30s | 4 | 10 |
| Pulse 0.24 (rubato ballad, "sung slowly") | 74 BPM | 113 BPM, autocorrelation 0.57 |
| Product on screen from frame 0 | dispenser on her knee in frame 0 | first appears at 34.35s (46.4% of runtime), after the cause is settled |
| Hook never called back | none | 53.0-58.4s: "Not doing anything? I was never getting there." with Maya, now warm, over a sheepish bottle |
| Sunday used once | refrain only | Sunday is the shame ("You said you'd start over Sunday") and the payoff ("Now Sunday can stay on the calendar") |

Kept from v1: product fidelity (the dispenser clips are unchanged), the cool-to-warm grade as the payoff, the Sunday
callback, the personal "oh" moment. Not copied from the reference: PCOS, hormones, "but not for long", any health claim.

**Decision for you:** your original brief said "sung slowly". The teardown's finding was that the slow rubato ballad
was part of why the hook scored 0 of 8, so v2 is a steady 113 BPM. If you want the slow version back, v1 is untouched.

## 2. Script (sung, 74.1s)

Word timestamps are the generated song's (take 0 minus a 1.5s lead-in), 154 words, 2.08 words per second.

| Time | Sung line | Picture |
|---|---|---|
| 0.0-3.4 | Why is my hair oil not doing anything? (text card on screen) | H1: Maya, towel, oil streak down her neck, wide eyes, flinches touching her hairline |
| 3.4-9.2 | Hey mama, it's me. The one you swore you'd use every night. | H2: the old amber dropper bottle pops up on the shelf, waves, looks sheepish, shrugs (dust puff) |
| 9.2-10.7 | You blame the baby. | BL1: Maya rubbing her eyes in a dark nursery, baby monitor glow (no baby visible) |
| 10.7-12.6 | You blame the shampoo. | BL2: drops a shampoo bottle in a basket |
| 12.6-14.4 | You blame yourself. | BL3: forehead in her palm |
| 14.4-17.4 | You said you'd start over Sunday. | B1 (reused from v1): circled Sunday, the bottle slides back |
| 17.4-19.9 | But here's what nobody told you, mama. | R1: the bottle hops forward, leans in, waves her closer |
| 19.9-22.0 | I never reached your scalp. | R2: cross-section, oil lands on the hair strand, skin below stays clean |
| 22.0-26.2 | I sat on your hair. I ran down your neck. I soaked your towel. | R3: oil running down her neck into the towel |
| 26.2-29.9 | It wasn't you. It was never you. | P1: tension to relief, the bottle pats her finger |
| 29.9-32.1 | It was the dropper. | P2: a dropper bulb in a spotlight, the drop falls and slides off a strand |
| 32.1-34.35 | Hair doesn't drink oil. Skin does. | P3: oil beads slide off hair, one lands on skin and is absorbed |
| 34.35-37.3 | So meet the one with hollow silicone tips. | C1 (reused): she opens the box, room warms to amber |
| 37.3-43.2 | Press them to your scalp, and I release right there, directly on the skin. | D1, D2, D3 (reused) |
| 43.2-53.0 | The first night, mama, I felt it. Oh. This is what it's supposed to feel like. | E1, E2 (reused), "oh" lands on the relief at about 47.7s |
| 53.0-58.4 | Not doing anything? I was never getting there. | M1: hook callback, warm mirror shot, Maya in the bonnet, the bottle shrugs |
| 58.4-61.8 | Now Sunday can stay on the calendar. | K1: gold ticks across a week, the bottle waves goodbye |
| 61.8-68.8 | The Nee-noo Kit. Free U.S. shipping. Thirty days to love it or send it back. | G2: dispenser and bonnet, offer card |
| 68.8-74.1 | Make tonight the easy one. | F2 (reused): Maya settled in bed, bonnet, dispenser in hand |

Cost: the song 13 credits, 15 new shots plus 4 retakes, 571 credits in all, about $2.86. Credits left: 503.7.

## 3. Same measurements as R10 section 3

| Measure | Reference | v1 | v2 |
|---|---|---|---|
| Runtime | 124.4s | 85.0s | 74.1s |
| Scenes | 34 (avg 3.66s) | 13 (avg 6.54s) | 22 (avg 3.37s) |
| Scene changes in first 30s | 9 | 4 | 10 |
| Hook length | 4.12s / 8 words | 8.22s / 9 words | 3.4s (the question) then the interrupt at 3.4s |
| First text on screen | frame 0 | 1.64s | frame 0 |
| Words / per second | 201 / 1.62 | 92 / 1.08 | 154 / 2.08 |
| Second person per 100 words | 9.5 | 1.1 | 10.4 |
| First person per 100 words | 4.0 | 9.8 | 5.8 |
| Pulse | steady, about 132 BPM | weak (0.24) | 113 BPM, 0.57 |
| Product on screen first | 54.3% | 0% | 46.4% |
| Brand first | 70.7% | 91.6% (end card only) | 84.5% (sung), card at 87.0% |
| Risk reversal | 80.1% | end card only | 87.9% sung, plus the end card |
| Cause / problem-mechanism block | 28.7% (36.9% with the reframe) | none | 33.9% |
| Solution mechanism block | 10.9% | 22% | 11.9% |

## 4. The 8-point hook test, v2

| # | Test | v2 |
|---|---|---|
| 1 | Text on screen in frame 0 | Yes, the question card |
| 2 | Hook is the avatar's own words about her pain | Yes ("hair oil not doing anything" is from her failed-solutions list, R10 section 6) |
| 3 | Names a specific shameful thing | Partial. Specific (oil that does nothing), but milder than "nipple hair". The towel and oil streak carry the embarrassment visually |
| 4 | High-arousal face within 2s | Yes, wide eyes at 0s, a flinch at about 1.5s |
| 5 | Pattern interrupt within 5s | Yes, 3.4s (a talking bottle) |
| 6 | Curiosity gap within 5s | Yes, "who is talking, and why was it never used?" |
| 7 | First cut at or before 5s | Yes, 3.4s |
| 8 | Avatar identifiable in 5s | Yes, "mama" at 4.6s, "baby" at 9.7s |
| | **Score** | **7 of 8, one partial** (v1: 0 of 8) |

## 5. Claims and compliance

- Mechanism claims only: oil on the hair does not reach the scalp, hair does not absorb oil, the tips release oil on
  the skin. No result claim (no hair growth, no shedding, no regrowth), no hormone or medical claim.
- "Thirty days to love it or send it back" matches the 30-day money-back guarantee on the PDP.
- The end card names the kit and $49.99. It shows the dispenser and the bonnet only, because the model kept drawing
  the oil with a dropper bulb, which contradicts "it was the dropper". The kit also includes 60ml oil (and the ebook
  is not mentioned anywhere). If you want the oil bottle in the end shot, add it as a real photo in the edit.
- The villain is the dropper method, not a competitor or a named product.

## 6. Risks and things to look at before spend

1. **Audio:** listen for the brand pronunciation, "U.S." and the price/guarantee lines.
2. **The dropper "villain" and our own oil:** the PDP flat-lay image shows our 60ml oil in a screw-cap bottle with no
   dropper, so the line is consistent. The talking bottle is drawn with a dropper bulb on purpose (the "old oil"), so
   do not let anyone swap it for the Ninu bottle in the edit.
3. **Pacing:** 2.08 words per second is faster than the reference (1.62). If the captions feel rushed, the song can be
   re-generated slower without changing the picture plan.
4. **Reused clips** (C1, D1-D3, E1, E2, F2, B1) were generated under a 85s plan and are cut shorter here, so check that
   the product close-ups still read at about 2 seconds each.
5. **The funnel gate stands** (R9b section 9): zero orders since Oct 26. Do not buy impressions for this until
   someone on an iPhone has bought through an ad link.

## 7. Test plan

One variable per round: keep the Ad C primary text, headline and description unchanged and run v2 against v1 as the
only difference, Facebook and Instagram placements only. Judge by the kill criteria in `ninu-kill-criteria.md`.
