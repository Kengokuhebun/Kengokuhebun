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
