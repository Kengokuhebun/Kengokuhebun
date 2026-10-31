# R12: Why isn't the store selling? W / O / A diagnosis (data pulled 2026-10-31)

Source: Shopify analytics (ShopifyQL) and Admin API, Oct 17-31. Store live since about Oct 19. Nothing here comes from
Meta Ads Manager (I have no read access); items that need it are marked NEEDS META.

## 1. Evidence

**Orders (7 in total, all from one paid Facebook campaign, 120250953264900342)**

| # | Date | Total | Status | Gateway | Ad (utm content) |
|---|---|---|---|---|---|
| 1001 | Oct 22 | $66.98 (kit + refill) | PAID | Shopify Payments | 120250988064320342 |
| 1002 | Oct 24 | $49.99 | PAID | Shopify Payments | 120251024608350342 |
| 1003 | Oct 25 | $49.99 | PAID | Shopify Payments | 120251061111520342 |
| 1004 | Oct 25 | $169.96 (2 kits + 2 applicators) | **PENDING** | PayPal | 120251061130930342 |
| 1005 | Oct 25 | $49.99 | **PENDING** | PayPal | 120251061130930342 |
| 1006 | Oct 26 | $49.99 | PAID | Shopify Payments | 120251061111520342 |
| 1007 | Oct 30 | $49.99 | PAID | Shopify Payments | 120251135585830342 |

Gross $486.89, of which **$219.95 (45%) is PayPal-pending since Oct 25**. Paid revenue $266.94 from 5 orders.

**Funnel, 14 days**

| Segment | Sessions | Added to cart | Reached checkout | Completed |
|---|---|---|---|---|
| Whole store | 1,932 | 28 (1.45%) | 18 | 7 |
| Whole store excluding Oct 29 (981-session junk day, 3 ATC) | 951 | 25 (2.6%) | n/a | 7 |
| Facebook + Instagram | 1,708 | 12 (0.70%) | 9 | 7 |
| Direct (mostly you and testers) | 205 | 12 | 7 | 0 |
| Mobile | 1,704 | 19 (1.1%) | 13 | 7 |
| Desktop | 178 | 9 | 5 | 0 |

- 1,813 of 1,932 sessions are US (94%). 88% mobile.
- 1,767 sessions (91.5%) land on `/products/the-ninu-kit`; bounce 91.5%, 24 ATC. 114 land on the homepage (95% bounce).
- Social ATC to checkout 75%, checkout to order 78%. The checkout step is not where people are lost.

**Page (iPhone 13 profile, Facebook in-app user agent)**: 91 requests, 39 scripts, 2.4 MB. LCP 1.8s on fast 4G,
8.1s on slow 4G. First screen on mobile: a 3-line announcement bar, logo, thumbnails and the hero slide. Price and the
Add to basket button appear about 1.4 screens down. No sticky add-to-cart bar.

**Offer**: no discount of any kind exists (zero discount nodes). Only AOV pusher is the refill subscription and a
"dispenser only" option. Inventory is not tracked (the kit shows -8). The hero slide carries an "EARLY BLACK FRIDAY"
pill with no offer behind it.

## 2. Findings that need fixing regardless of conversion

1. PayPal orders #1004 and #1005 are pending. Check PayPal Activity for the reason before fulfilling.
2. "Trusted by 10,000+ women" and three "verified buyer" testimonials on a store with 7 orders are not true. Remove them.
3. "LOW STOCK" is not backed by inventory (not tracked). Keep the ship date, drop the claim.
4. "EARLY BLACK FRIDAY" pill: remove it or put a real offer behind it.
5. Ebook promised on the PDP has no delivery set up.

## 3. The three whys

**Why isn't it selling?** About 99% of visitors never add to cart. Checkout converts the ones who start it.
**Why don't they add to cart?** Candidates in order of evidence: (a) traffic quality on some ads, (b) a first screen with
no price, proof or offer, (c) no real offer on a $49.99 product from an unknown brand.
**Why those?** Cold, low-awareness traffic is asked to decide in a 3-4 screen page with nothing that makes leaving feel
costly, and the only trust elements are claims that are not true.

Not yet separable with Shopify data: traffic quality versus page. NEEDS META: link clicks per ad versus Shopify sessions
per ad (loss before the page loads), ATC rate by ad, placement breakdown of the Oct 29 ad.

## 4. Fix order

1. Resolve the PayPal pending orders (money already earned, 45% of gross).
2. Remove the false claims (10,000+, verified buyer, low stock, Black Friday pill). Risk: FTC fake-review rule, Meta
   and Shopify account action, and trust.
3. Build a real offer (bundle or free gift) and put price, a real proof line and a sticky add-to-cart bar on the first
   screens of mobile.
4. Ads: Facebook and Instagram placements only, kill the junk-click ad, map the five converting ad IDs to names, collect
   real reviews from the 5 paid buyers.
5. Trim the page (scripts, images), lower priority.

Decision arithmetic for the offer (kill-criteria COGS): a 3-for-2 style offer at $99.98 for 3 kits leaves about $62.67
after COGS ($11.37 x 3) and card fees, against $34.74 on a single kit, so it roughly doubles the CAC you can afford.

## 5. Offer options against the master document (Drive doc, offer rules only)

