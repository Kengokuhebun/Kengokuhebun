# Ninu store: full status, problems, history and what has been tried (as of 2026-11-10, 14:00 UTC)

Purpose: give any AI or person the whole picture of the Ninu store in one file. Every number below was pulled from Shopify or Meta on 2026-11-10 unless it says otherwise. Items marked **UNVERIFIED** were said in earlier sessions but not checked today.

---

## 0. How to work with this owner (read first)

- Short answers. One best version, ready to paste. A recommendation, not a menu.
- Honest claims only: no fake urgency, fake scarcity, fake reviews, invented customers, or hair-regrowth, shedding or medical claims. Offer the true version of any tactic that would cross that line.
- New copy: no em dashes, no exclamation marks. Say "oiling my scalp", not "doing my scalp oil".
- Image prompts: the oil is pale golden-yellow and clear (rosemary-style), never dark.
- Do not publish, spend money, message customers or change the store without being asked. Never print or reuse API keys.
- The owner pastes code into Shopify themselves and has had trouble with large pastes (see problem P7). Prefer short, exact instructions.
- The owner follows a mentor (Aaron) and a master document ("Aarreign's Master Document", Google Drive ID `1aNoyCdvs485a16GD5ews1IwNTI-CNt0anToER2001cc`). Key rules: one variable per test, hooks from three doors (pain, identity, curiosity or mechanism), native-looking images, real urgency only.

---

## 1. Snapshot

| Item | Value |
|---|---|
| Brand | Ninu ("Nee-noo"), postpartum scalp-oil dispenser |
| Store | https://tryninu.store (Shopify Basic, `fpgc15-gt.myshopify.com`, prices in USD) |
| Owner | UK-based, sells to the US (94% of sessions are US, about 88% mobile), pays for Meta ads in GBP |
| Live since | First sessions about Oct 19, 2026. First order Oct 22 |
| Orders, all time | 7 orders, gross $486.89. **5 paid ($266.94). 2 PayPal orders expired unpaid ($219.95)** |
| Last order | **#1007 on Oct 30. No orders in the 11 days since** |
| Ninu ad spend, all time | **£1,813.54** (campaign R1_Ninu) |
| Real cost per paid order | about £363 (£1,813.54 / 5 paid orders) against a break-even of about £26.72 |
| Cash | Thin. Spend has been held to roughly £20 to £75 a day for tests |
| Ads running now | 2 ads, £60 a day in total (see section 8) |

---

## 2. Brand history and timeline

**Before Ninu (same Meta ad account, dates not checked):**
- **Lumen**: 3 campaigns (LUMEN_R1_ABO_ColdWomen, R2_Lumen_Test_Campaign, R3_Lumen), £1,824.71 spent, 49 add-to-carts, **0 purchases**. Ad set names (FailedIPL, RazorReveal, DeviceGraveyard, Strawberry) suggest a hair-removal (IPL) device. UNVERIFIED what the product was.
- **Velmir**: 1 campaign (R1_Velmir_Redraft), £645.42 spent, 3 add-to-carts, **0 purchases**. Product not checked.
- Pattern carried into Ninu: long-form story copy in the brand's voice and testing several angles at once.

**Ninu timeline:**

