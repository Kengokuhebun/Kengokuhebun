# Old page + gift block test

One change: the old page (`?view=old-pdp`) with the "+ 4 free gifts" block added inside The Ninu Kit card. Everything else on the page is unchanged: images, copy, banner, prices, buttons and cart.

## Files

| File | What it is |
|---|---|
| `templates/product.old-pdp-gifts.json` | **New test page.** Old page + gift block + dispenser price fix. |
| `templates/product.old-pdp.json` | **Control.** Old page with only the dispenser price fix. |
| `theme-original/` | Copies of the live templates as of 2026-11-10, for rollback. |
| `preview/kit-card-mobile.png` | How the kit card looks on a phone. |
| `build.py` | Rebuilds both templates from `theme-original/`. |

## Dispenser price fix (both files)

The live old page shows Dispenser Only at **$34.99**, but Shopify charges **$39.99**. Both files show $39.99, so the page matches checkout. Apply it to both pages so the only difference between them is the gift block.

## Install (about 5 minutes)

1. **Online Store → Themes → shrine-theme-dev → ⋯ → Edit code.**
2. **Templates → Add a new template.** Type: product. Format: JSON. Name: `old-pdp-gifts`.
3. Select all in the new file, paste the full contents of `templates/product.old-pdp-gifts.json`, then **Save**.
4. Open `templates/product.old-pdp.json` in the theme, paste the contents of `templates/product.old-pdp.json` from this folder, then **Save**. This is only the $39.99 fix.
5. Check on your phone:
   - https://tryninu.store/products/the-ninu-kit?view=old-pdp-gifts shows the gift block in the kit card.
   - https://tryninu.store/products/the-ninu-kit?view=old-pdp shows Dispenser Only at $39.99.
   - On both, Add to Cart adds the kit at $49.99.

Rollback: paste `theme-original/product.old-pdp.json` back, and delete `product.old-pdp-gifts.json`.

## Ad setup for the test

Same as the last test: one ad set, two identical ads.
- Ad A Website URL: `https://tryninu.store/products/the-ninu-kit?view=old-pdp`
- Ad B Website URL: `https://tryninu.store/products/the-ninu-kit?view=old-pdp-gifts`

Gifts are fulfilled outside the cart, the same as on the current page. Nothing is added to the order automatically.
