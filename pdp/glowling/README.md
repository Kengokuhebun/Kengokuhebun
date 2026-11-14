# Glowling PDP: custom liquid blocks

Layout follows the competitor's product page block for block, with: benefits above Add to cart, trust + payment badges and a testimonial below it, extra social proof, a below-the-fold sales section, and a working side cart. All copy is original.

**Quickest route:** open `ALL-BLOCKS-paste.liquid`. Every block is there with a "PASTE INTO" line telling you where it goes. Or paste the individual files below.

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