The master document has no worked offer breakdown (no prescribed bundle or price ladder). It has rules and a menu:
- Section 3: "Offer + Bonuses: what they get, and what sweeteners come with it", plus guarantee and urgency.
- Intake rule: "Offer: only if straight to product page. Exact prices, tiers, bonuses, guarantee. Never invent prices."
- Offer framings it lists: "price-agnostic / BOGO named / guarantee-led / kit-led / quantity-as-course".
- PDP slide 01: an offer badge "must reflect my real offer"; slide 09: do not fabricate a complementary product.
- Offer block: per-day or per-use cost math if real; "free gift or free shipping callouts if real"; "No manufactured
  urgency unless the brand truth gives you a real deadline."
- CTA rule: button text names the offer, one-line guarantee subtext under it, "Sticky bottom bar on mobile only".
- Its own diagnosis rule: "Weak CTR with good impressions means hook and lead. Good clicks but weak conversion means the
  belief shift did not complete, strengthen the body. Add-to-cart but no purchase means risk, offer, urgency."

| | Kit + 1 free oil (gift) | 3-Month Kit at $79.99 (kit-led, quantity-as-course) |
|---|---|---|
| Allowed by the doc | Yes: free gift callout "if real", bonus stacking is a listed device | Yes: "quantity-as-course" is a listed framing; per-use math is encouraged |
| Real deadline for urgency | Yes (a dated promotion) | Yes (a dated promotion) |
| AOV | unchanged ($49.99) | +60% ($79.99) |
| Margin after COGS and card fees | $27 to $31 (down from $34.74) | $49 to $56 (up) |
| Cost per night (30 nights per oil) | $0.83 (60 nights for $49.99) | $0.89 (90 nights for $79.99) |
| Fits "do not drop AOV" | No (neutral AOV, lower margin) | Yes |
| Needs | supplier quote for an extra oil | supplier quote for kit + 2 oils, new Shopify product |

By the doc's own rule the first lever is not the offer. Clicks are good (1,708 social sessions) and add-to-cart is weak
(0.7%), which the doc reads as "belief shift did not complete, strengthen the body". The offer rule applies after
add-to-cart, and the add-to-cart to order step here is healthy (78% of social checkouts complete). So: round 1 changes
the page (mechanism and price block early, sticky bar) with the offer frozen at $49.99. Round 2 tests the 3-Month Kit
as the one offer change. The doc's "one variable per round" rule is also the answer to "the offer has been changed so
many times".

## 6. Mobile round 1: what changed in `pdp/ninu-pdp.html` (below 900px only; desktop unchanged)

- One-line top bar (dropped the bonnet text, which is in the bullets).
- Compact nav (smaller logo and cart button).
- Thumbnail row hidden on mobile; a "1/12" counter sits under the gallery instead.
- New benefit line under the headline: "Oil poured on your hair mostly stays on your hair. These hollow tips part the strands
  and release it where it matters: your scalp." (a mechanism statement, no result claim; check you are happy with
  "mostly").
- Price block moves above the intro and bullets; the trust bar and "Trusted by" block follow it.
- Sticky bottom bar: price (follows the selected option and quantity), "Ships <date> · 30-day guarantee" and an
  Add to Basket button that uses the same add function and analytics event as the main button.
- The theme's purple scroll-to-top button and the "Low stock" pill are hidden on mobile (the bar carries the ship date).
- Whitespace minified: 50,954 to 49,728 bytes (limit 51,200).
- Not touched: the "EARLY BLACK FRIDAY" pill inside slide 1, "Trusted by 10,000+ women", the reviews and receipts.

## 7. Early Black Friday sale UI (added to `pdp/ninu-pdp.html`)

- Kit card: strike-through $62.49 in brick red next to $49.99, an "Early Black Friday Sale" pill, a countdown under the
  Add to Basket button, and the line "Price goes to $62.49 on Nov 11." The sticky mobile bar shows the strike price too.
  Quantity changes the strike price (2 kits: $124.98), and Dispenser Only shows no sale.
- Countdown ends at a fixed time for every visitor: Nov 10, 2026 11:59 PM Pacific (`Date.UTC(2026,10,11,7,59,59)`).
  When it passes, the strike, pill, bar and timer remove themselves. The page never restarts the timer per visitor.
- Stock bar: not built as "89% sold". It reads the kit's real Shopify inventory (Liquid) and stays hidden unless the kit's
  inventory is tracked and the quantity is between 1 and the cap in the code (`CAP=50`). To switch it on: product
  inventory, Track quantity, set it to the number of kits you will sell at this price, and untick Continue selling when
  out of stock. Today the kit is untracked (shows -8), so the bar is hidden.
- Conditions that make the strike price legitimate: the kit must actually be charged at $62.49 from Nov 11 (change the
  Shopify variant price and the `price` for the kit in the page's `TIER` map, which is in cents). If the price will not
  go up, remove the strike price and the "goes to $62.49" line before launching.
- Size: Apple Pay and Google Pay logos replaced by text pills to free about 3.3KB. File is 47,908 bytes of 51,200.
- Side cart: added a line above Secure Checkout, "Early Black Friday price ends in <countdown>. Goes to $62.49 on Nov 11.",
  shown only while the cart has items and the sale is live. A "cart reserved for 10 minutes" timer was not built: nothing is
  reserved in a Shopify cart and the kit's inventory is untracked, so the timer would be false urgency.
- Stock bar versus timer only: at about 0.8 orders a day (7 orders in the first 9 days), a 50-kit cap would show about 16%
  claimed at the end of the 10 days, which reads as slow selling. Keep the timer-only version until sales volume is higher.
