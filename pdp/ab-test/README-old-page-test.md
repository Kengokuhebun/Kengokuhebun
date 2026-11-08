# Old page vs current page: the A/B test (about £30 to £40)

**Question this answers:** is the page or the traffic the reason for ~97% bounce and zero add-to-carts? The old page (the one that got your first sales, Oct 22 to 26) goes live on a second address. The same ad is sent to both. Only the page differs.

**Files:** `ninu-pdp-oct26-old.html` is the page exactly as it was at commit `48d897c` (48,845 bytes, under Shopify's 51,200 limit). It has not been edited.

**Use it for this test only.** It still contains claims I have flagged as risky ("Made for postpartum hair", "Trusted by 10,000+", the named reviewer cards). Run it for the test, then take the template off the ad.

## 1. Create the second page address (about 10 minutes)

1. Shopify admin, **Online Store, Themes, Customize** on your live theme.
2. At the top, open the page selector and choose **Products**. Choose **Create template**.
3. Name it `old`. Base it on the product template you use now, so the sections match. Create it.
4. In that `old` template, find the **Custom Liquid** section that holds your page code. Replace its contents with the whole file `ninu-pdp-oct26-old.html`. Leave the current page alone. Save.
5. Open `https://tryninu.store/products/the-ninu-kit?view=old` on your phone.
   - Check you see the older page. Its top bar reads "FREE US SHIPPING · 30-DAY MONEY-BACK GUARANTEE · SATIN BONNET INCLUDED WITH KIT" and it has a green "MADE FOR POSTPARTUM HAIR" pill. There is no red Black Friday banner.
   - Tap Add to Basket and go to checkout. Stop before paying.
   - Open `https://tryninu.store/products/the-ninu-kit` and confirm the current page is unchanged.

If `?view=old` shows the current page, the template was not saved or named `old` exactly.

## 2. Set up the two ads

1. In Ads Manager, **duplicate `Hook3_OG_Copy`** inside the same ad set. Name the copy `Hook3_OG_Copy_OLDPAGE`.
2. In the copy, set the website URL to `https://tryninu.store/products/the-ninu-kit?view=old`. Keep the URL parameters field exactly as it is, so the ad ID still tags the sessions.
3. Leave the original ad on the normal page. Everything else (image, copy, headline, audience) stays identical.
4. Keep the ad set budget at about £15 to £20 a day. **Turn off every other ad.** Nothing else should be running.

## 3. Read it

In Shopify, run this and look at the two ad IDs (the new one is the copy):

```
FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, bounce_rate GROUP BY utm_content SINCE -2d UNTIL today ORDER BY sessions DESC
```

Wait for **about 60 to 100 sessions on each**. At current click prices that is roughly £10 to £35 per side. Then stop both ads, whatever the result.

| Result | What it means | Next step |
|---|---|---|
| Old page bounce about 88% or lower, with add-to-carts. Current page about 97% | The page rebuilds hurt conversion | Go back to the old page as the base and re-add changes one at a time |
| Both about 97% with no add-to-carts | The traffic is the problem, not the page | Stop Sales-campaign ads. Use a Traffic campaign diagnostic on Facebook Feed only |
| Both better than 97% (for example 90%), neither has add-to-carts | Mixed. Watch recordings before spending more | Add session recordings and read 20 visitors |
| Current page better than the old one | The page is not the cause | Same as "both about 97%" |

Stop-loss: if either ad reaches £28 with no add-to-cart, pause it, but only after the other has reached at least 60 sessions.

## 4. Clean up

When the test is done, remove the `?view=old` ad. Keep or delete the `old` template as you like.