| Date (2026) | Event |
|---|---|
| Oct 19 | Store goes live (first sessions) |
| Oct 22 to 30 | All 7 orders, every one from the R1_Ninu Meta campaign |
| Oct 25 | Orders #1004 and #1005 placed by PayPal while PayPal was not properly connected. Both later **expired** unpaid |
| Oct 29 | 981-session junk-click day from one ad, 0 orders |
| Oct 31 | Store diagnosis (R12): the leak is before add-to-cart, not at checkout. Owner's PayPal account restricted during verification; appeal filed (outcome UNVERIFIED) |
| Nov 1 | Product page rebuilt mobile-first (sticky add-to-cart, price higher up, offer cards) |
| about Nov 4 to 6 | "Early Black Friday" sale added: $49.99 shown against a struck-through $62.49, countdown to Nov 10 11:59 PM Pacific, "Price goes to $62.49 on Nov 11". 4-free-gifts block added. Red Black Friday banner added |
| Nov 6 | R16 test: Ad C body rewritten in buyer language |
| Nov 7 | R17 "swipes" ad set (7 native-style ads) launched at about £70 to £75 a day. Personal bulk ad launcher app built (`ads-launcher/`) |
| Nov 7 to 8 | 3 UGC-style green-screen videos produced (`ugc-video/`). 4 Black Friday static ads made and drafted into a paused £55/day ad set |
| Nov 8 | Landing-page test launched: same ad to the current page vs the old page (`?view=old-pdp`). Every other ad set paused |
| Nov 9 to 10 | Owner paused the current-page ad. Test stopped at the click limit. Owner turned the old-page ad back on |
| Nov 10 | Gift-block test launched (old page vs old page plus gift block). Owner deleted the control ad. Template paste problems left the old page white for about 15 minutes (fixed) |

---

## 3. Product, offer and money

| Product (Shopify) | Price | Notes |
|---|---|---|
| The Ninu Kit | $49.99 | Dispenser, 60ml rosemary scalp oil (30-day supply), satin sleep bonnet. Shopify compare-at price is **empty** |
| Ninu Applicator + Satin Bonnet ("Dispenser Only") | $39.99 | No oil |
| Rosemary Essential Oil Refill | $32.99 one-time, or $16.99 a month on subscription ($16 off) | Subscription selling plan "Deliver every 4 weeks" |
| Shipping Protection | $3.50 | Cart add-on |

- **Free US shipping, 30-day money-back guarantee.** Dropshipped from supplier WANB-US, 6 to 12 days.
- **Free gifts promised on the current page:** scalp massager, bedside pouch, "The Scalp Routine That Sticks" guide (emailed), Ninu Night Tracker (emailed). Gifts are not added to orders automatically; they must be packed and emailed by hand. UNVERIFIED whether the massager and pouch are sourced and whether the emails work.
- **Costs:** landed cost about $13.50 per kit. Card fees about 2.9% + $0.30. **Break-even cost per order about $34.74 (about £26.72); target about £21.38.**
- At the store's historical conversion rate (about 0.7% of ad sessions buy), a click must cost about £0.20 or less to break even.

**Avatar:** postpartum mothers with hair loss, who already believe in oiling the scalp but keep skipping it. Pain: "pulling out handfuls of hair in the shower", temples in photos. Desire: "I just want to feel like myself again." Failed solutions: shampoos, vitamins, satin pillowcases, castor oil with a shower cap, expensive supplements.

**Winning angle (Ad C, "messy routine"):** "The habit was always there. The routine just needed to be easier than the reason to quit." Mechanism: hair does not absorb oil, skin does. A dropper or fingers put the oil on hair, neck and towel; hollow silicone tips press along the part and release it on the scalp. One hand, two minutes, works with the oil you already have. Compliance lane: behaviour and delivery claims only.

---

## 4. Results: store funnel and orders

**Weekly store funnel (Shopify):**

| Week starting | Sessions | Added to cart | Reached checkout | Orders |
|---|---|---|---|---|
| Oct 19 | 368 | 12 | 9 | 5 |
| Oct 26 | 1,675 | 18 | 10 | 2 |
| Nov 2 | 1,034 | 5 | 5 | 0 |
| Nov 9 (to Nov 10) | 361 | 2 | 2 | 0 |

**Orders:**

| Order | Date | Total | Payment | Status | Ad (utm content) |
|---|---|---|---|---|---|
| #1001 | Oct 22 | $66.98 (kit + refill) | Shopify Payments | Paid, fulfilled | 120250988064320342 |
| #1002 | Oct 24 | $49.99 | Shopify Payments | Paid, fulfilled | 120251024608350342 |
| #1003 | Oct 25 | $49.99 | Shopify Payments | Paid, fulfilled | 120251061111520342 |
| #1004 | Oct 25 | $169.96 (2 kits + 2 dispensers) | PayPal | **Expired, unfulfilled** | 120251061130930342 |
| #1005 | Oct 25 | $49.99 | PayPal | **Expired, unfulfilled** | 120251061130930342 |
| #1006 | Oct 26 | $49.99 | Shopify Payments | Paid, fulfilled | 120251061111520342 |
| #1007 | Oct 30 | $49.99 | Shopify Payments | Paid, fulfilled | 120251135585830342 |

