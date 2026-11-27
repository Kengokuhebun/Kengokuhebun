# Google Ads build sheet: BFCM Search campaign (draft, 2026-11-27)

I cannot create this in Google Ads from here (no Google Ads connection). This is the exact build to enter by hand. Tags: [OBSERVED] seen directly, [INFERRED] reasoned, [UNVERIFIED] not confirmed.

## 1. Reality check
- Meta ads cannot be imported. Google uses its own formats; the Meta winners are reused as ASSETS (copy, offer, images, video), not copied as ads.
- Nothing can serve until: Google Ads account + billing, conversion tracking, and (for Shopping/PMax) Merchant Center approval, which can take days. [INFERRED] A Search campaign needs no product feed, so it is the only type that can realistically spend before Cyber Monday ends.
- New advertisers may be asked to verify identity/business, which can also take days. [UNVERIFIED]
- Storefront check (public pages, 2026-11-27): /policies/shipping-policy and /policies/terms-of-service returned 404; refund, privacy and contact pages returned 429 (rate limited, not verified). Google's Misrepresentation policy expects clear shipping, returns and contact information. Fix before spending. [OBSERVED 404s, UNVERIFIED cause]
- The store has no custom domain (x5a9bu-97.myshopify.com). Search ads can use it; Merchant Center may not. [UNVERIFIED]
- Shopify connector in this session is pointed at a different store ("Orava"), so I could not audit the Glowling admin.

## 2. Setup order
1. Create the Google Ads account. When it pushes "Smart campaign" or a goal wizard, choose Expert Mode / create without guidance. Decline auto-applied recommendations.
2. Shopify admin > Sales channels > Google & YouTube app > connect Google account, link the Ads account, enable conversion tracking (Purchase). Place a test order and confirm the conversion appears.
3. Add shipping, returns/refund and terms pages to the store.
4. Build the campaign below, paused, check, then enable.

## 3. Campaign
- Type: Search. Goal: Sales (website). Networks: Search only (untick Search Partners and Display expansion).
- Budget: £50/day. Run to end of Cyber Monday (set end date 2026-11-30).
- Locations: United States, Canada, Australia (matches Meta; NZ excluded, landed cost unconfirmed). Setting: Presence only (people in the location), not "presence or interest". Language: English.
- Bidding: Maximize clicks with max CPC cap £1.00. Switch to Maximize conversions after about 15-30 conversions (rule of thumb, not Google doc). [INFERRED]
- Audiences: add as Observation only, not targeting: In-market Toys and games; Affinity/Detailed: parents of toddlers and preschoolers. No remarketing list exists yet (starts building once the tag is live).
- Ad schedule: all hours (too little data to cut).
- Final URL: https://x5a9bu-97.myshopify.com/products/glowling-led-drawing-board
- Tracking template suffix: utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}

## 4. Ad groups and keywords (phrase and exact only; no broad match)
AG1 Product intent: [led drawing board], "led drawing board for kids", "light up drawing board", "glow drawing board", "neon drawing board for kids", "acrylic led drawing board", "led art board for kids".
AG2 Gift and screen-free intent: "christmas gifts for 5 year old", "gifts for 4 year old boy", "toys for 5 year old boy", "screen free toys for kids", "quiet time toys for kids", "toys to replace ipad".
Campaign negatives (phrase): free, diy, how to make, printable, template, svg, app, software, download, pdf, tablet, lcd writing, projector, wholesale, supplier, alibaba, aliexpress, jobs, adult, professional.

## 5. Responsive Search Ad (same RSA in both groups; character counts verified)
Headlines (max 30):
1. Glowling LED Drawing Board (26)
2. Buy 2, Get 1 Free (17)
3. Black Friday: Buy 2 Get 1 Free (30)
4. Ends Cyber Monday (17)
5. Free Tracing Book Included (26)
6. Neon Lines That Light Up (24)
7. Screen-Free Drawing Board (25)
8. No App. No Ads. No Autoplay (27)
9. Wipe Clean, Draw Again (22)
10. Sold Only On Our Website (24)
11. 30-Day Money-Back Guarantee (27)
12. Toy That Won't Go In Garage (27)
13. Kids' Light-Up Drawing Board (28)
14. Christmas Gift Idea For Kids (28)
15. Shop Black Friday Deals (23)
Descriptions (max 90):
1. Clear acrylic board that lights up from the base. Kids draw, lines glow. Wipe and repeat. (89)
2. Black Friday: Buy 2, Get 1 Free plus a free tracing book. Ends Cyber Monday. Shop now. (86)
3. No app, no ads, no autoplay. Comes with eight fluorescent markers and a USB cable. (82)
4. Sold only on our website. 30 days to send it back for your money if it is not for you. (86)
Rules: no exclamation marks, no superlatives, no invented claims. Every line is from the store or the offer. Pin nothing at first.

## 6. Assets
- Promotion asset: occasion Black Friday, "Buy 2, Get 1 Free", dates to 2026-11-30.
- Callouts: Buy 2 Get 1 Free; Free Tracing Book; Ends Cyber Monday; 30-Day Money Back; Screen-Free.
- Sitelinks: skip until separate pages exist (identical URLs risk disapproval).

## 7. Economics and stop rule
- Average order about £51.56 (V1 purchases). Breakeven ROAS US 1.74-1.76, CA 1.57-1.63, AU 1.57-1.92. Affordable CPA about £27-33.
- At £1.00 CPC, breakeven conversion rate is about 3-3.7%. At £1.50, about 4.6-5.5%. Meta LPV-to-purchase has been 7.5% on n=40; Search CVR is unknown. [UNVERIFIED]
- Stop rule: pause if spend reaches about £100 with no purchase, or blended ROAS is under 1.1 after about £150.
- Total exposure with Meta: CBO £90 + ABO £40 + Google £50 = about £180/day.

## 8. After the weekend
Merchant Center approved: Performance Max with the product feed, assets from the Meta winners (4:5 and 1:1 crops, the video uploaded to YouTube). Demand Gen with the video once conversion data exists.
