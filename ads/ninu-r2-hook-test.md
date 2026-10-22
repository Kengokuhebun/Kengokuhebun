# R2: Hook isolation test (R1-A winner → 5 new hooks)

Mentor directive after R1-A converted:
1. Extract the angle + desire from the winner.
2. Hold everything else constant and test only the hook.
3. New ad set with the control + 5 variations.

After the hook winner is called, next phases are: image test, then advertorial.

---

## 1. Angle + desire extraction from R1-A

| | |
|---|---|
| **Angle** | *The oil wasn't failing. The delivery was. You've been oiling the wrong thing.* A dropper or fingers can't reach the scalp through hair — gravity sends the oil to the shaft, the neck and the towel. Hollow silicone tips press through the part and release the oil on the scalp skin directly. **New mechanism, not new ingredient.** |
| **Desire** | To feel in control of her postpartum body again. To finally be *doing it right* after months of consistency with no return. To be exonerated: it wasn't her discipline that was failing, it was the tool. |
| **Awareness level (BTA)** | **3** — knows the problem (postpartum shedding) and the solution category (scalp oiling). Doesn't know our tool or the delivery mechanism. |
| **Sophistication level (BTA)** | **3** — ingredient claims are exhausted. A new mechanism is the only thing that cuts through. |
| **Core emotional driver (consistent across all hooks)** | Shame of invisible effort → relief of exoneration. "I was never the problem. The method was." |
| **Rule of One** | *The oil wasn't reaching the scalp.* |

The 5 new hooks below enter this same angle from 5 different emotional doors. Everything else — image, body, headline, link description, CTA, URL — stays identical.

---

## 2. The six ads (control + 5 variants)

### Hook A — CONTROL (R1-A winner)
*Entry: specific moment in a private ritual.*

> Month five postpartum. Before I check my phone, before I check the baby monitor, I'm at the bathroom mirror pressing my hair back to check my temples.
>
> Not checking like I was admiring myself. Checking like I was scared of what I'd see.

### Hook B — Confession
*Entry: shame-forward self-indictment. Great Leads: proclamation.*

> I spent two months oiling my scalp every single night postpartum. The only thing that changed was my pillowcase.
>
> Not a joke. Not the setup for one. Just the quiet result of doing the work every night and seeing nothing.

### Hook C — Direct address + filter
*Entry: hard filter so the only clicks are the exact avatar. AARREIGN rule 1 applied literally.*

> If you're four months postpartum, oiling your scalp every night, and still can't see a change — read this before you buy another bottle of anything.
>
> I was you two months ago. I thought I was doing it right. Here's what nobody told me.

### Hook D — Evidence / timestamp
*Entry: hard data as the thumb-stopper. Phase 5: "the evidence no one else sees."*

> 62 nights of castor oil. About $84 spent. Zero change at my temples.
>
> Not a dramatic failure. A quiet one. The kind where you keep going because you're sure you'll see it eventually.

### Hook E — Worst-part reframe
*Entry: name the hidden emotional cost. Master Doc "worst part isn't X, it's Y" move.*

> The hardest part of postpartum hair loss isn't the shedding.
>
> It's being consistent for two months, doing everything right every single night, and watching nothing happen.

### Hook F — Dialogue (per AARREIGN: dialogue not reported speech)
*Entry: in-scene conversation. Lets the reader hear the problem, not be told about it.*

> "You've been in there forty minutes."
>
> My husband at the bathroom door, 10pm. I had been. Castor oil, rosemary, scalp massage. Every single night since the shedding started. He didn't understand why nothing was changing.

---

## 3. Shared body (identical on all six ads, starts right after the hook)

> I'd been doing the scalp oil routine since the shedding started. Castor oil every night. A little rosemary mixed in. I sat on the edge of the tub, worked through every section, thirty minutes. I never skipped. I was the most consistent I'd been about anything since having the baby.
>
> Six weeks of that. Nothing changed.
>
> So I went through the checklist. More protein. Iron. Collagen powder. New biotin gummies. I watched videos about scalp massage technique. I told myself I probably just needed more time.
>
> What I hadn't thought to check was where the oil was actually going.
>
> Here's what nobody told me. When you tip a dropper over your hair, the oil lands on top of the shaft. Your scalp is buried underneath, under all that length. The oil spreads across the hair, runs down your neck, soaks into the towel on your shoulders. Some of it makes it through eventually. Most doesn't. You've been doing the work every night and most of the product is ending up on cotton.
>
> I'd been massaging my hairline for two months with oil that barely touched the skin I was trying to treat.
>
> The thing that changed it is embarrassingly simple. A dispenser with hollow silicone tips at the head. You part the hair, press the tips flat against your scalp, and the oil releases right there. Not on top of the hair. Not into the towel. On the scalp. On the skin. The chamber is clear with 1 to 4ml markings on the side so you can see exactly how much goes in. One hand, no drips, about three minutes from start to done.
>
> The first night I used it I could actually feel it reaching the scalp. By the end of that first week I'd cut the routine from thirty minutes to four. A few weeks in, I stopped doing the anxious morning check. I don't call that a result, hormones are still doing what they're doing, but the routine I'd been getting wrong for two months I was finally getting right.
>
> The Ninu Kit comes with the dispenser, 60ml scalp oil, and a satin bonnet for $49.99. Free US shipping and a 30-day money-back guarantee. If it doesn't change how your routine feels, send it back.
>
> You try it, you fill it with the oil you already trust, you press the tips against your scalp, and you feel the difference on the first use. You stop guessing where it's going. You stop standing at the mirror every morning.
>
> You don't, month six looks like month five. The oil keeps going on the towel.
>
> Try the Ninu Kit risk-free for 30 days.