---

## 5. Results: Meta spend by Ninu ad set (lifetime, campaign R1_Ninu `120250953264900342`)

Purchases, add-to-carts and checkouts are Meta pixel counts.

| Ad set | Spend | Link clicks | Cost per click | Add to cart | Checkout | Purchases |
|---|---|---|---|---|---|---|
| A1_C_VariantsTest | £467.42 | 80 | £5.84 | 10 | 10 | 4 |
| New_Creative_Test | £319.73 | 1,438 | £0.22 | 0 | 0 | 0 |
| A1_C_Messyroutine_HookTest | £225.13 | 143 | £1.57 | 2 | 1 | 1 |
| A1_Ninu | £176.88 | 42 | £4.21 | 2 | 1 | 1 |
| Variant_Format_Rerun_Hooks_Test | £139.15 | 97 | £1.43 | 1 | 1 | 1 |
| R17 Swipes (Nov 7) | £102.33 | 503 | £0.20 | 0 | 0 | 0 |
| New_Creative_Test_2 | £85.88 | 41 | £2.09 | 0 | 0 | 0 |
| New vid_Set | £84.84 | 40 | £2.12 | 1 | 1 | 0 |
| Hook3_BuyerLanguage_Test (R16) | £68.10 | 240 | £0.28 | 0 | 0 | 0 |
| A1_C_Advetorial | £60.02 | 19 | £3.16 | 1 | 0 | 0 |
| Hook3_PageTest_Current_vs_OldPDP | £50.45 | 312 | £0.16 | 1 | 1 | 0 |
| Hook3_OG_Copy_Test | £28.70 | 190 | £0.15 | 0 | 0 | 0 |
| Hook3_GiftTest_OldPDP_vs_Gifts (live) | £4.91 | 32 | £0.15 | 0 | 0 | 0 |
| **Total** | **£1,813.54** | **3,177** | | **18** | **15** | **7** |

**The clearest pattern in the data:** every purchase came from ad sets where clicks cost £1.40 to £5.80 (Oct 22 to 30). Every ad set since Oct 29 with very cheap clicks (£0.15 to £0.28) has produced about 2,700 clicks and almost no add-to-carts (1 in total). Cheap clicks are not buyers. This supports the owner's theory that recent ads attract scrollers, not buyers. It is a pattern in small numbers, not proof.

---

## 6. Problems, ranked by impact

Each problem lists: the evidence, what has been done, and the current status.

### P1. Almost nobody adds to cart (the main problem)
- **Evidence:** about 99% of ad visitors leave the product page without adding to cart. Checkout is not the leak: when people do start checkout, most finish (7 orders from 15 Meta-reported checkouts).
- **Done:** store diagnosis (Oct 31); mobile-first page rebuild (Nov 1); Black Friday offer, gift stack and banner (Nov 4 to 6); buyer-language copy (R16); page test current vs old (Nov 8 to 10); gift-block test (Nov 10, running).
- **Status:** not solved. No orders since Oct 30.

### P2. Traffic quality: cheap clicks, no buyers
- **Evidence:** see the pattern in section 5. Ad sets with £0.15 to £0.28 clicks: about 2,700 clicks, 1 add-to-cart. Oct 29 had a 981-session junk-click day.
- **Done:** the owner suspected this and asked for buyer-language copy (R16, 0 add-to-carts on 240 clicks) and buyer-focused swipes (R17, 0 on 503 clicks). Neither changed the result.
- **Status:** open. Untested ideas: placement exclusions (Audience Network, Threads, in-stream), turning off Advantage+ audience, longer copy that filters for intent, or bringing back the higher-cost-click creatives that did convert.

