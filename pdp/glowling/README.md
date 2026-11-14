# Glowling PDP

## Use this: `GLOWLING-PDP-one-section.html` (one paste, whole page)
Built on the same structure as the working Ninu page: one Custom Liquid **section**, one root `<div class="gw">` with its own `<style>` and `<script>`, pure HTML/CSS/JS, no Liquid. 39 KB (under the 50 KB limit).

It contains: announcement bar, header with its own cart button, swipe gallery (9 images from Files) with thumbnails, trust line, title, price, offer box with the holiday date for each country, benefits, Buy 1 / Buy 2 Get 1 FREE tiers, the free tracing book, Add to cart, shipping line, payment icons, trust row, testimonial, accordions, marquee, the full below-the-fold sales sections, a sticky add-to-cart bar, and its own side cart (free-shipping bar, quantity +/−, pen pack upsell, checkout).

**Prices:** loaded from `/products/glowling-led-drawing-board.js`, which returns the visitor's own market price, so UK sees £29.99, US $34.99, Canada $44.99 and Australia $49.99 from the fixed prices in Markets. Free-shipping threshold and holiday date switch by currency. All settings are at the top of the `<script>` under `SETTINGS`.

**Paste steps**
1. Online Store → Themes → Customize → Products → **Default product** (or a new template assigned to the Glowling product only).
2. Hide or remove the **Product information** section (and anything else on the template you don't want).
3. **Add section → Custom Liquid** → paste the whole file → Save.
4. Theme settings → **Cart → Cart type → Page**, so the theme's own drawer doesn't open on top. Theme links to `/cart` open the Glowling drawer instead.

Tested in Chromium against a mock store in all four currencies: gallery, tier switch, Add to cart (3 boards + free book), automatic discount shown in the cart, free-shipping bar, upsell, quantity, removing the last board also removes the free book, ESC/overlay/close, theme cart link, sticky bar, CTA scroll, checkout, no horizontal scroll at 390 px, no JS errors.

---

## Older version: separate Custom Liquid blocks
Layout follows the competitor's product page block for block. Use the one-section file above instead.

## Store status (Glowling, x5a9bu-97.myshopify.com · GBP · Horizon theme)
Created via the Admin API, all as **drafts** (nothing is live until you set them to Active):

| Item | Handle | Price | Notes |
|---|---|---|---|
| Glowling LED Drawing Board | `glowling-led-drawing-board` | £29.99 (placeholder) | 9 gallery images attached in order: hero → offer → how it works → vs tablet → four uses → collage → size → dinner → box. Alt text set. Description + SEO filled. |
| Glow Tracing Book – Free Gift | `glow-tracing-book` | £0.00 | Added automatically to every order by block 03b |
| Neon Marker Pen Pack | `neon-marker-pen-pack` | £5.99 (placeholder) | Side cart upsell (block 07). Needs a product photo |
| Discount "Buy 2, Get 1 FREE" | automatic, Buy X get Y | — | Active, but only applies to the Glowling board, so nothing happens while the board is a draft |

### Fixed prices per country (Shopify Markets, verified with contextual pricing)
Markets: United Kingdom (GBP, store base) · United States (USD) · Canada (CAD, split out of the old "United States and Canada" market) · Australia (AUD). Each non-UK market has its own catalog + price list with fixed prices:

| Product | UK | US | Canada | Australia |
|---|---|---|---|---|
| Glowling LED Drawing Board | £29.99 | $34.99 | C$44.99 | A$49.99 |
| Buy 2, Get 1 FREE (3 boards) | £59.98 | $69.98 | C$89.98 | A$99.98 |
| Neon Marker Pen Pack | £5.99 | $6.99 | C$8.99 | A$9.99 |
| Glow Tracing Book (gift) | £0 | $0 | C$0 | A$0 |

Free-shipping thresholds in blocks 03b/04/07 (£40 / $50 / C$70 / A$75) sit between the single and bundle price in every market. Make your shipping rates in Settings → Shipping match them.
UK prices are set on the product itself. To change US/CA/AU prices: Settings → Markets → (market) → Products and pricing.

To go live: set your real prices, add a pen pack photo, set all three products to **Active** on the Online Store channel, then paste the blocks into the Horizon product template.
Horizon note: Custom Liquid is available both as a block inside the product information section and as a standalone section. If your Horizon version doesn't list it as a block, add the blocks as Custom Liquid sections directly under the product section, in the same order.

## Product information blocks (theme editor → Products → Default product)

| # | Block | File |
|---|---|---|
| 1 | Custom Liquid: holiday offer box (date changes per market) | `01-offer-box-above-title.liquid` |
| 2 | Title | theme |
| 3 | Review stars (Judge.me app block) | app |
| 4 | Custom Liquid: social proof line | `02-social-proof-under-title.liquid` |
| 5 | Price | theme |
| 6 | Custom Liquid: benefits | `03-benefits-above-atc.liquid` |
| 7 | Custom Liquid: bundle tiers + Add to cart (replaces Kaching, Quantity and Buy buttons) | `03b-bundle-tiers-and-add-to-cart.liquid` |
| 8 | ~~Quantity + Buy buttons~~ | remove these theme blocks, and turn Kaching off for this product |
| 9 | Custom Liquid: trust row + payment badges | `04-trust-and-payment-badges-below-atc.liquid` |
| 10 | Custom Liquid: featured testimonial | `05-testimonial-under-atc.liquid` |
| 11 | Description / collapsible tabs | theme |

Under Product information: **Add section → Custom Liquid** → `06-below-the-fold-section.liquid`. Then the review widget, then Related products.

## Side cart (`07-side-cart.liquid`)
1. Theme editor → **Footer** section group → **Add section → Custom Liquid** → paste. It then works on every page.
2. Theme settings → **Cart → Cart type → Page**, so the theme's own drawer or popup doesn't open on top.
3. If you keep Kaching Bundles on other products, set its after-add action to **Do nothing / stay on page**.
4. Optional upsell: create the add-on product (e.g. a marker refill pack) and put its handle in `gl_cart_upsell_handle`.
5. Free-shipping thresholds are in the `FREE_SHIP` line (in cents, by currency). Keep them in step with block 04.

Tested against a mock Shopify cart API in Chromium. These all pass: theme form add, app fetch add, app XHR add, quantity +/−, remove, empty state, upsell add, header cart icon, ESC and overlay close, and the checkout link. No JS errors.

## Offer setup (block 03b, no app needed)
Offer: **Buy 1** / **Buy 2, Get 1 FREE** (default, "MOST POPULAR") + a **free tracing book** with every order + a **pen pack** upsell in the side cart.

| Tier | Adds to cart | Price shown | Perks shown |
|---|---|---|---|
| Buy 1 | 1 board + tracing book | 1 × price | FREE tracing book (+ FREE shipping if over the market's threshold) |
| Buy 2, Get 1 FREE | 3 boards + tracing book | 2 × price, 3 × price struck through, "Save 1 × price" | 1 board FREE · FREE tracing book · FREE shipping (if over threshold) |

Three things to set up in Shopify admin:
1. **The discount (required):** Discounts → Create discount → **Buy X get Y** → Automatic. Customer buys: minimum quantity **2** of Glowling. Customer gets: **1** of Glowling, discounted value **Free**. Leave "maximum uses per order" blank. Without it, the 3rd board is charged.
2. **The free tracing book:** create a product priced **0.00** with the handle `glow-tracing-book` (or change `gl_gift_handle` in 03b). It's added to every order automatically. If you'd rather just pack it in the box, set `gl_gift_handle` to `''`.
3. **The pen pack upsell:** create a product with the handle `neon-marker-pen-pack` (or change `gl_cart_upsell_handle` in block 07). It shows in the side cart once the cart has items, and hides after it's added.

Tested with the side cart on a mock store: the tier switch updates the button total, and "Buy 2, Get 1 FREE" adds 3 boards + the tracing book and opens the drawer. No JS errors.

## Placeholders to replace before running paid traffic
- **Testimonials** in blocks 05 and 06 are placeholder copy. Swap in real customer reviews: fake reviews break FTC (US), DMCC (UK), Competition Act (CA) and ACL (AU) rules.
- Block 02: real rating and order count, once you have them.
- Block 01: real holiday cutoff date per market. Block 04 + side cart: real free-shipping thresholds.
- Block 06: board size and marker count from your supplier; image URLs (`gl_img_problem`, `gl_img_steps`, `gl_img_box`) from Shopify Files.

Payment icons load from jsDelivr (`payment-icons@1.2.1`, `simple-icons@13.21.0`, version-pinned). Delete any icon for a payment method you don't offer.