Everything downstream of the hook is **identical** on all six ads. That is what makes this a hook test.

---

## 4. Ad set structure (what to import)

- **Campaign:** same as R1 (`Ninu | R1 Validation | ABO | US | Purchase`). ABO stays. Objective stays `OUTCOME_SALES`, optimized for `PURCHASE`.
- **New ad set:** `Hook Test | Postpartum Moms | US | Broad | Adv+ Placements`
  - Daily budget: **$150** (so each of 6 ads averages ~$25/day — enough signal to call a winner)
  - Audience: US, women, 25–44, broad, Advantage+ audience on
  - Placements: Advantage+
- **6 ads**, all paused on import, all using:
  - **Same image:** the native bathroom-mirror image that won on R1-A (the one you shared today)
  - **Same headline:** `Oil for your scalp, not your towel`
  - **Same link description:** `Free US shipping · 30-day guarantee`
  - **Same CTA button:** `Shop Now`
  - **Same URL:** `https://tryninu.store/products/the-ninu-kit` (if the domain is live by import time; otherwise the myshopify URL)
  - **Same UTM:** `utm_source=facebook&utm_medium=paid-social&utm_campaign=r2-hook-test&utm_content={{ad.name}}`

The only variable is the hook (first 1–3 lines above "See more" in Meta's rendering).

---

## 5. Kill rules + what to look for

During the test, read **link CTR** and **link CPC** per ad separately from "all" CTR/CPC (mentor's instruction). Also watch per-ad funnel: spend → impressions → link clicks → landing page views → ATC → IC → purchases.

| Trigger | Action |
|---|---|
| Ad has $40+ spend and link CTR is < 50% of the control's link CTR | Pause that ad |
| Ad has $80+ spend and 0 purchases while control (or another ad) has 1+ | Pause that ad |
| End of day 3, every ad still alive | Call the winner by CPA. On tie by CPA, break on link CTR (hook strength isolates there). |

Max total exposure for this test: **$450** ($150/day × 3 days).

Do not edit any ad mid-flight. Any iteration happens after the kill checkpoint, with the mentor.

---

## 6. The roadmap after this test

**Phase 2 — Image test.** Winner hook stays. Winner body stays. Test the current image against 3–4 variants of the same Phase 5 scene (different angle on the same temple shot, different person doing the same action, overhead crown instead of temple, different time of day). Same ad set structure, 1 variable: the image. Budget framework repeats.

**Phase 3 — Advertorial.** If post-click conversion is the bottleneck (ATC/IC/Purchase drop-off even on a winning hook + image), build an advertorial as the landing page between ad click and PDP. The advertorial reuses the winning hook and the long-form body, extends the mechanism explanation, embeds the before/after cards, and ends with the CTA to the PDP. New ad variant: same hook, link now goes to the advertorial URL (`/pages/why-your-scalp-oil-isnt-working`) instead of the PDP. A/B advertorial-vs-direct-PDP across the same hook.

---

## 7. Pre-launch checks

- **Image.** The one you shared today matches the Phase 5 prompt in `creatives/ad-a-native-image-prompt.md` cleanly. **Lock it as the control image for all 6 ads** — otherwise this isn't a hook test, it's a hook + image test. If Meta flags the image for personal attributes, the softer temple-only crop is the fallback (same POV, less visible scalp).
- **Domain.** If `tryninu.store` is live, the Link column uses that. Otherwise fall back to the myshopify URL and swap after SSL provisions.
- **Attribution.** The one R1 sale came from the short-form Ad A body. This R2 test uses the long-form body from `ninu-r1-long-form.md`. That means the hook test is also telling you something about short-vs-long body length — note that when reading results.
- **Pixel.** Confirm the `Purchase` event fires correctly on the first R1 sale (Events Manager → event history). If it didn't, the R2 optimization data starts cold.