### P3. Cost per order far above break-even
- **Evidence:** £1,813.54 spent for 5 paid orders, about £363 per paid order against about £26.72 break-even. Even counting all 7 orders it is about £259.
- **Done:** kill checkpoints written (`ads/ninu-kill-criteria.md`: £14 with 0 link clicks, £28 with 0 add-to-cart, £42 with 0 checkout, £54 with 0 purchases). Spend reduced to test budgets.
- **Status:** open. The account has never been profitable on Ninu.

### P4. The Black Friday price claim expires tonight
- **Evidence:** the current page says "Price goes to $62.49 on Nov 11" with a countdown ending Nov 10 11:59 PM Pacific. In Shopify the kit is $49.99 with **no compare-at price**; the $62.49 is typed into the page code only.
- **Done:** flagged as fake urgency in several sessions. The owner was advised the claim is only honest if the price really changes on Nov 11 and $62.49 was a real recent price.
- **Status:** **urgent decision needed today:** either raise the price to $62.49 on Nov 11, or remove the countdown and "goes to $62.49" text before it passes.

### P5. Unverified trust claims still on both pages
- **Evidence (checked today on the current page and the old page):** "Trusted by 10,000+ women" on a store with 7 orders; three named "verified buyer" reviews (Rachel M., Amara T., Jenna K.) with AI-generated before-and-after images; a "Month 2 / Month 5" before-and-after section; "Made in the USA"; "Natural Ingredients". Both pages also show a 5-7 day shipping figure while the supplier ships in 6 to 12 days.
- **Done:** flagged as false or unsupported since Oct 31. The owner chose to keep "Trusted by 10,000+".
- **Status:** open. Risks: ad account rejection, chargebacks, consumer-protection complaints. It may also lower trust with savvy buyers.

### P6. Payments: two orders lost to PayPal
- **Evidence:** #1004 ($169.96) and #1005 ($49.99) are now **Expired**, never paid, never shipped. PayPal was restricted during verification around Oct 31; appeal outcome UNVERIFIED.
- **Done:** advised not to ship until paid.
- **Status:** open. These customers have not been contacted (UNVERIFIED). Check whether PayPal works at checkout now.

