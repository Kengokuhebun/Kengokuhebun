# R15: The TryVera "Overflow" rescue story, rebuilt for Ninu (structure only, no health claims)

Source analyses: `ad-spec-tryvera-overflow-story.md` (this ad), `ad-spec-emmafy-gofree-disney-story.md`, `ad-spec-emmafy-quilty-story.md`.
Earlier rebuilds: `ninu-r13-static-native-from-quilty.md` and `ninu-r14-native-from-gofree.md`. Your inputs: the winning Ad C body (`ninu-r8-hook-only.md`),
the R2 extraction, the Hook D text (`creatives/build-r2-adC-variants.js`), the R1 Ad B copy (`ninu-r1-long-form.md`).

## 1. Read this first: what in this ad cannot be carried over

The structure is reusable. A large part of its content is not. The spec records these claims (Step 7); none of them can go into a Ninu ad:

| In the TryVera ad | Why Ninu cannot reuse it |
|---|---|
| A quoted study: "152% ... within 5 days" [¶35], "over 60% of postpartum women are severely deficient" [¶54] | The copy names no author, journal, year or title, so I can't verify it, and you have no study. An invented statistic is a false claim. |
| A medical cause: "severe nutritional depletion" [¶47], "one of the leading causes of low milk supply" [¶125] | Ninu's guardrail since R1 is behaviour and delivery claims only. |
| Symptoms resolved: "My hair stopped falling out in the shower. The rash on my hands disappeared." [¶107] | A health outcome. Your Ad C converts without any hair or health claim. |
| A doctor's quote about a child's health [¶112] | No real doctor said anything. |
| A diagnosis aimed at the reader: "You don't have a low supply gene" [¶139], "You're depleted" [¶134] | Telling the reader something about her body is the kind of line ad platforms restrict. I'm describing the general policy from memory, so check Meta's current wording. |
| Quoted people who doubted her [¶22-24] | Invented people. |

I would not run that ad's claims, and the rebuild carries over none of them. I am not saying the product is or isn't what it claims. I can't tell. I'm saying the claims need substantiation Ninu does not have.

## 2. What this ad adds to the other two, and what all four winners share

