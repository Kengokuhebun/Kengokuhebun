# R3: CPM refinement (post-second-sale, Ad C control)

Second sale came from the Ad C control (habit/consistency angle — "the habit was always
there, the routine just needed to be easier than the reason to quit"). This round does
not touch the copy or the angle. It isolates two presentation variables that affect CPM
and post-click conversion: **creative presentation** (text size + background color) and
**destination** (PDP vs advertorial).

No new hooks in this round. The angle, copy, and offer that have now converted twice stay
exactly as they are.

---

## Ad set 1 — Color test

**Variable:** background color only. Text size is bumped on all three (62px → 70px) and
held constant, so color is the single thing being compared between them.

| Ad | Background | Copy |
|---|---|---|
| OG-Orange-Large | Same orange→red→magenta gradient as the control | Identical to control |
| OG-Purple-Large | Blue→violet→magenta gradient (user reference) | Identical to control |
| OG-Green-Large | Sky blue→teal→green→gold gradient (user reference) | Identical to control |

Images: `creatives/png/R3-OG-Refined-Colors/OG-Refined-{A,B,C}__9x16.png`
Build script: `creatives/build-r3-og-refined.js`

All three point at the PDP (not the advertorial). Same hook, same lead, same body, same
CTA, same URL as the running control — only the creative file changes.

**Known gap:** none of the three is a *clean* before/after against the small-text
original, since the text-size change is baked into all three. If you want a true
control inside this ad set, add a 4th ad using the original (smaller-text) orange
creative. Otherwise you're comparing against the already-running original ad set as
an external baseline, which is valid but not a same-ad-set apples-to-apples read.

**Suggested budget:** $120–150/day across 3 ads (3–4 ads if you add the small-text
control) → ~$40/ad/day. 3-day read.

---

## Ad set 2 — Advertorial test

**Variable:** destination only (PDP vs advertorial). Creative and copy are identical to
the Ad set 1 orange variant.

| Ad | Creative | Destination |
|---|---|---|
| OG-Orange-Large → Advertorial | Same image as Ad set 1's orange | `https://tryninu.store/pages/why-your-scalp-oil-routine-never-sticks` |

Compare this ad's funnel (LPV → ATC → IC → Purchase) against the matching PDP-direct
orange ad in Ad set 1. Same creative and copy on both sides of the comparison — the only
difference is what's on the other side of the click.

**Advertorial file:** `pdp/ninu-advertorial.html` (new, not yet published to Shopify)

What it is: a Shopify Page (not a product page) that sits between the ad click and the
PDP. Built from the frameworks already applied to this campaign — reuses the exact
chiefed Ad C copy verbatim (`ninu-r1-long-form.md`), broken into editorial sections with
subheads so it reads like an article instead of an ad post:

- Hook + Lead → opens the piece, no subhead (matches how an article opens)
- **"The routine I could never keep up with"** → Failed Solutions (the stop/skip/restart pattern)
- Mid-article product card (compact, price + Shop Now) — this is the soft first CTA
- **"What was actually going wrong"** → Discovery + Mechanism
- **"What changed by week one"** → Product Timeline
- Pull-quote: *"The habit was always there..."* → the Rule of One, set off visually
- Before/after section — same 3 cards as the PDP, same images
- Final CTA block — offer stack, price, guarantee, big button

Compliance: carries a **"Partner content · Ninu"** disclosure in the top bar and a
plain-language footer disclosure, per FTC endorsement guidance for advertorial-style
pages tied to a brand.

**Attribution:** the page reads whatever UTM/query string the visitor arrived with (from
the ad) and automatically appends it to every outbound link to the PDP — no manual UTM
editing needed per campaign. Falls back to `utm_source=advertorial&utm_medium=onsite&utm_campaign=r3-advertorial-test` if someone lands with no query string.

**Before this ad goes live:**
1. Create a Shopify Page with handle `why-your-scalp-oil-routine-never-sticks`, paste
   `pdp/ninu-advertorial.html` into a Custom Liquid/HTML block on it
2. Confirm the published URL matches `NINU_PDP_URL` fallback logic in the page's own
   script (only matters if the domain changes)
3. View it live on mobile before turning the ad on — rendered previews in this repo
   look clean, but always check the real Shopify render

**Suggested budget:** $40–50/day, single ad. 3-day read, same kill-rule posture as prior
tests (pause if CPA is clearly worse than the PDP-direct version by day 2–3).

---

## Ad set 3 — New angle (later)

Not built yet. New native images + new copy from a freshly extracted angle/desire, once
you're ready. Flagged here only so this file's structure matches what you described.

---

## Pre-launch checklist

- [ ] Advertorial page created in Shopify and spot-checked live on mobile
- [ ] Color-test ad set: confirm whether to add the small-text original as a 4th ad
- [ ] UTM `utm_content` set per ad name on import (`og-orange-large`, `og-purple-large`,
      `og-green-large`, `og-orange-large-advertorial`) so results are readable per ad
- [ ] Pixel firing confirmed on the advertorial page too (same site-wide pixel should
      cover it, but verify a PageView fires there in Events Manager)
