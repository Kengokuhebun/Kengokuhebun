# Ninu: project handoff for a new chat (state as of 2026-11-06)

Read this file, then `ads/ninu-brand-context-for-organic-chat.md` (written Nov 2; it has the business, product, costs, avatar, winning angle and master-document rules). This file covers **what changed since Nov 2** and where everything is. If the two disagree, this one is newer.

**First action in the new chat:** the owner says this will be "a really big project" but has not said what it is. Do not start work. Ask what the project is, in one short message, and what outcome and deadline they want. Then plan before building.

## 0. How to work with this owner (learned in this session)

- Short answers. A recommendation, not a menu. Say what you are unsure of.
- **One best version, ready to paste.** The owner gets confused by multiple versions and long files. When asked for copy or prompts, give one version per item, in one clean file, and attach it.
- Ship, then report. Build the thing, test it (render it, check it), then say plainly what changed and what is still open.
- Honest claims only. No fake urgency, fake proof, invented customers or medical and hair-regrowth claims. Offer the true version of any tactic that would cross the line.
- Do not publish, spend money, message customers or upload to the store on the owner's behalf without being asked. The owner uploads assets to Shopify Files and sends the link.
- Never print or reuse any API key. A video-generation key was shared earlier; treat it as sensitive.
- New copy: no em dashes, no exclamation marks. Say "oiling my scalp", not "doing my scalp oil".
- Generated-image prompts must say the oil is a pale golden-yellow, clear rosemary-style oil (not dark, not motor oil). Image generators block prompts with bodies plus wet or see-through clothing; keep scenes to objects and hands.

## 1. State of the business (Nov 6)

- **Brand:** Ninu, postpartum scalp-oil dispenser, https://tryninu.store (Shopify Basic, USD). Owner is UK-based, sells to the US, spends in GBP.
- **The core problem:** ads get clicks but almost no add-to-carts. The leak is the page and the traffic quality, not checkout. The owner's theory is that ads attract content consumers, not buyers.
- **Current test (R16):** Ad C's body rewritten with buyer language, on the Hook3 image. Last read: about 65 sessions, 0 add-to-carts, too early to call. Checkpoints about £68, £100, 225 sessions. Planned end Nov 9. **Do not change the page during the test.** (The banner, gift images and video were added just before this handoff, so treat the page as of Nov 6 as the new baseline.)
- **Break-even:** CAC about $34.74 (about £26.72). Kill checkpoints: £14 with 0 link clicks, £28 with 0 add-to-cart, £42 with 0 checkout, £54 with 0 purchases.
- **Cash is thin.** Spend is about £40 a day for tests. Do not scale before CAC is under break-even for 7 or more days and the account is paid up.
- **PayPal:** two orders have been pending since Oct 25 (PayPal was not connected to Shopify at the time). Do not ship them until paid. Customer contact and a refund or recapture decision are still open.

## 2. The offer now (live on the PDP code, not yet pasted live)

- **Ninu Kit $49.99** (struck-through $62.49 compare price): dispenser, 60ml rosemary scalp oil, satin sleep bonnet. Free US shipping, 30-day guarantee.
- **Four free gifts shown in the gift block:** scalp massager, bedside pouch (caramel faux-leather cosmetic pouch), the guide "The Scalp Routine That Sticks", and the Ninu Night Tracker (web page). The massager and pouch must still be sourced and in the box. The guide and tracker need working emails.
- **Black Friday banner:** a red strip above the shipping bar, "Black Friday Sale" with "$49.99 kit + 4 free gifts". It appears only while the sale switch is on. The page also has a countdown to Nov 10, 11:59 PM Pacific and "Price goes to $62.49 on Nov 11". **This is honest only if the Shopify price and the page price really change on Nov 11.** The $62.49 must also have been a real recent price.
- **Pricing question:** the owner asked whether to drop the sale because add-to-carts stopped after it started. My advice: keep it until Nov 10 (the ads promise it), do not blame it without checking what else changed that day, then run a new real sale for Black Friday week Nov 24 to 30. A permanent discount only pays if it lifts conversion by more than about 36%, which they cannot measure at this volume.
- **Unit economics with gifts:** gift cost scenarios of $4, $6, $8 mean the offer needs about +13%, +21%, +30% conversion to pay for itself.

## 3. Where things are (all in the repo, branch `claude/new-session-o5o13k`)