| Measure | Ad C (yours) | Quilty | GoFree | TryVera |
|---|---|---|---|---|
| Words | 430 | 1,103 | 645 | 2,005 |
| Paragraphs | 14 | 16 | 23 | 153 |
| Average words per sentence | 9.0 | 12.5 | 8.5 | 7.8 |
| Product named at | 54.7% ("dispenser") | 47.5% | 29.0% | 50.6% (brand), 26.0% (moringa) |
| Price in the copy | yes, 87.2% | no | no | no (other products' $87 only) |
| Mechanism explained | yes ("Hair doesn't absorb oil. Skin does.") | yes (shape) | no | yes (depletion) |
| A third party quoted | none | Kate (a text) | the husband ×4 | pediatrician, mother-in-law, mother |
| Numbers / statistics | counts only | counts | counts, clock times | counts, clock times, "152%", "60%" |
| Devices present (of 35) | not run | 24 | 19 | 29 |
| Link | CTA button | URL, end | URL, end | "I left a link below where I got mine." |

**Shared across all four (as measured):**
1. A first-person narrator who is the avatar's peer.
2. A villain that is the common set-up (Ad C: the dropper and towel routine; Quilty: flowers; GoFree: other bags; TryVera: supplements).
3. Specific numbers and times in the story.
4. A line that takes the blame off the reader: Ad C "Not because I'd become more disciplined. Because the tool I'd been using was wrong"; Quilty [¶3] "every one of those arrangements was love. People are good."; GoFree [¶6] "that is the law"; TryVera [¶74-75] "I wasn't broken. I was just empty."
5. The product named late, after the problem is established (47% to 55% of the way through).
6. A closing line that points to a link or button.

**What TryVera adds:** the longest and most emotional version of the same shape as your Ad C. Compare the failed-solutions beats: Ad C spends 40% of its words on them (`ninu-dissect-winner-adC.md`), TryVera's effort, shortfall and judgment beats are 14.0% plus a 3.0% desire beat, and its results beats are 25.3%. It adds a dated breaking point, a "nobody told me" anger beat, an address to the reader on the same floor, analogies, and a reframe line, "I wasn't broken. I was just empty."

That reframe line is the same move as your winning desire, "I was never the problem. The method was." This ad is the strongest confirmation in the set that the move works as a structure.

## 3. Slot map: TryVera → Ninu

| Spec slot | TryVera | Ninu (your winning elements) |
|---|---|---|
| Command hook | "Please STOP buying lactation supplements." | "Please STOP trying to be more consistent with your scalp oil." (the villain is the discipline advice; no product is attacked) |
| Concession and promise | "I know that sounds crazy" / "Let me explain." | same device |
| Stake | the growth-curve sentence | "It was 10pm on a Sunday when I finally gave up." (10pm and Sunday are from Ad C) |
| Rock-bottom scene | the bathroom floor, pump running | "I was in bed. Wet hands. Again." |
| Effort ladder | pumping, cookies, tea | "I had the castor oil. I had the rosemary." + Ad C's four nights, three wake-ups, bottle at the back of the shelf, "start over Sunday" |
| Others succeeding | mom groups with overflowing freezers | Hook D: "every mom in my fb group did her nightly oil for six months straight. I made it eleven nights." |
| Judgment | mother-in-law, pediatrician, mother | **dropped.** Self-judgment only: "I started believing it was me." |
| Desire | "the breastfeeding relationship I'd dreamed about" | "I just wanted to feel like myself again." (the avatar's own phrase, R10) |
| Discovery | a study in Manila | **dropped.** "Then I found a dispenser with hollow silicone tips." |
| Mechanism of the problem | depletion | "It was about where the oil was going." + Ad C: "Hair doesn't absorb oil. Skin does." |
| Analogy | gas pedal, printer, horse | "Like pouring water on a plant's leaves and wondering why the soil stayed dry." |
| Mechanism of the solution | moringa supplies raw materials | Ad C's tips paragraph, unchanged |
| Reframe | "I wasn't broken. I was just empty." | "I wasn't undisciplined. I was just using the wrong tool." (and Ad C's "the tool I'd been using was wrong") |
| Results ladder | day 3, day 5, week 2, ounces | Ad C's own: first night "oh", end of the first week, a few weeks in |
| Beyond the main result | energy, hair, rash | **behaviour only:** "I stopped dreading 10pm. The bottle came off the back of the shelf." |
| Anger | "nobody told me the truth" | R1 Ad B's own line: "Nobody, not once, ever asked me how I was applying the oil I already believed in." |
| Address to the reader | "from their own bathroom floor" | "from bed, with wet hands, about to tell herself Sunday" |
| Permission | "it's not you" | "It's not you. You're not undisciplined." |
| Offer | Not present | Ad C's offer paragraph and the Early Black Friday line (a deliberate departure) |
| Link line | "I left a link below where I got mine." | same line, with Meta's CTA button as the link |

## 4. The long-form primary text (725 words)

In the TryVera beat order, 48 paragraphs. 44 of 89 sentences (52% of the words) are verbatim from your Ad C, your R1 Ad B and your Hook D; the other 45 are connective lines.
No em dashes, no question marks, no exclamation marks, no claim about hair, health or results beyond what Ad C already says.

```
Please STOP trying to be more consistent with your scalp oil. I know that sounds crazy, but every time you set a reminder, buy another bottle, or promise yourself Sunday, you're ignoring what's REALLY making you skip. Let me explain.

It was 10pm on a Sunday when I finally gave up.

I was in bed. Wet hands. Again.

The baby had been up three times.

The bottle was at the back of the shelf, behind the other bottles.

And I was lying there thinking: I can't even do this one thing for myself.

I had the castor oil. I had the rosemary. I believed in the routine. I just couldn't make myself do it consistently.

I'd do it four nights in a row and then the baby would be up three times and I'd get into bed with wet hands and just not do it.

Then I'd skip a second night. The bottle would migrate to the back of the shelf and I'd tell myself I'd start over Sunday.

I never started over Sunday.

Every. Single. Sunday.

My routine was annoying. Oil on my fingers before I touched anything else. Running down my neck. Soaking into the towel I'd wrapped around my shoulders to protect my shirt.

By the time I finished one section I was already thinking about the cleanup.

It stopped feeling like self-care and started feeling like a chore.

A chore at 10pm after a full day with a baby is a chore that gets skipped.

Meanwhile every mom in my fb group did her nightly oil for six months straight.

I made it eleven nights.

I started believing it was me. That I was just one of those people who can't stick to anything.

But I didn't want to stop.

I just wanted to feel like myself again. The scalp oil was the one thing I was doing for me, and it was the one thing I kept skipping.

Then I found a dispenser with hollow silicone tips. I almost scrolled past it.

It wasn't about discipline. Or motivation. Or wanting it enough.

It was about where the oil was going.

Turns out I'd been putting it in the wrong place. Hair doesn't absorb oil. Skin does. Nights of working it down the strands, and almost none of it reached my scalp.

Like pouring water on a plant's leaves and wondering why the soil stayed dry.

That's why the towel was always wet and the routine was always a chore.

You press the tips against the scalp along the part and the oil releases right there, directly on the skin. Nothing runs. Nothing drips. Clear chamber, 1 to 4ml markings. One hand. Two minutes. Works with the oil I already had.

I wasn't undisciplined.

I was just using the wrong tool.

I ordered the Ninu Kit that night.

The first night I used it I thought: oh. This is what it's supposed to feel like.

No towel. No wet hands. No cleanup.

By the end of the first week I hadn't skipped a night. That had never happened.

A few weeks in the routine was automatic, same as washing my face. Not because I'd become more disciplined. Because the tool I'd been using was wrong and this one isn't.

I never started over Sunday. This time I didn't have to.

But it wasn't just the routine.

I stopped dreading 10pm. The bottle came off the back of the shelf.

I felt like myself again.

And what makes me a little angry now is that nobody told me.

Everyone said do it every night.

Nobody, not once, ever asked me how I was applying the oil I already believed in.

I'm sharing this because I know someone is reading this right now from bed, with wet hands, about to tell herself Sunday.

It's not you. You're not undisciplined. You don't need a better reminder.

The habit was always there. The routine just needed to be easier than the reason to quit.

The Ninu Kit comes with the dispenser, 60ml scalp oil, and a satin bonnet for $49.99. Free US shipping and a 30-day money-back guarantee.

Early Black Friday price: $49.99 until Nov 10. It goes to $62.49 on Nov 11.

Make tonight the easy one. Try the Ninu Kit risk-free for 30 days.

I left a link below where I got mine.
```

**Headline / description / CTA** (keep the control's): "Your messy oil routine's worst nightmare" / "Free US shipping · 30-day guarantee" / Shop Now.

### Measurements against the reference

| Measure | TryVera | Ninu copy |
|---|---|---|
| Words | 2,005 | 725 |
| Paragraphs | 153 | 48 |
| Product named | 50.6% | 45.1% ("a dispenser with hollow silicone tips"); the brand "Ninu" at 64.6% |
| Price / guarantee in the copy | Not present | 93.7% / 94.8% (from Ad C) |
| Reframe line | 50.1% | 62.8% |
| "Nobody told me" beat | 80.5% | 82.3% |
| Permission "it's not you" | 98.2% | 87.6% |

It is not padded to the reference's length. The reference's extra length is the study, the symptoms, the numbered results and the doctor's quote. None of that exists for Ninu without invention.

## 5. Lines to check before you run it

| Line | Check |
|---|---|
| "I ordered the Ninu Kit that night." | a made-up chronology; fine as brand voice, not as a verified customer's account |
| "I almost scrolled past it." | a feeling line, new |
| "I stopped dreading 10pm. The bottle came off the back of the shelf." | behaviour, new; true only if that is how you or a tester use it |
| "I felt like myself again." | a feeling, from the avatar's own phrase (R10); not a result claim |
| "Like pouring water on a plant's leaves and wondering why the soil stayed dry." | an analogy about where the oil lands, not about hair or scalp health; keep it that way |
| "That's why the towel was always wet and the routine was always a chore." | follows Ad C's "Soaking into the towel" |
| Hook D lines | your own earlier copy (the Hook D ad had the most link clicks in that test, 44, at a £0.85 link CPC, and no purchase) |

Standing note: this is a first-person brand-voice story, not a verified testimonial.

## 6. The native image (the TryVera one, and the Ninu version)

**What the original shows (from the image spec):** a plain countertop photo of containers of a white liquid with measurement marks and a Dr Pepper can in the middle. There is no product, no person, no caption and no claim in it. A soda can sits in the middle of the row of containers.

Compared with the other two winners' images:

| | Quilty (you only described the copy) | GoFree | TryVera |
|---|---|---|---|
| Image | not supplied | candid photo, product large and centred, a child's hand in hers | candid countertop photo, product not in frame, no people |
| Product in frame | n/a | yes | **no** |
| People in frame | n/a | yes (from behind) | **no** |
| Text overlay | n/a | none | none |

So you now have a pair of winners that disagree on whether the product is in the picture. That is a test, not a rule.

**The Ninu equivalent (product out):** the old routine's evidence, a real phone photo.
- A dark-coloured towel or pillowcase from a real session with a dropper, with the oil stain visible, on a counter or tub edge next to something with a known size (a soda can, a card, a coin), with the bottle that sits at the back of the shelf.
- It must be a real stain from a real session. Do not fake or exaggerate it (the master doc's rule: "Accurate, not fabricated").
- Phone camera, natural light, slightly imperfect, no caption, no overlay, no brand. Straight on at counter height, objects in a row, one object at the centre.
- Export 4:5 (1080 × 1350) and 9:16 (1080 × 1920) with the objects between 14% and 80% of the height for the 9:16.

A generated stand-in is possible, but a stain made by a generator is an invented result, so I would shoot it. If you still want one, a prompt for an image model:

```
A candid, slightly imperfect iPhone photo of a bathroom counter in warm evening light. Centred: a grey bath towel folded over the edge of the counter with a dark glossy patch of golden-brown oil soaked into the cotton near one corner, next to a plain brown glass dropper bottle with a black rubber bulb and a standard 12 oz soda can for scale. Soft background of a bathroom mirror and a shelf. A little grain, handheld, no retouching. Portrait 4:5. No people, no hands, no text on any object, no logos, no watermark.
```

Label it as illustrative if you use it, and do not present it as a customer's photo.

## 7. Test order (updated: all five assets, one change per round)

| Round | Image | Copy | What it tests |
|---|---|---|---|
| A | Notes 1:1 (R13, ready) vs your current hook-only image | Ad C unchanged | a product-out native vs your control |
| B | bedside photo (R14, product in) vs the winner of A | Ad C unchanged | product in or out |
| C | the oil-on-towel photo (this doc, product out, evidence) vs the winner of B | Ad C unchanged | an evidence photo vs a text note |
| D | the winner of A to C | R13 (664 words) vs R14 (450 words) vs R15 (725 words) vs Ad C (430 words) | which long-form structure |
| E | the winner of A to C | the winner of D, with and without the price paragraph | whether a link-only close helps |

You are thin on budget, so run A first (it costs nothing to build). Stop a round at the usual checkpoints (£14/0 link clicks, £28/0 add-to-cart, £42/0 checkout, £54/0 purchases), FB and Instagram placements only, and about 1,000 impressions before comparing.

## 8. Pre-launch gates

- First-person story: brand voice, not a verified testimonial.
- "$49.99 until Nov 10, then $62.49" requires the price to actually change on Nov 11.
- No claim about hair, health or results beyond Ad C. No study, statistic or doctor.
- Ebook left out. No URL in the text.
- Funnel gate from `ninu-r12-store-diagnosis-woa.md`.
