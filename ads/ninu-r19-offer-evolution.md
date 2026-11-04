# R19: Evolving the Ninu offer (free gift, oil bundle, subscription, post-purchase)

Written 2026-11-04. Facts about your store come from your live Shopify data (checked today). Anything marked **unknown** needs a supplier answer before you build.

## 1. What your store has now

| Item | Today |
|---|---|
| The Ninu Kit | $49.99 (shown with a $62.49 strike until Nov 10) |
| Ninu Applicator + Satin Bonnet | $39.99 |
| Rosemary Essential Oil Refill | $32.99 one-time. Selling plan "Deliver every 4 weeks, $16.00 off" gives $16.99 a month (48.5% off) |
| Shipping Protection | $3.50 |
| Inventory tracking | Off for all products |
| Discounts | None created (checked earlier) |
| Cart logic | Custom code in your PDP (`ninuAdd()`, side cart, refill toggle) |

Landed cost for one kit is $13.50 (supplier sheet), so margin is **$34.74 per kit order** after card fees. That is your break-even CAC (about £26.72).

## 2. Three things to fix or confirm first

**a. The oil bottle in your images may not match what ships.** The earlier supplier sheet showed the real oil in a dropper bottle in a green rosemary-oil box. Your flat-lay image shows a screw-cap bottle labelled "Ninu Scalp Oil". A product image that doesn't match what the customer receives is a refund and chargeback risk, and it damages trust right where you are trying to build it. Your instinct to fix it is right. Steps:
1. Ask the supplier for photos of the exact bottle and box, or order one sample. (Message in section 8.)
2. Ask whether they offer custom labels. If they don't, your page images must show their bottle as it arrives.
3. Then I'll write a prompt that reproduces that bottle. The label text must be added afterwards in HTML, because generators garble label words.

**b. "Rosemary essential oil" is not the same as "rosemary scalp oil".** Your product is titled "Rosemary Essential Oil Refill". Pure essential oil is normally diluted before it goes on skin. If what ships is rosemary oil already blended in a carrier oil, "rosemary scalp oil" is accurate and safer wording. If it is neat essential oil, labelling it as a ready-to-use scalp oil would be wrong. Get the ingredient list from the supplier before you rename it. Also add a patch-test line and a "check with your doctor if you're nursing or pregnant" line, because your buyers are postpartum.

**c. Can the supplier send castor and batana oil, in the same parcel?** Unknown. Separate parcels can cost more than the gift is worth.

## 3. The recommended offer: one free gift, plus a paid oil bundle

Keep the price. The kit stays $49.99, so AOV doesn't drop. A free gift lowers margin per order, not AOV, and it isn't a discount, so it fits your mentor's Q4 advice.

**Front end, on the page (converts more people): Kit + free Batana oil.**

- Gift: a small batana oil, not castor. Your own copy and your buyers' words say "I had the castor oil" and "castor oil and a shower cap." She already owns castor, so castor as a free gift has low perceived value. Batana is the one she probably hasn't tried.
- Message to keep in mind: your winning copy says "works with the oil I already had." A free oil gift doesn't contradict it, as long as the gift is framed as a bonus to try and not as something she needs.
- Show it as a bonus line in the kit card: "Free with your kit: batana oil, 30ml" (size depends on the quote).
- Price shown in the copy as "worth $X" only if you also sell it separately at $X. Give it a real product page and price. Fake "values" are a compliance risk.

**Back end, in the cart (raises AOV): the Oil Trio.**

- Rosemary, castor and batana in 60ml each at a bundle price. Offer it in the side cart as an add-on after the kit is in the basket.
- Fits your "maybe the oil" idea: more oil, no extra dispensers or bonnets.
- Needs separate product pages for castor and batana so the comparison price is real.

Here are the pieces side by side:

| Piece | Where | Job |
|---|---|---|
| Free batana gift | PDP and kit card | Conversion (the add-to-cart leak) |
| Oil Trio add-on | Side cart | AOV |
| Refill subscription | Side cart | Lifetime value |
| Post-purchase offer | After payment | AOV with no friction |

## 4. What the free gift costs you

Gift cost = landed cost of the gift plus any extra shipping. I don't have the number, so here are scenarios. The last column is how much more often people must buy for you to be no worse off per click.

| Gift cost | Margin per kit order | Break-even CAC | Conversion lift needed to stay level |
|---|---|---|---|
| $0 (today) | $34.74 | £26.72 | none |
| $4 | $30.74 | £23.65 | +13% |
| $6 | $28.74 | £22.11 | +21% |
| $8 | $26.74 | £20.57 | +30% |