### P7. Store editing is fragile
- **Evidence:** the product page is one large Custom Liquid block (44,000 to 51,000 characters, near Shopify's 50,000-character limit). On Nov 10, pastes landed in the wrong template, were cut to the first line, or saved empty. The old page went white for about 15 minutes while an ad was sending traffic to it.
- **Done:** files rebuilt as single-line versions; fixed by restoring older versions in Edit code and editing three price spots with Find. Both test pages verified correct afterwards.
- **Status:** working now. Lesson: use Edit code, then Older versions or Find and replace. Avoid pasting the whole page in the theme editor. Close other editor tabs first.

### P8. Offer and fulfilment gaps
- **Evidence:** the current page promises 4 free gifts (massager, pouch, guide, tracker). Gifts are not added to orders automatically. UNVERIFIED whether the massager and pouch are sourced and the emails are set up. The oil the supplier ships may be a MELAO-branded rosemary oil (UNVERIFIED) while the page calls it Ninu scalp oil.
- **Status:** open. Promising gifts that are not sent turns into refunds and chargebacks.

### P9. Smaller page issues
- Current page button says "Add to Basket" (UK wording for US shoppers).
- The old page says "Cancel refills any time" (true only for subscription buyers).
- Page gallery claims flagged earlier: "Hair doesn't absorb oil. Skin does." (unsupported as written), a shedding line on slide 5, and shipping 5 to 7 days on slide 12.

---

## 7. What has worked and what has not

**Worked (evidence, small numbers):**
- **Ad C, the "messy routine" story**, in its earlier executions (A1_C ad sets): all 7 orders came from these, at £1.40 to £5.80 per click.
- **The old product page** (`?view=old-pdp`) beat the current page in the Nov 8 to 10 test: 1 add-to-cart and 1 checkout from 134 clicks, against 0 from 102. Too small to be sure.
- **Checkout itself:** most people who start checkout finish, so the checkout is not the problem.
- **Hook "Baby up three times. Wet hands, in bed. Skipped my scalp oil again."** (Hook3): cheapest link clicks (£0.15) and the copy used in the latest tests.

**Not worked:**
- Cheap-click ad sets since Oct 29 (New_Creative_Test, R16, R17 swipes, Hook3 variants): about 2,700 clicks, 1 add-to-cart, 0 orders.
- The current product page with the Black Friday offer, 4 gifts, countdown and 12-image gallery: 0 add-to-carts from 102 clicks in the page test, and no orders since it went live.
- Video ads so far (3D sung ad, New vid_Set): high cost per click, no purchases.
- The earlier products, Lumen and Velmir: about £2,470 spent, 0 purchases.

**Built but not yet run:**
- 4 Black Friday static ads (paused ad set `120251279013400342`, £55/day). The ads use the current page's offer (4 gifts), so they only make sense if the gifts are real and the page matches.
- 3 UGC green-screen videos (`ugc-video/`).
- Bulk ad launcher app (`ads-launcher/`).

---

## 8. What is live right now (Nov 10, about 14:00 UTC)

| Ad set | Ad | Page | Budget | Lifetime numbers |
|---|---|---|---|---|
| Hook3_PageTest_Current_vs_OldPDP `120251286699140342` | Hook3_OG_Copy_OLDPAGE `120251286712810342` (switched back on by the owner) | `?view=old-pdp` | £30/day | £31.94 spent, 210 clicks, 1 add-to-cart, 1 checkout, 0 purchases |
| Hook3_GiftTest_OldPDP_vs_Gifts `120251307551640342` | Hook3_OG_Copy_GIFTS `120251307559490342` | `?view=old-pdp-gifts` | £30/day | £4.91 spent, 32 clicks, 0 add-to-carts |

- The gift test's control ad (`120251307558610342`) was deleted by the owner, so the gift ad is now being compared against OLDPAGE in a different ad set. That is a weaker comparison, because Meta delivers the two ad sets separately.
- An hourly automated check pauses the two gift-test ads when the gift-test spend reaches £45 (or both reach 100 link clicks). It does not touch OLDPAGE, which has no automatic stop.
- All other ad sets are paused.

---

## 9. Open questions to confirm with the owner

1. What happens to the price on Nov 11: raise it to $62.49, or remove the countdown?
2. Are the massager and pouch sourced and being packed? Do the guide and tracker emails work?
3. Is PayPal working at checkout now? Were the #1004 and #1005 customers contacted?
4. Which oil actually ships, and what does its label say?
5. Is the owner willing to remove the unverified reviews and "10,000+" claim?
6. How much cash is available for testing, and for how long?

---

## 10. Where things are

- **Repo:** `kengokuhebun/kengokuhebun`. Branches: `claude/new-session-o5o13k` (main Ninu work: `ads/`, `creatives/`, `pdp/`), `claude/ads-launcher-v1` (ads launcher, UGC video, Black Friday statics), `claude/pdp-gift-test` (gift test and this file).
- **Key docs:** `ads/ninu-brand-context-for-organic-chat.md` (Nov 2), `ads/ninu-project-handoff-2026-11-06.md` (Nov 6), `ads/ninu-r12-store-diagnosis-woa.md`, `ads/ninu-kill-criteria.md`, `ads/ninu-r19-offer-evolution.md`, `ads/ninu-r21-after-the-test-scale-roadmap.md`, `ads/ninu-r8-hook-only.md` (Ad C copy).
- **Theme:** `shrine-theme-dev` (live). Product templates: `product.json` (current page), `product.old-pdp.json` (old page), `product.old-pdp-gifts.json` (old page plus gift block). Each page body is one Custom Liquid section, `custom_liquid_QQwhib`.
- **IDs:** Meta ad account `act_1308050554875217` (GBP), Page `1319525544575060`, pixel `1736160617626618`, campaign R1_Ninu `120250953264900342`. Shopify kit variant `63751529824586`, dispenser `63751699595594`, refill `63751894630730`.
