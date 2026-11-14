# Glowling PDP: custom liquid blocks

The layout follows the competitor's product page (kidsaustralia.com, Shrine theme) block for block, with the changes you asked for: benefits above Add to cart, payment badges and a testimonial below it, more social proof, and a side cart. All copy is original. Do not reuse the competitor's text or photos.

Paste each `.liquid` file into a **Custom Liquid** block. In the theme editor go to Products → Default product → Product information → Add block → Custom Liquid. Every block has its editable values at the top (`assign` lines). Fill every `[BRACKET]` before publishing.

## Block order in "Product information"

| # | Block | File | Competitor equivalent |
|---|---|---|---|
| 1 | Custom Liquid: offer box | `01-offer-box-above-title.liquid` | "EARLY BLACK FRIDAY: 50% OFF" box |
| 2 | Title | theme block | same |
| 3 | Judge.me review stars (app block) | app | same |
| 4 | Custom Liquid: social proof line | `02-social-proof-under-title.liquid` | **new** (more social proof) |
| 5 | Price | theme block | same |
| 6 | Custom Liquid: benefits | `03-benefits-above-atc.liquid` | their 3 icon bullets, now clearer and above the ATC |
| 7 | Variant picker / Kaching Bundles (app block) | app | same |
| 8 | Quantity + Buy buttons | theme block | same |
| 9 | Custom Liquid: trust row + payment badges | `04-trust-and-payment-badges-below-atc.liquid` | **new** |
| 10 | Custom Liquid: featured testimonial | `05-testimonial-under-atc.liquid` | their "Olivia T." card, moved under the ATC |
| 11 | Description (collapsible tab or text) | theme block | same |

Under the main product section: **Add section → Custom Liquid** → paste `06-below-the-fold-section.liquid`. Then add the Judge.me review widget section, then Related products.

## Side cart
Theme settings → Cart → set **Cart type** to **Drawer**. In Shrine and other Dawn-based themes the label may be "Cart drawer". Turn on the free-shipping progress bar and cart upsell if your theme version has them. If not, Kaching Bundles' cart features or an app like UpCart can add them.

## Before you go live
- Reviews and counts must be real (Australian Consumer Law). The blocks hide or show placeholders until you fill them in.
- Only say "ships from Australia" or give a Christmas cutoff date if your stock is local.
- Avoid countdown timers that reset. The competitor's "Offer ends 13.11.2026" was already in the past and still showing. Use a real deadline, such as the Christmas cutoff.
- Check box contents, board size and marker count against your supplier's spec sheet.
