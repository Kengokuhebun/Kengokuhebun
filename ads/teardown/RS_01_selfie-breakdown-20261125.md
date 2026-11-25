# Why is RS_01_selfie getting add-to-carts? — breakdown, 2026-11-25

Applying the master document's "Dissect the Winner" discipline (beat-by-beat, ranked drivers, every claim tagged PROVEN or HYPOTHESIS, never present a guess as a finding) to the actual question asked, since that protocol is built for rewriting winning copy, not full-funnel friction — the rigor transfers, the template doesn't.

## The fixed facts (controlled across this comparison)

All 8 original Ritual Swipe ads, including RS_01_selfie, share: the same ad set (same targeting, same audience pool), the same landing page, the same offer, the same CTA (SHOP_NOW), the same pixel. **Anything that differs between RS_01's performance and its siblings' cannot be the page, the offer, or the targeting — those are identical. It has to be the ad itself: image, copy, or headline.** This is the first and most important logical move, and it's PROVEN by construction, not a hypothesis.

## RS_01_selfie's exact creative (verbatim, pulled from the live ad)

- **Image**: vertical selfie-style photo, a woman in a kitchen holding the glowing board up to camera, two white text pills baked into the image: "Plug it in. Hand over the markers. That's the whole setup." (top) and "Buy 2 get 1 free right now." (bottom-right).
- **Primary text**: "My 5-year-old asks for this by name. Plug it in, hand him the markers — that's the whole setup."
- **Headline**: "The toy that doesn't go in the garage"
- **Description**: "Buy 2, Get 1 FREE + free tracing book. Ends Cyber Monday."

## Ranked drivers for "why RS_01, not its siblings" (pre-click only — the page is identical for all of them)

1. **The ad shows the offer on the thumbnail itself, before any click.** [PROVEN as a factual difference, HYPOTHESIS as a cause] RS_01's image carries the "Buy 2 get 1 free right now" pill. `RS_02_bin` and `RS_03_offerposter` through `RS_08` either carry no offer cue or carry it as a designed graphic element rather than a lived-in moment. Someone who clicks RS_01 already knows the offer before they land — the PDP's job becomes confirmation, not a first pitch. This is the master document's own awareness-level principle: the ad should move the reader toward product-aware before the click; a page can't out-persuade an ad that already told the reader what to expect.
2. **The headline targets the account's single most-proven emotional driver.** [PROVEN as a pattern, HYPOTHESIS as the specific cause here] "The toy that doesn't go in the garage" is the same underlying fear — money already wasted on abandoned toys — that drives the entire "ledger" copy family (gift-ledger, dinner-ledger, shower-ledger), which is independently the most-favored content this account has ever run by CTR and spend. RS_01 hits that nerve in four words, on its own, without needing the ledger's 800-word story to do it.
3. **A real, identifiable person demonstrating the product.** [HYPOTHESIS] Builds the "someone like me already uses this" signal. Can't be proven from this data alone — RS_04_reframe and RS_05_checklist also show the product clearly (satisfying the audit's own U1 native rule) without converting, so visibility of the product is necessary but not sufficient on its own.
4. **High-curiosity, low-offer-signal images get clicks without intent.** [PROVEN as a pattern within this account's own data] `RS_02_bin` has this campaign's best CTR (14.9%) and cheapest CPM (£10.7) — better than RS_01 on every top-funnel metric — and zero ATC. The gift-ledger/shower-ledger family shows the exact same shape at far larger scale: ~2,655 clicks, 2 ATC, 0 purchases. Cheap clicks and purchase intent are not the same signal, and this account now has two independent, consistent examples proving it.

## The confound I need to own

The native re-expression test (`N1_proven-native`) was built to isolate exactly one variable — image format, native vs. designed — holding the hook constant. It didn't fully do that: **in removing the on-image overlay text to make it "native," it also removed the offer pill** — which driver #1 above says may be doing real work. N1 has changed two things against RS_01 (format *and* offer-visibility), not one, so if N1 under- or out-performs RS_01, it won't be possible to say which of the two changes caused it. This is a real design flaw in that test, not just caution — it should be corrected in the next build, not treated as acceptable noise.

## Why does 4 of 5 add-to-carts still not become a purchase? (post-click, page-side — the same question applies regardless of which ad they arrived from)

This is a different question from the one above, and the data is thinner (n=5 ATC total). Ranked, same discipline:

1. **The fabricated testimonials were live on the page for the entire window these 5 add-to-carts happened in.** [PROVEN that this was live; HYPOTHESIS that it caused the drop] This is the only candidate on this list that is already confirmed true (not inferred), already a known rule violation independent of this analysis, and already has a fix sitting ready, unpaid, unexecuted.
2. **The cart drawer shows 4 separate line items for what the buyer thinks of as one purchase** (paid board x2, free board x1, free tracing book, each its own row) — seen directly in the NZ checkout test screenshots. [OBSERVED that this is the UI; HYPOTHESIS that it confuses anyone at the moment of commitment]
3. **The pen-pack upsell prompt sits inside the cart drawer, one more decision right before checkout.** [OBSERVED; HYPOTHESIS as friction] Order #1002 took this upsell, so it isn't pure friction for everyone — but an extra decision point at the commitment moment is a known abandonment lever in general.
4. **No custom domain** — raised last turn. [HYPOTHESIS, unresolved either way] Real but unprovable from 3 total initiated checkouts.
5. **Ordinary cart abandonment with no specific cause.** [always possible, can't be ruled out] Baseline behavior, not a finding.

Items 2-5 cannot be told apart from each other with 5 data points. Item 1 is the only one that's already proven true and free to fix — which is why it keeps surfacing as the top recommendation across several different angles of this analysis, not because I'm repeating myself, but because it's the one thing on every list.

## What this changes about the plan

- **Don't read N1-N4 vs RS_01 as a clean format test yet.** Fix the confound first: the next native-format ad should keep a visible offer cue (even a small one, native-styled — e.g. a handwritten-looking price tag in frame, not a designed pill) so format is the only thing that moves.
- **The "ledger family converts poorly" finding from last turn and "RS_02_bin converts poorly despite great CTR" are the same phenomenon, now proven twice in this account's own data**, independent of copy length or image style: cheap clicks and buying intent are different things here, consistently.
- **Push the testimonial fix live.** It's the only item on the post-click list that's already proven true rather than guessed, and it's free.