A gift that costs about $4 to $6 needs conversion to rise 13% to 21% to pay for itself. If the page converts at 0.7% today, that's 0.8% to 0.85%. That's a realistic ask for a strong offer. A gift above $8 makes the maths hard at your current CAC.

(Break-even CAC converted at $1.30 to £1, as before.)

## 5. The subscription: "50% off" for Black Friday

Today: $32.99 one-time, subscription $16.99 (selling plan "$16.00 off"). I read your request two ways:

| Option | Price | Cost to you | My view |
|---|---|---|---|
| A. True 50% off one-time price, labelled Black Friday | $16.49 a month ($16.50 off) | $0.50 a month | Do this. It is honest, it matches the label, and it costs almost nothing |
| B. Half of the $16.99 | $8.50 a month | $8.49 a month | Don't, unless the supplier quote shows oil + shipping + fees come in under about $7.95 (the break-even after card fees). Every renewal is a repeat loss risk |

Two checks: (1) the first refill ships with the kit order, which means two bottles in the first parcel. Confirm that is intended, because you pay for that second bottle immediately. (2) The sale label should end on the same date as the kit sale (Nov 10) and the plan should go back to $16.99 after.

## 6. Do you need Kaching?

Short answer: not yet, for two reasons.

1. **Your PDP is custom code.** Theme-app widgets (bundle blocks, quantity breaks) are built for standard theme templates. I can't confirm Kaching Bundles would render inside your Custom Liquid page and custom side cart, and getting that wrong costs you a day of fixing. The free gift can be done in your own code: add the gift line with the kit, and a Shopify automatic discount makes it free. That is free to build.
2. **Volume is tiny.** At under about one order a day, an app that raises AOV by $10 to $60 on some orders adds a few dollars a day. Worth building, but behind fixing the conversion leak.

What the apps do, from their listings (pricing from third-party sources and the app pages, please check the live listing):
- **Kaching Bundles:** bundles, free gift with purchase, buy-X-get-Y. Free to install, paid plan from about $14.99 a month.
- **Kaching Post Purchase Upsell:** a separate app. One-click offers after payment. About $4.99 a month for up to 99 orders, with a 14-day trial. Post-purchase offers don't show for every payment method, so expect some orders to skip it (this matters with PayPal, which you are sorting out).

If you want one app, the post-purchase one is the better fit. It runs in checkout, outside your theme, so your custom page doesn't break it, and it's cheap.

## 7. Build order (cheapest and highest-impact first)

1. Supplier answers: oil photos and ingredients, castor and batana costs, parcel consolidation, custom labels. **Blocks everything below.**
2. Fix the oil images and the product title so they match what ships.
3. Free batana gift (new product, free via automatic discount, added by `ninuAdd()`), shown in the kit card. Update ad copy to mention it.
4. Subscription Option A and the Black Friday label.
5. Oil Trio add-on in the side cart, with real separate product prices.
6. Post-purchase upsell, once orders are flowing (more than a few a week).

Testing note: step 3 changes the offer and the R16 copy test changes the copy. Don't run them in the same window, or you won't know which one moved add-to-carts.

## 8. Message to the supplier (WANB-US)

> Hi, I'm planning to add two oils to my Ninu kits and need some details:
> 1. Photos of the exact rosemary oil bottle and box that ship with the kit, and the full ingredient list. Is it pure rosemary essential oil or rosemary oil blended in a carrier oil?
> 2. Do you supply castor oil and batana oil (30ml and 60ml)? Ingredient lists, landed cost per unit for US dropship, and photos.
> 3. Can they ship in the same parcel as the kit? What does the extra weight add to shipping?
> 4. Do you offer custom labels or private label on the oils?
> 5. Stock levels, lead time, and any safety data sheet or test report you can share.

## 9. One thing that will undercut any offer

The PDP still shows named reviewers (Rachel M., Amara T., Jenna K.) with split hairline images that look AI-generated. An irresistible offer on a page with unverifiable testimonials is a risk: fake reviews and fabricated before-and-after images are enforced against by the FTC and by Meta. I've flagged this before and you chose to keep "Trusted by 10,000+ women". These specific named cards with images are a bigger exposure. I'd remove them before spending more on traffic.

## 10. What I can do for you next

- Write the supplier-matched oil bottle prompt as soon as you have the photo.
- Write the PDP code change for the gift line and the side-cart add-on, and the selling-plan update for Option A. I will not change anything in Shopify until you say so.
- Draft the new offer copy for the R16 and R17 ads once you've chosen the gift.