| What | File |
|---|---|
| Product page code (Shopify Custom Liquid, limit 51,200 bytes; now about 50,500) | `pdp/ninu-pdp.html` |
| Gift assets, guide and tracker tile graphics | `pdp/gift-assets/` |
| Guide (9-page PDF and HTML) | `pdp/ninu-guide-scalp-routine-that-sticks.html` / `.pdf` |
| Night Tracker (self-contained page, localStorage) | `pdp/ninu-night-tracker.html` |
| How to paste, swap icons, set up the tracker and emails | `pdp/README-gifts-tracker-guide.md` |
| **Paste-ready copy, one version of each of 8 swipes** | `ads/ninu-swipe-copy-paste-ready.md` |
| **Native image prompts, one per swipe** | `creatives/ninu-native-prompts-per-swipe.md` |
| Current test copy (R16) | `ads/ninu-r16-buyer-language-adC.md` |
| Core copy resource (Breakthrough Advertising applied) | `ads/ninu-core-copy-resource-breakthrough-advertising.md` |
| After-the-test scale plan (stacking, CBO, cost caps, true scarcity) | `ads/ninu-r21-after-the-test-scale-roadmap.md` |
| Offer evolution and gift-stack docs | `ads/ninu-r19-offer-evolution.md`, `ads/ninu-r20-pdp-offer-stack.md` |
| Full consolidated swipe file (archive, 13 versions) | `ads/ninu-adapted-swipe-copy-all.md` |
| Kill criteria | `ads/ninu-kill-criteria.md` |

The product page's gallery slide 2 is a muted looping video hosted on Shopify (`cdn.shopify.com/videos/c/o/v/88726671c14c4e3c9a52243df1c0b3a6.mp4`). A lighter copy is in `pdp/gift-assets/ninu-in-use-720p-lite.mp4`.

## 4. Open items, roughly by priority

1. **Pasting the latest `pdp/ninu-pdp.html` into the live page** (the owner does this) and confirming the page shows correctly on a phone.
2. **Sourcing the gifts** (massager, pouch). Supplier quotes (the WANB-US message is in `ads/ninu-r19-offer-evolution.md`). Real photos of the pouch.
3. **Nov 11 price change** set up in Shopify, and the compare-at price must be a price really charged.
4. **Guide and tracker delivery:** upload the PDF to Files, host the tracker at `/pages/night-tracker`, set the order-confirmation email block, set up the `orders@` and `support@` aliases (done in Google Workspace and Shopify sender settings earlier; check).
5. **Oil naming and ingredients:** page says "60ml scalp oil"; the supplier's bottle is a MELAO-labelled rosemary essential oil (a trademark and honesty risk if sold as Ninu's own). Get the supplier's ingredient list and dilution (essential oil in a carrier).
6. **Remaining PDP gallery fixes:** slide 5 shedding line; slide 6 "Glide, don't scrub"; slide 9 old bottle and "$ value" labels; slide 10 "Hair doesn't absorb oil. Skin does." (flagged as an unsupported claim); slide 12 shipping 5 to 7 days (page says 6 to 12) and a weight conflict with slide 7; the hero caption says "EBOOK"; the hero's small label print is garbled.
7. **Reviews:** the three named reviewer cards (Rachel M., Amara T., Jenna K.) with AI-generated split images are the highest-risk item on the page. The "Trusted by 10,000+ women", "Made in the USA" and "Natural Ingredients" lines are unverified. The owner chose to keep "Trusted by 10,000+" against advice.
8. **Creative production:** generate the 8 native images from `creatives/ninu-native-prompts-per-swipe.md`; image prompts 5 and 8 were repeatedly blocked and rewritten (see the file).
9. **Guarantee window vs shipping time:** 30 days from delivery or from order? 6 to 12 day shipping makes this matter.

## 5. Tools the main session had

Shopify admin and analytics (ShopifyQL by `utm_content` ad ID), Google Drive and Gmail, Canva, a headless browser (Playwright), PIL, ffmpeg, a video pipeline script `creatives/kie_pipeline.py`. A new chat may or may not have all of them. Check before promising a task.

## 6. Do not

- Do not carry over any claim from the competitor swipes (they are structure-only teardowns).
- Do not add gift lines to ad copy until the gifts are in the box.
- Do not edit files in the main branch's `ads/`, `creatives/` or `pdp/` without saying so; the new chat should work in a new folder named for the project.
