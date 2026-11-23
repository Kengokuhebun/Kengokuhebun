# New Zealand market setup — 2026-11-21

Request: "yes supplier ships to new NZ set up the market for that and shipping and make sure flo to checkout works confirm with screenshot"

## Shopify changes

- **Market**: New Zealand (gid://shopify/Market/110064632135), status Active, base currency NZD, region condition country NZ.
- **Catalog**: "New Zealand pricing" (gid://shopify/MarketCatalog/188556411207), Active, scoped to the NZ market.
- **Price list**: "New Zealand (NZD)" (gid://shopify/PriceList/31506268487), currency NZD, parent adjustment 0% (fixed prices), 3 fixed prices:
  - Glowling LED Drawing Board: NZ$54.99
  - Glow Tracing Book – Free Gift: NZ$0.00
  - Neon Marker Pen Pack: NZ$10.99
  - (Buy 2 Get 1 FREE bundle computes to NZ$109.98, same automatic discount as other markets — no separate bundle variant.)
- **Shipping**: added a "New Zealand" zone to the existing "General profile" delivery profile (gid://shopify/DeliveryProfile/140657590599), free shipping (5 to 10 business days), NZ$0.00, same as AU/CA/US. Confirmed via `deliveryProfile.profileLocationGroups.countriesInAnyZone` showing NZ.

### Snag hit and resolved
After creating the zone, `shop.shipsToCountries` / `shop.countriesInShippingZones` kept returning only AU/CA/GB/US — NZ was configured but Shopify hadn't propagated it, so the storefront reported the board "already sold out" in NZ (confirmed via direct `/cart/add.js` calls returning 422). Re-saving the zone didn't force it; it resolved on its own after a delay (confirmed clear roughly 1.5–2 hours after the zone was created). No further action was needed once it cleared.

## PDP code change (committed `6b9ccfc`)

`pdp/glowling/GLOWLING-PDP-one-section.html` — added NZD to the SETTINGS block:
- `PRICE.NZD = 5499` (fallback, overridden by live Shopify price)
- `FREE.NZD = 8000` (free-shipping threshold, NZ$80 — no real free-ship threshold exists since all shipping is free; this is inert for NZ but kept for parity)
- `CUT.NZD = '18 December'` (holiday cutoff, copied from AU — not independently confirmed)
- `LOC.NZD = 'en-NZ'`

## Verification (Playwright, mobile viewport)

1. Product page `/products/glowling-led-drawing-board?country=NZ` — NZD prices render correctly: NZ$54.99 (Buy 1), NZ$109.98 / NZ$36.66 each (Buy 2 Get 1 FREE, "MOST POPULAR"), free tracing book shown.
2. Add to cart (Buy 2 Get 1 FREE tier) → cart drawer: 4 items (2× board paid, 1× board free, 1× tracing book free), subtotal NZ$109.98.
3. Checkout (`/checkout`) → entered test address (1 Queen Street, Auckland, Auckland, 1010, New Zealand) → shipping method populated: **Standard, FREE, Wed 2 Dec – Wed 9 Dec**.
4. Stopped before payment — no real order placed, matching the "pause, never delete / confirm before anything live" rule.

Screenshots sent to user: cart drawer and checkout-with-shipping-method.

## Still open

- NZ$54.99 board / NZ$10.99 pen pack prices — confirmed OK by user (2026-11-21).
- NZ free-ship threshold and 18 December cutoff date are placeholders, not confirmed by the user or the supplier.
- NZ was not part of the original Meta ad-set budget plan written up in `ads/ritual-swipe/prompts.md`; that doc still reflects CA/US/AU only (UK dropped, NZ added per later messages) and needs updating before any NZ ad spend.
- All Meta campaigns remain paused; no ad traffic should be sent to NZ until the user says so.
