# R28: Why Hook3_BuyerLanguage (R16) failed. A full-funnel feedback loop

Written 2026-11-06. Sources: Shopify analytics and orders (queried today), the Meta Ads Manager screenshot you sent, the ad logs in `ads/ninu-kill-criteria.md`, the store diagnosis `ads/ninu-r12-store-diagnosis-woa.md`, the winner dissection `ads/ninu-dissect-winner-adC.md`, the R16 copy file, the page history in git, a live page load test, and the master document (Drive ID `1aNoyCdvs485a16GD5ews1IwNTI-CNt0anToER2001cc`).

Where something is a measurement, it says so. Where it is my inference, it is marked **Inference**. Section 9 lists what I could not see.

---

## 0. Verdict (read this first)

1. **The R16 copy test did not fail because of the copy.** It failed to produce a readable test at all. The 241 visitors it sent bounced at **97.9%**, against 85% to 89% for the five ads that produced all 7 of your orders. They are almost all single-page visits, and they are almost all on Instagram (231 of 241). Nobody got far enough to meet the copy's belief work or the offer.
2. **Cheap clicks are not your friend in this account.** Every ad I have click prices for that sold had expensive clicks (£2.61 to £7.85). Every ad with clicks under £1 (R16 at £0.29, A3_CribHair £0.61, A2_Pillow £0.71, HookD £0.85) sold nothing. The pattern is consistent across at least 6 ads. Meta is finding a cheap pool of people who tap but do not buy.
3. **"Validated" was overstated.** The orange and purple ads were credited with 4 sales. **Two of those 4 (#1004 and #1005, $219.95) were PayPal-pending and have never been paid.** The real paid proof is 2 sales on 14 sessions from one ad, plus 3 single sales from three other ads. That is promising, not proven.
4. **Six of your seven orders came in the first week (Oct 22 to 26), on a different page, with different traffic.** After the Oct 27 rebuilds there has been 1 order in about 1,860 sessions. Page and traffic both changed at once, so nobody can say which one did it. That is the central measurement problem.
5. **Even with perfect traffic, the copy has real gaps against the master document.** It skips the discovery moment, the deeper desire, proof, and the "why $49.99 for something I can buy for less" objection. Those matter once traffic is fixed. They are the second job, not the first.
6. **The right next step is a diagnostic, not another creative.** Re-run the untouched Ad C control under identical settings and read the bounce rate first. That one test tells you whether you have a traffic problem, a page problem, or a copy problem. Section 8 has the plan.

---

## 1. What was measured

### 1.1 The failed ad

| Metric | Value | Source |
|---|---|---|
| Spend | £67.86 | Meta |
| Impressions / reach / frequency | 5,521 / 4,497 / 1.23 | Meta |
| CPM | £12.29 | Meta |
| Link clicks / link CTR / link CPC | 237 / 4.29% / £0.29 | Meta |
| Website purchases | 0 | Meta |
| Shopify sessions from this ad (utm_content 120251229985780342) | 241 (237 clicks, 241 sessions: nothing is lost before the page) | Shopify |
| Add-to-carts / checkouts / orders | 0 / 0 / 0 | Shopify |
| Bounce rate | **97.9%** | Shopify |
| Device | 238 mobile, 3 tablet | Shopify |
| Referrer | **231 Instagram**, 5 Facebook, 5 none | Shopify |

Statistics on 0 add-to-carts in 241 sessions:
- At your old social add-to-cart rate of 0.7%, you would expect 1.7. Seeing 0 happens about 1 time in 5 (18%). So this does **not** prove the ad is worse than before.
- At the 2.5% the test needed, you would expect 6. Seeing 0 happens about 1 time in 400 (0.25%). So this **does** show the copy did not lift the rate to 2.5%.
- The 95% upper bound on the true add-to-cart rate for this traffic is about 1.2%.

On Shopify's "average session duration" (1.2 seconds): bounced sessions count as zero duration, so that number is mostly a restatement of the bounce rate. I am not using it as evidence of how long people stayed.

### 1.2 The ads that did sell (Shopify, last 30 days)

| Ad ID | Sessions | Add-to-cart | Orders | Bounce | Avg duration | Note |
|---|---|---|---|---|---|---|
| 120250988064320342 | 28 | 1 | 1 ($66.98, #1001) | 85.7% | 27.8s | |
| 120251024608350342 | 20 | 1 | 1 ($49.99, #1002) | 85.0% | 32.5s | |
| 120251061111520342 | 14 | 2 | 2 ($99.98, #1003 and #1006) | 85.7% | 18.9s | Both paid |
| 120251061130930342 | 54 | 3 | 2 ($219.95, #1004 and #1005) | 88.9% | 17.8s | **Both PayPal-pending, never paid** |
| 120251135585830342 | 65 | 1 | 1 ($49.99, #1007) | 95.4% | 7.2s | Oct 30 |
| **Total** | **181** | **8** | **7** | | | 5 paid, 2 unpaid |

The two ad IDs with 4 orders between them (…61111520342 and …61130930342) match the 4 sales logged for Purple_Textincrease and Orange_Textincrease on Oct 25 and 26 (`ads/ninu-kill-criteria.md` sections 8 and 12). **Inference:** I cannot see which ID is which colour. The order data shows one ID had two paid orders and the other had two unpaid PayPal orders.

Traffic from these five ads, by referrer: Facebook 99 sessions (7 add-to-carts, 6 completed checkouts), Instagram 60 sessions (1 add-to-cart), no referrer 22 (0).

### 1.3 The ads that did not sell

| Ad ID | Sessions | Add-to-cart | Bounce | What it was |
|---|---|---|---|---|
| 120251120340920342 | 1,005 | 0 | 93.8% | The Oct 29 "junk-click" ad |
| 120251062019940342 | 269 | 0 | 90.7% | |
| **120251229985780342** | **241** | **0** | **97.9%** | **Hook3_BuyerLanguage (R16)** |
| 120251062091660342 | 100 | 0 | 89.0% | |
| 120251024825770342 | 90 | 0 | 94.4% | |
| 120251136725630342 | 48 | 0 | 95.8% | |

These ads sent **1,753 sessions** (Facebook 998, Instagram 735, 0 add-to-carts from any of it). So Facebook alone is not the cure: the same placement produced 0 from these ads and 7 add-to-carts from the buyer ads. **The ad itself, not the platform, is the variable.**

### 1.4 Click price against sales, across the whole account

Link CPC and purchases for ads in `ads/ninu-kill-criteria.md`, plus today's:

| Ad | Link CPC | Link clicks | Purchases |
|---|---|---|---|
| Orange_Textincrease (Oct 26) | £7.49 | 7 | 2 |
| Control hook, Ad C (Oct 25) | £4.22 | 21 | 1 |
| Copy 3-OG advertorial (killed) | £3.08 | 19 | 0 |
| Purple_Textincrease (Oct 26) | £2.61 | 16 | 2 |
| HookB | £1.80 | 18 | 0 |
| Hook3 (first run) | £1.09 | about 50 | 0 to 1 add-to-cart |
| HookD Social-Compare | £0.85 | 44 | 0 |
| A2_Pillow | £0.71 | 28 | 0 |
| A3_CribHair | £0.61 | 104 | 0 (1,588 "all clicks") |
| **Hook3_BuyerLanguage (R16)** | **£0.29** | **237** | **0** |

The ads that sold were the expensive ones. **Inference:** a high CPM means the auction judged those users valuable to other advertisers, which usually means people more likely to buy. A £12 CPM means Meta found a cheap pool that does not convert for you. Small samples, so this is a pattern and not a law. But the direction has held on every ad I can see.

The break-even arithmetic shows why cheap clicks can still be fine if they convert at all. Break-even CAC is £26.72.

| Link CPC | Session to order rate needed to break even |
|---|---|
| £0.29 | 1.1% |
| £0.53 | 2.0% |
| £1.09 | 4.1% |
| £2.61 | 9.8% |

So at £0.29 you only need about 1 order per 90 sessions. R16 delivered 0 per 241. The bar was low and the traffic still did not clear it.

### 1.5 Timeline: when the page changed and when the orders came

Page dates are git commit dates (UTC). **Inference:** your live page may lag the commits by hours or days, so treat the boundaries as approximate.

| Window | Page state | Sessions | Add-to-carts | Orders |
|---|---|---|---|---|
| Oct 22 to 26 | Earlier PDP (trust bar, mechanism row; commit 48d897c) | 405 | 15 (3.7%) | **6** |
| Oct 27 to 30 | Rebuilt: BOGO tiers, Manscaped-style structure, benefit bullets | 1,440 (981 on the junk day) | 12 | 1 |
| Oct 31 to Nov 6 | Mobile round 1, sale strike price, countdown, gifts, video, banner | 424 | 6 (4 are untagged) | 0 |

Bounce rate drifted up: 87% to 92% (Oct 22 to 27), 93% to 97% (Oct 29 to Nov 6). Page weight also rose: the Oct 31 diagnosis measured 2.4 MB and 91 requests. A load test today on an iPhone profile measured **7.4 MB and 128 requests**, of which about **4.4 MB is the product video loading twice** (2.3 MB and 2.0 MB range requests). First paint was about 2.0 seconds on a fast connection from my test environment. On a phone on mobile data it will be slower.

The 23 add-to-carts and 15 checkout starts on sessions with no ad tag (249 sessions, 82% bounce, 0 completed) are mostly you and your testers (`ads/ninu-r12-store-diagnosis-woa.md` already flagged "Direct, mostly you and testers"). Today's 4 add-to-carts are in that group. They are not evidence about any ad.

---

## 2. What changed since the orange and purple ads

| Element | Then (Oct 22 to 26, when the sales came) | Now (R16) | Effect on what we can conclude |
|---|---|---|---|
| Creative | Orange and purple gradient text posts, hook "ok i actually do my scalp oil EVERY night now" | Orange post, hook "baby up 3 times. wet hands, in bed. skipped my scalp oil again" | Same format family, different hook. Hook3 was always a pain hook, not the proven identity hook |
| Primary text | Ad C story, about 430 words | R16 body, 438 words, mechanism and price heavy | The one planned variable. But see 4.3: it is the part most clickers never read |
| Click price and delivery | CPM £115 to £314 on tiny impressions, CPC £2.61 to £7.85 | CPM £12, CPC £0.29 | A completely different pool of people |
| Click quality | 85% to 89% bounce, 18 to 32 seconds average for those who stayed | 97.9% bounce | Visitors engaged then, almost none engage now |
| Placement mix (buyer ads) | Facebook 62% of sessions | Instagram 96% | Instagram is the weaker placement even in the buyer ads (1 add-to-cart in 60 sessions against 7 in 99) |
| Page | Older, simpler PDP | Rebuilt three times, now with gifts, video, banner, countdown | Not separable from traffic |
| Page weight | Not measured then (2.4 MB on Oct 31) | 7.4 MB | A real cost on mobile data |
| Offer shown on page | $49.99, no strike price, kit plus tiers | $49.99 with struck $62.49, countdown, 4 free gifts | Untested: almost no one reaches the gift block |
| Learning data | 0 to 3 purchases in the pixel | 7 purchases, 2 unpaid | Too few conversions for Meta to find buyers, so it drifts to the cheapest taps |
| Account and season | Fresh account | Ad account payment declined mid-test; Q4 CPMs rising | Adds noise |
| How "validated" was judged | CTR and CPC and 4 logged sales | 2 of 4 sales were never paid | The proof was thinner than it looked |

**Biggest single difference:** the traffic. The page changed too, but the traffic changed far more: the share of visitors who did anything beyond landing fell from about 1 in 7 to about 1 in 50, and CPM fell from £115 to £314 down to £12 (roughly 10 to 25 times cheaper).

---

## 3. Funnel audit, stage by stage

| Stage | What I can see | Grade | Evidence |
|---|---|---|---|
| 1. Targeting and delivery | Broad, "Advantage+ audience", women 25 to 44, US, Advantage+ placements (from the R1 campaign export; I have not seen the R16 ad set). 96% of sessions came from Instagram | **Weak** | CPM £12, 96% Instagram, 98% bounce |
| 2. Creative stops the scroll | Link CTR 4.29%, above every earlier ad | **Strong at stopping, unknown at qualifying** | The image gets taps. The taps do not turn into engagement |
| 3. Message match, ad to page | Ad shows a 10pm wet-hands scene. The page opens with a red sale banner, a shipping bar, nav and a hero image headed "The scalp routine that actually sticks" | **Medium-weak** | The visitor who tapped on the scene does not see the scene again |
| 4. Landing page, first screen | Product pack hero image with garbled small label print, MELAO label on the oil, price is below the fold on mobile | **Weak** | Oct 31 diagnosis: "price and Add to basket appear about 1.4 screens down", partly fixed with the sticky bar |
| 5. Page weight and speed | 7.4 MB, video downloaded twice, 128 requests | **Weak on mobile data** | Load test |
| 6. Trust | Fake-looking named reviewers with AI split images, "Trusted by 10,000+", "Made in the USA", no real reviews, brand new store | **Weak, and the highest legal and trust risk on the page** | Flagged in R12 and still there |
| 7. Offer | $49.99, 4 free gifts, 30-day guarantee, 6 to 12 day shipping | **Unproven** | Section 6 |
| 8. Checkout | 75% of add-to-carts reach checkout, 78% of those finish | **Strong** | R12 numbers. Not the leak |
| 9. Payment | PayPal orders pending, never collected | **Broken for that gateway** | #1004 and #1005 |

The master document's own diagnostic rule: "Weak CTR with good impressions means hook and lead. Good clicks but weak conversion means the belief shift did not complete, strengthen the body. Add-to-cart but no purchase means risk, offer, urgency." R16 has strong CTR and no add-to-carts, so the rule points at the body. **But that rule assumes the clicks came from people reading the body.** Here 98% did not stay long enough to meet it. The rule cannot be applied until the traffic is real.

---

## 4. Copy and mechanism audit against the master document

### 4.1 The master document's checklist, applied to R16

The long-form system prompt (section 13 of the master doc) has a self-verification checklist. R16 against it:

| Master doc requirement | R16 | Verdict |
|---|---|---|
| Hook crystallises the deep desire and matches awareness level | The image states the pain ("skipped my scalp oil again"), not the desire | **Partial.** The reader must already oil her scalp to relate |
| First line of lead drops into her own recognisable moment | "I had the castor oil. I had the rosemary. I believed in the routine." | **Pass** |
| Emotion shown, not named | Wet hands, bottle at the back of the shelf, "start over Sunday" | **Pass** |
| Lead type matches awareness | Story lead for a solution-aware reader | **Pass if she is solution-aware.** Broad targeting makes most readers problem-aware or unaware |
| Failed solutions from the research ladder, weighted to awareness | Only dropper and fingers. The research's ladder (shampoos, vitamins, satin pillowcases, castor oil with shower cap, an $88 supplement) is mostly absent | **Fail** |
| Discovery device: the narrator finds, is not sold | "So I switched to a dispenser." No finding moment | **Fail** |
| UMP explains why the failed solutions failed; UMS connects to it | UMP: oil goes on the hair, hands and towel. UMS: hollow tips deliver on the scalp | **Pass.** The strongest part of R16 |
| All five belief buckets, including self-guilt and timing | Self-guilt: "It wasn't discipline. It was the routine." Timing: a sale date only | **Partial** |
| One honest limitation | "What it won't do" paragraph | **Pass** |
| Proof: real testimonials, results ladder, or credible authority | A first-person "I hadn't skipped a night". No third-party proof anywhere in the ad | **Weak.** Thin proof is allowed only if results stay modest, which they do. But there is nothing for a sceptic to check |
| Objection handler near the end | None | **Fail** |
| Crossroads close, both paths hit the deep desire | "Make tonight the easy one." No inaction path | **Partial** |
| Word count in range | 438. The master doc's default is 1,200 to 1,400 for an advertorial destination, and "straight-to-product-page hard closes may run longer" | **Short** for a hard close to a product page |

R16's own design doc said it "removes the absolute claim, moves the mechanism up, adds a disqualifier, reframes price and the guarantee." Those changes were sensible. They did not touch the three failing rows above, which are the ones that build belief in someone who is not yet sold.

### 4.2 The mechanism bridge: pain, cause, solution, desire

The master doc's structure is: the hook earns the "see more", the lead makes her feel understood, and the body builds belief that (a) she can be helped, (b) past failures were not her fault, and (c) this product is why it finally works. The mechanism has to be the thing that connects **what hurts** to **what she wants**.

Here is how the chain looks for Ninu, from the research in `ads/ninu-brand-context-for-organic-chat.md`:

| Link | What the avatar research says | R16 | Gap |
|---|---|---|---|
| **Pain** | "Pulling out handfuls of hair in the shower", the temples and hairline, photos, "humiliating" | Skipping a nightly routine, a messy towel | The deeper wound is missing |
| **Desire** | "I just want to feel like myself again." Mass desire: confidence and identity back after a baby | "The routine easier than the reason to quit" | The desire R16 pays off is a tidier habit, not the identity-level one |
| **Failed fixes** | Shampoos, vitamins, satin pillowcases, castor oil with a shower cap, an $88 supplement | "I had the castor oil. I had the rosemary." | Barely used, so she does not feel "this person tried what I tried" |
| **UMP (why fixes failed)** | Only one commenter mentions oiling and nobody mentions where the oil lands | Oil goes on hair, hands and towel, so little reaches the scalp | Good, plain and checkable |
| **UMS (why this works)** | | Hollow silicone tips press on the scalp along the part | Good, but the same mechanism is sold as a $5 applicator bottle |
| **Bridge to desire** | | "By the end of the first week I hadn't skipped a night" | **The break:** she is asked to believe that a nightly routine matters, without being shown why she would care. R16 never connects "oil on the scalp" to the thing she actually wants |

The break is the important finding. Ad C only got away with this because the people who saw it and bought were already convinced that scalp oiling matters (they were the solution-aware buyers). Cold broad traffic is not. R16 asks a reader who may not oil her scalp at all to become excited about oiling it more neatly. The hook filters for existing oilers, but the targeting does not.

You cannot make hair-regrowth or medical claims, and I would not change that. You can, however, name the emotional wound honestly in her own words (the shock of the shower drain, the dread of photos, "I want to feel like myself") without claiming a result. R1-A did a version of that ("the first thing I check every morning is my temples") and the master doc rewards "the emotional driver shown through a specific scene". Two cautions: keep it first person ("I", never "you" about her hair or body, which can trip Meta's personal-attributes policy), and do not describe shedding, thinning or any result. R1-A's "since the shedding started" is the kind of line to avoid. I have not checked Meta's current policy text, so verify before running it. Example of the missing link, written as structure only:

1. Pain scene (hers, not the product's): a moment of dread about how she looks.
2. What she tried, in her order: the shampoos, the vitamins, castor oil with a shower cap.
3. The discovery: she watches where the oil actually goes (the towel test) and sees it was never reaching the place she wanted.
4. The mechanism, in use.
5. The honest limit: it does not grow hair, it makes the routine she already believes in doable.
6. Proof she can check herself (the 30-night test, the towel test).

R23 and R25 in `ads/ninu-swipe-copy-paste-ready.md` already do this better than R16 does. Using one of those as the next copy test, not another R16 tweak, is more likely to build belief.

### 4.3 Why the R16 test could not have given a clean answer

1. **It changed the part most clickers never read.** On a native image ad, taps come from the image and the first line. The 438-word body only matters to people who expand it. The test varied the body, and the body varies almost none of the clicking behaviour. The R16 file already said "a win won't tell us which part did it" and "need roughly 300 to 400 clicks per ad". It got 237 clicks and no control.
2. **No control was run alongside it.** The master doc: "Never rewrite the control. The control is the untouched winner." Without Ad C running under identical conditions, 0 add-to-carts has no baseline. The page, the audience and the traffic all moved since Ad C converted.
3. **The page changed during the test.** The gifts, the video, the banner and the strike-through price all went live around Nov 5 and 6, while R16 was running.
4. **The kill rules were applied late.** The rule is £28 with 0 add-to-carts. The ad reached £67.86, which is 2.4 times that.

---

## 5. Creative audit

| Check | Finding |
|---|---|
| Native look | Pass. A plain orange text card reads like a person's post |
| Thumb-stop | Good. 4.29% link CTR is the best you have had |
| Information scent | **Weak.** Nothing in the image says "product". A curious scroller taps to find out what the post is about, then lands on a store |
| Audience qualification | **Weak.** "Skipped my scalp oil again" qualifies existing oilers, but the targeting is broad, so the audience is not qualified |
| Message match with the page | Weak. The scene (10pm, wet hands, baby up) is not echoed above the fold on the page |
| Style risk | You said the colour-post style had "insane CPMs and CPC" on Hook1_OG. It now gets £12 CPM. That swing is as likely to reflect where Meta chose to deliver as anything about the creative |

I would not call the creative bad. It is a good scroll-stopper pointing at the wrong crowd.

---

## 6. Offer audit

Judged against the master doc's offer rules (real tiers and prices only, per-use cost math if real, real gifts and deadlines only, no manufactured urgency) and against what a sceptical cold buyer would compare it to.

| Item | Assessment |
|---|---|
| Price vs perceived value | **Inference, check it yourself on Amazon or AliExpress:** a plain silicone scalp applicator bottle, a 60ml rosemary oil and a satin bonnet each sell for roughly $5 to $15 on marketplaces. The sum of parts is about $20 to $40. At $49.99 you are asking her to pay at or above the marketplace total for a kit from an unknown store. The "$62.49" anchor comes from your own store, so it carries no outside weight |
| The $62.49 anchor | Honest only if it was a price actually charged recently. Orders #1001 to #1007 were all at $49.99 or bundles, so the $62.49 has never been charged. **Risk:** a compare-at price that was never real is a misleading reference price (FTC and state rules, Shopify and Meta policy). Fix it before it becomes a complaint |
| Free gifts | Four items on the page (massager, pouch, guide, tracker). They raise perceived value on paper, but only those who scroll past the first screen see them. 98% of this ad's clicks did not. And two are digital, which buyers know are free to make |
| Shipping | "Free US shipping, 6 to 12 days." Amazon-trained US buyers expect 2 to 5. For a product she could get faster elsewhere, this is a real friction. Disclosing 6 to 12 days honestly is right. Hiding it is worse |
| Guarantee | 30 days, but the clock (from order or from delivery) is not stated. With 6 to 12 day shipping, "30 days from order" would leave her 18 to 24 days to try it. Decide and say so |
| Urgency | A real sale end date is legitimate, if you really change the price on Nov 11. Otherwise it is manufactured urgency, which the master doc prohibits |
| Proof | No real reviews. The page's named reviewer cards with AI split images are the single biggest trust liability on the page |
| Unit economics | Margin $34.74 per kit order at $49.99. The gift costs reduce it: at $4, $6 or $8 per order, you need roughly 13%, 21% or 30% more conversion to stand still |
| The discount question | The sale is unlikely to be what stopped add-to-carts, because a lower price rarely lowers add-to-cart rate. But it is also not enough on its own to rescue conversion, and a never-charged strike price may hurt trust |

The master doc's rule from the store diagnosis still holds: by its own rule the offer is the **last** lever, after the belief shift. Do not change the offer again until the traffic is fixed, or you will not know what moved.

---

## 7. Hypotheses, ranked, with what would settle each

| # | Hypothesis | Confidence | Evidence for | Evidence against | What settles it |
|---|---|---|---|---|---|
| H1 | The ad delivers to a cheap, low-intent pool (Instagram heavy, accidental or curiosity taps) | **High** that clicks are poor. Cause not confirmed | 98% bounce. £0.29 CPC. 96% Instagram. Every sub-£1 ad sold 0 | Facebook sessions from non-buyer ads also converted 0 | Meta placement, age and region breakdown. Run the control on identical settings |
| H2 | Awareness mismatch: the ad speaks to existing scalp-oilers and the targeting is broad | **Medium-high** | The hook and copy assume she already oils her scalp. Broad Adv+ audience | Cannot see the R16 ad set | Narrow targeting or a pre-qualifying hook. Compare bounce |
| H3 | The page lost conversion after the Oct 27 rebuilds | **Medium** | 6 of 7 orders on the old page. Bounce rose. Page weight tripled | Traffic changed at the same time. Oct 22 to 26 ads also had very different CPMs | Run the same ad to the old page version and the new, same hour |
| H4 | Copy gaps stop belief forming (no discovery, desire, proof or price reason) | **Medium** once traffic is real | Master doc audit in 4.1 and 4.2 | Cannot test on 98% bounce traffic | A copy test on good traffic, after the control run |
| H5 | Trust: fake-looking reviews, "10,000+", no real proof | **Medium** | R12 flagged it. Still on the page | No direct measurement | Remove and compare. Install session recordings |
| H6 | The offer (price, shipping, strike price) is not compelling | **Low-medium, unproven** | Section 6 | The gifts have effectively never been seen | After H1 to H3 are fixed |
| H7 | The sale or strike price itself suppressed add-to-carts | **Low** | Timing coincidence | A lower price rarely lowers add-to-cart rate | Not worth testing separately |
| H8 | Measurement: unpaid PayPal orders and own sessions inflated the earlier "wins" | **High that it distorted the read** | 2 of 4 colour-ad sales unpaid. 249 untagged sessions | | Already confirmed from data |

Most likely combined story (**Inference**): the early orange and purple sales came from a narrow, expensive, Facebook-heavy slice of Meta's delivery during its learning phase. As Meta had too little conversion data to hold that slice, delivery drifted toward cheaper, Instagram-heavy inventory, whose clicks look great on CTR and CPC and do not convert. Meanwhile the page got heavier and more complicated. The copy then changed on top, so every variable moved at once.

---

## 8. Plan: the next 10 days

Budget at about £40 a day total, with checkpoints.

### Phase 0: today, £0
1. **Pause Hook3_BuyerLanguage.** It has passed the £42 with 0 checkouts and £54 with 0 purchases lines.
2. **Confirm the other junk ads are off:** `…120340920342` (1,005 sessions), `…062019940342`, `…062091660342`, `…024825770342`, `…136725630342`.
3. **Pull Meta breakdowns for the R16 ad:** by placement, by age and gender, by device and by region. Check the optimisation event (it must be Purchase), the attribution setting, and whether Advantage+ placements and Advantage+ audience are on.
4. **Collect real order data:** resolve #1004 and #1005. They are $219.95 of your gross and have not been paid.
5. **Add session recordings** (a free tool such as Microsoft Clarity is one option). Watching 20 recordings of this ad's visitors will settle in an hour what the numbers cannot. Your call on adding a third-party script.

### Phase 1: the decisive diagnostic, 3 days, up to about £45
Run the **untouched Ad C control** (the original orange body, "ok i actually do my scalp oil EVERY night now") under identical settings: same ad set, same audience, same placements, same page. Do not change the page during this. Read, in this order:

| Read | If it looks like R16 (98% bounce, 0 add-to-cart) | If it looks like the old buyer ads (85% to 90% bounce, add-to-carts) |
|---|---|---|
| Bounce rate by ad | The traffic is the problem, not the copy | The copy or hook is the difference. R16 hurt |
| Add-to-cart per 100 sessions | Fix delivery first (Phase 2) | Return to Ad C and test one change at a time |

Checkpoints: £14 with 0 link clicks, £28 with 0 add-to-carts, £42 with 0 checkouts, £54 with 0 purchases. Do not let it drift past £28 without a result this time.

### Phase 2: fix delivery if the control also bounces
- Switch to **Facebook feed only** placements (or Facebook plus Instagram feed, no Reels, Stories or Explore), and turn off Advantage+ audience for one test cell.
- Use a narrower, more qualified audience or a pre-qualifying hook ("if your scalp oil is at the back of the shelf") so only existing oilers click.
- Read bounce rate and add-to-cart per 100 sessions at 100 sessions, before any spend past £30.

### Phase 3: page parity test, only if delivery is fixed
- Put the **Oct 26 page** (commit `48d897c`, `git show 48d897c:pdp/ninu-pdp.html`) next to the current one as separate pages and send equal traffic to each.
- This needs at least 150 to 200 sessions per page to see anything at a 2% to 3% add-to-cart rate. At £0.50 to £1 a click, that is £75 to £200 per side. Not affordable this week, so only do it if Phase 1 points at the page.

### Phase 4: copy, only after Phases 1 and 2 give good traffic
- Test **one** new long-form body built on the mechanism bridge in 4.2 (R23 or R25 are the closest). Keep the image fixed.
- Expect the first real read at about 300 clicks of good traffic.

### Fix now, regardless of the tests (no money needed)
1. Remove the named reviewer cards, "Trusted by 10,000+", and any claim you cannot prove.
2. Fix the compare-at price: either charge $62.49 for a real period first or remove the strike price.
3. Decide and state when the 30 days starts.
4. Upload the lighter 691 KB product video (`pdp/gift-assets/ninu-in-use-720p-lite.mp4`) and set it to load after the first screen.
5. Resolve the MELAO label question.

---

## 9. What I could not see (so treat the conclusions as conditional)

- The **R16 ad set's settings**: placements, audience, optimisation event, attribution window, budget and schedule. I only saw the ad-level screenshot.
- **Meta breakdowns** (placement, age, region). Everything about Instagram comes from Shopify referrers, not Meta.
- **Whether the control was ever run.** I found no control for R16 in your data.
- **When you pasted each page version into Shopify.** I used git commit dates.
- **Which ID is orange and which is purple.** The mapping of the two 4-order IDs is inferred.
- **Real visitor behaviour.** I have no recordings or heatmaps.
- **A physical sample** of the product, which matters for the mechanism claims ("nothing runs, nothing drips").
- **Price comparisons** are my estimates and need a quick check against marketplace listings.

---

## 10. Questions that would sharpen this

1. In Ads Manager, open the R16 ad set and tell me: placements (automatic or manual), whether Advantage+ audience is on, the optimisation event, and the daily budget.
2. In Breakdown, by placement: how many of the 237 clicks were Instagram Stories or Reels?
3. Did you run an Ad C control alongside R16? If so, what did it show?
4. When did you paste the new page into Shopify, and was it before or after R16 launched?
5. Has anyone other than you and testers added to cart on the new page?

---

## Appendix: queries and numbers

- Funnel by ad and by day: Shopify `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, bounce_rate GROUP BY utm_content` and `TIMESERIES day`, run Nov 6.
- Orders by ad: `FROM sales SHOW orders, gross_sales GROUP BY order_utm_content` (5 IDs, 7 orders, $486.89 gross, $266.94 paid).
- Statistics: P(0 add-to-carts in 241 sessions) at 0.7% = e^(-1.69) = 18%, at 2.5% = e^(-6.0) = 0.25%. Rule of three upper bound 3/241 = 1.2%.
- Page load test: iPhone 13 profile, `tryninu.store/products/the-ninu-kit`, 128 requests, 7.4 MB, first contentful paint about 2.0 seconds on a fast datacenter connection (so mobile will be slower).
- Pages by commit: `48d897c` (Oct 26), `ab5f324` (Oct 27 BOGO tiers), `a95cb9d` (Oct 28 Manscaped rebuild), `60449a2` and `f1fb967` (Oct 31 mobile round 1 and sale), `bf46e49` (Nov 4 gifts).
