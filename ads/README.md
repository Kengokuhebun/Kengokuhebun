# Ninu — Meta Ads Manager Bulk Import (Launch Campaign)

**File:** `ninu-meta-cbo-launch.csv` — a Meta Ads Manager bulk import ready to load.

## What's in the file

- **1 campaign:** `Ninu | Launch | CBO | US | Purchase`
  - Objective: **Sales** (`OUTCOME_SALES`)
  - Buying type: **Auction**
  - CBO daily budget: **$50/day** (change to yours — the value is on the first row, in cents: `5000` = $50)
  - Special ad categories: **None**
  - Bid strategy: **Lowest cost** (highest volume for the budget)
  - Status: **PAUSED** (nothing spends until you turn it on)
- **5 ad sets, one per angle:**
  1. `AS1 - Ritual-Upgrade`
  2. `AS2 - Temple-Rescue`
  3. `AS3 - Not-A-Pill`
  4. `AS4 - Regrowth-Companion`
  5. `AS5 - Root-Cause`
  - Optimization: **Purchase conversions**
  - Countries: **US only**
  - Age: **25–44**, gender: **women**
  - Placements: **Advantage+** (Meta chooses across FB, IG, Reels, Stories, etc.)
  - Advantage+ Audience: **On** (Meta will treat your interest list as a suggestion, not a hard limit)
  - Detailed targeting: 3–4 interests per set, matched to the angle (e.g. AS3 gets `Postpartum;Motherhood;Wellness;Prenatal vitamins`)
- **15 ads, 3 per ad set:**
  - Body (primary text): the full longform copy for that sub-desire, hook included
  - Headline: a short one-liner matched to the angle
  - Link description: `Free US shipping · 30-day guarantee`
  - Destination: `https://ninu.com/products/the-ninu-kit` — change if your handle is different
  - CTA button: **Shop Now**
  - UTM parameters preset: `utm_source=facebook&utm_medium=paid-social&utm_campaign=ninu-launch-cbo&utm_content={{ad.name}}&utm_term={{adset.name}}`
  - Image / video slot: **blank** — you'll attach these in Ads Manager after import

## Before you import — three things to check

1. **Change the destination URL** if `ninu.com/products/the-ninu-kit` isn't right. Do a find/replace in the CSV before uploading.
2. **Change the budget** if $50/day isn't what you want. Find `5000` in the `Campaign Daily Budget` column (row 2 of the CSV) and replace with your daily budget in cents ($30/day = `3000`, $100/day = `10000`).
3. **Confirm the Meta Pixel is installed on `ninu.com`** and fires the `Purchase` event on order-confirmation. Without this, the "Optimization Goal: OFFSITE_CONVERSIONS" won't work and ads will spend without learning. Check in Meta Events Manager → Test Events.

## How to import

1. Ads Manager → top-left menu → **Ads** → **Import**
2. Upload `ninu-meta-cbo-launch.csv`
3. Meta will validate the file and show a preview:
   - **Green rows** → import as-is
   - **Yellow / red rows** → Meta flagged something. Common fixes below.
4. Click **Publish** to create everything (still paused).
5. Go into each ad set individually and confirm the **interest targeting** — Meta will try to auto-match my interest names to real interest IDs. Verify each set has the intended interests (or replace them with something closer if the auto-match missed).
6. For each of the 15 ads, add the creative:
   - AS1 (Ritual-Upgrade) → your 3 Ritual-Upgrade PNGs from `creatives/png/Angle1_Ritual-Upgrade/`
   - AS2 → `Angle2_Temple-Rescue/`
   - …and so on
   - Each ad slot in Meta can hold multiple images if you want to run image-carousels; or keep 1 image per ad and let Meta serve each ad in its most-appropriate placement.
7. Once creatives are attached, toggle the campaign live.

## Common Meta import errors and fixes

| Meta says | What it means | Fix |
|---|---|---|
| "Ad set must have creative attached" | You clicked Publish before adding images | Add images in the Ads Manager UI, then republish |
| "Detailed targeting: interest not found" | Meta didn't match the interest name | Delete the flagged interest and pick the closest match from the suggestion dropdown |
| "Special ad category required" | Meta thinks this touches health | Set to **NONE** (already done in the file) — if Meta still forces it, change to "Employment/Housing/Credit" is wrong; you'd only add if targeting one of those. For beauty, **NONE** is correct — reply in the import dialog and try again |
| "Placement not supported by Advantage+" | Rare — usually a valid placement | Turn Advantage+ off and manually pick Facebook Feed + IG Feed + IG Reels + Stories |
| "Pixel not found" | The pixel isn't attached to your ad account | Business Settings → Data Sources → Pixels → connect your Ninu pixel to this ad account |

## Post-launch playbook (once live)

**Day 1–3 (learning phase):**
- Don't touch anything. Meta needs 50+ purchase events per ad set to exit learning. Constantly editing resets the learning phase.
- Check twice a day: is the pixel firing? Is spend pacing to budget?

**Day 4–7 (first read):**
- Look at ROAS, CTR, CPC, hook rate (3-sec video views / impressions if you go video later), and cost per purchase per ad
- **Kill any ad that spends 2× your target CPP with 0 purchases.** For a $49.99 AOV product with ~66% GM, target CPP is ~$25–33. So kill any ad above ~$60 spend with no purchase.
- **Kill any ad set** where all 3 ads are under-performing — the audience isn't right
- **Duplicate winners** (ROAS >1.5) into a scaling ad set at 2× the budget

**Day 8+ (scaling):**
- Consolidate: if AS3 is your winner, kill 2 losing sets, put their budget into AS3 (still CBO, so this just happens as Meta reallocates)
- Angle-test what's next: rotate in the confessional-format creatives if you started with Reddit-style, or vice versa
- Never increase a working ad set's budget by more than 20% in 48 hours — steeper hikes reset learning

## What I need from you if we're iterating this file later

- Real numbers after 3 days (CTR, CPC, CPP, ROAS per ad set)
- Which angles won and which flopped
- The winning creative format (Reddit vs confessional vs before/after split)
- I'll then generate v2 of this file — kill the losers, add scaling sets, and rotate new hooks
