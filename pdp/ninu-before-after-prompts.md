# Ninu — Before/After Testimonial Image Prompts (6 total, 2 per card)

Written under the **Phase 5: Native Image Psychology** framework, adapted for testimonial pairs. The core rules still hold — POV from her own eyes, phone-camera quality, honest bathroom/bedroom light, no glamour lighting, no product visible, no face performing emotion. What changes for testimonials: the *hair itself* has to be visible enough that the difference reads instantly, so we shoot overhead crown-and-hairline angles (which show the transformation without needing a full face).

**Test:** would this pair look at home on a friend's camera roll if she'd taken one photo at month 2 and another at month 5?

**Match rules across every before/after pair (critical, or the pair reads as fake):**
1. Same person (same hair color, texture, skin tone, hairline shape).
2. Same angle and framing (overhead crown POV, or 45° temple close, held roughly the same distance).
3. Same lighting conditions (same room, same time of day, same window direction).
4. Same background context visible at the edges (same tile, mirror frame, towel, ceramic mug).
5. The only thing that changes is the hair itself.

**Model:** written for Nano Banana Pro. Generate the **before** first, then feed it as reference for the **after** and prompt only the change (regrowth density, baby-hair blending, temple fill-in).

**Aspect ratio:** 1:1 square. The PDP cards display them side by side in a 1:1 grid.

---

## Card 1 — Rachel M. · temple hairline
**Story:** Month 2 thin temples → Month 5 filled-in fuzz turning into real hair.

### 1A — BEFORE (Month 2)
Amateur smartphone photo, first-person POV in a bathroom mirror. Frame is tight on a woman's right temple: dark auburn hair pulled back into a low bun, exposing the temple hairline. Visible postpartum thinning — sparse short wispy hairs, a see-through half-moon patch of scalp behind the temple. Skin slightly flushed, no makeup, faint under-eye shadow. Warm bathroom vanity light from above, mirror lightly speckled with toothpaste flecks, a cream-colored linen towel blurred in the background. Slightly out of focus at the edges, real phone-camera grain. No face expression — the eye is out of frame above the eyebrow. Documentary, honest, unflattering. 1:1 square.

### 1B — AFTER (Month 5) — use 1A as reference
Same person, same angle, same bathroom mirror, same warm vanity light, same cream linen towel blurred in the background. Frame tight on the same right temple, hair pulled back into the same low bun. This time the temple hairline is visibly denser — a soft layer of new baby hairs about 1–2 inches long has grown in across the previous thin patch, no longer see-through, edges softer and more filled. Skin still no makeup, honest lighting. Same phone-camera grain, same slight edge blur. Only the hair has changed. 1:1 square.

---

## Card 2 — Amara T. · crown and part line
**Story:** Week 1 wide part with visible scalp → Month 4 denser coverage.

### 2A — BEFORE (Week 1)
Overhead first-person POV of a woman's own crown, phone held high, looking straight down at the top of her head. Dark coily hair parted cleanly down the middle. The part line is wide — a visible strip of warm brown scalp shows through, especially at the crown where postpartum shedding has thinned coverage. Cream duvet edge in the bottom of the frame, morning bedroom light from the left, no makeup, honest. Slightly grainy, taken quickly, no styling. Photorealistic, no filter, no glamour. 1:1 square.

### 2B — AFTER (Month 4) — use 2A as reference
Same overhead POV of the same woman's crown, same dark coily hair, parted down the middle in exactly the same place, same cream duvet edge in the frame, same morning bedroom light from the left. This time the part line is visibly narrower — the previously wide strip of scalp is now mostly filled in with denser hair growth along both sides of the part, especially at the crown. Same phone-camera quality, same honest lighting. Only the density has changed. 1:1 square.

---

## Card 3 — Jenna K. · baby-hair halo along the front hairline
**Story:** Month 3 unruly baby-hair halo sticking straight up → Month 6 baby hairs blended into a fuller front hairline.

### 3A — BEFORE (Month 3)
Amateur smartphone selfie POV in a bathroom mirror, mid-length light brown hair pulled back into a loose ponytail. Frame tight on the front hairline. A halo of short, fine baby hairs sticks straight up and out along the entire front hairline, resisting the pulled-back style — some flattened by sweat, most sprung upward in every direction, catching the overhead bathroom light. No makeup, honest morning light, ceramic mug of coffee out of focus on the counter behind. The eye is barely in frame above the eyebrow. Slightly greasy, unstyled, phone-camera grain. Documentary. 1:1 square.

### 3B — AFTER (Month 6) — use 3A as reference
Same person, same bathroom mirror, same overhead light, same ceramic mug blurred behind, same mid-length light brown hair pulled back into a loose ponytail. Frame tight on the same front hairline. This time the baby hairs along the hairline have grown longer and integrated into the main hair — the frizzy halo has settled into a soft, fuller front hairline, still natural and slightly imperfect, no gel or styling product visible. Same lighting, same no-makeup honesty, same phone-camera grain. Only the hair has changed. 1:1 square.

---

## Workflow

For each card:
1. **Generate the BEFORE first**, text-only, iterate until the person, angle and background feel right.
2. **Save that image.** It becomes your visual reference for the AFTER.
3. Feed it into Nano Banana Pro as image reference, along with the AFTER prompt. Only the hair should differ.
4. Save both, upload to Shopify Files, and paste the URLs into the PDP placeholders:

| Card | Placeholder | Path in PDP |
|---|---|---|
| 1 Before | `BA1_BEFORE_URL` | Rachel · Month 2 |
| 1 After  | `BA1_AFTER_URL`  | Rachel · Month 5 |
| 2 Before | `BA2_BEFORE_URL` | Amara · Week 1 |
| 2 After  | `BA2_AFTER_URL`  | Amara · Month 4 |
| 3 Before | `BA3_BEFORE_URL` | Jenna · Month 3 |
| 3 After  | `BA3_AFTER_URL`  | Jenna · Month 6 |

---

## Compliance note (please read before running these on Meta)

Generated before/after images sit in a grey area for Meta ad policy and FTC endorsement rules. Meta has been increasingly strict on synthetic testimonials — especially in beauty and hair regrowth — and can strike the ad account for undisclosed AI-generated results.

Two safer paths:
1. **Get real UGC.** Offer 3 free kits to postpartum moms in exchange for month-1 and month-4 crown photos with a signed release. Use those instead. The quotes you have on this PDP are already placeholders — real customers will give you real quotes at the same time.
2. **If you must use these:** never claim they're real customer results. Frame them as illustrative ("Here's what regrowth typically looks like") or watermark them "Illustration" in small type in the corner. Do NOT put fake customer names on generated photos anywhere the ad reads as a testimonial. The card copy in the PDP currently uses names (Rachel, Amara, Jenna) — swap these for real names when you have real photos, or remove the names entirely and label the cards "Typical month-by-month progress" for now.

I'd start with option 1. Even 3 real UGC pairs beat 30 generated ones for both trust and legal safety.
