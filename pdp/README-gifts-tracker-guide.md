# Gifts block, Night Tracker and guide: how to use these files

Written 2026-11-04.

## Files

| File | What it is |
|---|---|
| `pdp/ninu-pdp.html` | The product page (Custom Liquid). Now has the "+ 4 free gifts" block, clearer benefits, a trimmed FAQ, and no "Low stock" pill. 50,845 of 51,200 bytes. |
| `pdp/ninu-night-tracker.html` | The Night Tracker. Paste into a Custom Liquid section on its own page. |
| `pdp/ninu-guide-scalp-routine-that-sticks.pdf` (+ `.html` source) | The 9-page guide, 5.5 x 8.5 in, phone-friendly. |
| `pdp/previews/` | Screenshots of each. |
| `pdp/ninu-ebook-scalp-routine-that-sticks.md` | Old text. Superseded by the new guide. Not to be used (it made claims we shouldn't promise). |

## Product page: the gifts switch

The whole gifts feature is controlled by one class on the first line of the page: `ninu-gon`.

- **Present** (as shipped): the "+ 4 free gifts" block, the "Add Kit + 4 Free Gifts" button, "+ 4 free gifts" in the sticky bar, the gift line in the benefits, the gifts in the cart's "What's included", and the gift sentence in the FAQ.
- **Removed** (delete ` ninu-gon` from `<div class="ninu-wrap ninu-kit ninu-gon">`): the page goes back to the old kit list with the ebook line and "Add to Basket".

**Do not paste it live with the class present until the massager and pouch exist and ship.** The tiles are placeholders (a line icon on a cream square) and promise real gifts.

### Putting in the real photos

Each tile has an icon inside `<span class="ninu-g-i">`. To add a photo, replace the whole `<svg ...>...</svg>` inside that span with:

```html
<img src="YOUR_IMAGE_URL" alt="Scalp massager">
```

Square-ish images work best (the tile crops to about 1:0.72). Do this for the four tiles in the kit card. The text under each tile (name and one-line description) is in the same tile.

## Night Tracker: setting it up

1. Shopify admin: Online Store > Themes > Customize.
2. Top bar: choose Pages, then Create template, name it `night-tracker`, base on Default page.
3. Add a Custom Liquid section and paste `ninu-night-tracker.html` into it. Save.
4. Online Store > Pages > Add page. Title "Night Tracker", pick the `night-tracker` template, handle `night-tracker`. Publish.
5. The page lives at `https://tryninu.store/pages/night-tracker`. That's the link used in the guide. If you use a different handle, change the link on the last page of the guide (search `night-tracker` in the HTML, then re-export the PDF).
6. The refill button inside the tracker links to `/products/rosemary-essential-oil-refill`. If you rename that product, check the link.

Progress is saved in the customer's browser. No accounts, nothing is collected.

## Sending the guide and tracker

Shopify can't attach files to the order email, so link them:
1. Upload the PDF to Settings > Files and copy its URL.
2. Settings > Notifications > Order confirmation (or Shipping confirmation). Add a short block: the guide link and the tracker link.

## Check before you go live

- [ ] The massager and bedside pouch are sourced, photographed, and in the box. (Run the supplier checks in `ads/ninu-r19-offer-evolution.md`.)
- [ ] Steps 2 to 4 of the guide (fill, part, press) match how your real dispenser works. I wrote them from your page copy, not from a manual.
- [ ] The guarantee: your shipping time (6 to 12 days) plus 30 nights is longer than 30 days. Decide whether the 30 days run from delivery, and say so in the policy.
- [ ] The tracker and guide are emailed after purchase. Don't advertise them until that email works.
