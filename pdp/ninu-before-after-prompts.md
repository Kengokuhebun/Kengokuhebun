# Ninu — Before/After Split Image Prompts (3 total, one split image per card)

Written under the **Phase 5: Native Image Psychology** framework, adapted for split-image testimonials. Each prompt produces a single side-by-side image (BEFORE on the left, AFTER on the right) with the woman wearing different clothes on the AFTER side so time visibly passes between the two frames.

The core Phase 5 rules still hold: POV from her own eyes or an honest overhead crown angle, phone-camera quality, real bathroom/bedroom light, no glamour lighting, no styling, no product visible.

**Test:** would this split look at home in a "3 months later" post on a friend's Instagram story?

**Consistency rules baked into every split (critical, or the pair reads as fake):**
1. Same person on both sides (same hair color, texture, skin tone, hairline shape, face shape when visible)
2. Same angle and framing (both sides shot from the same distance and viewpoint)
3. Same room and lighting conditions (same bathroom or bedroom, same window direction, same time of day)
4. **DIFFERENT clothing on the AFTER side** (a different top, sleeve, or fabric visible at the edge of frame — the visual cue that time has passed)
5. The change: hair is visibly denser or more filled in on the AFTER side. Nothing else beauty-related changes (no new makeup, no different styling).

**Model:** written for Nano Banana Pro. Ask it explicitly for "a single side-by-side image, before on the left, after on the right, same person, different top on the right." A thin white or matching-color gutter (2–4px) between the two halves helps the split read clean.

**Aspect ratio:** 2:1 (landscape) so each half is 1:1. Suggested output: 2048×1024. The PDP cards display this full split image.

---

## Card 1 — Rachel M. · temple hairline (Month 2 → Month 5)

A single side-by-side split-image amateur smartphone photo (before left, after right, thin 3px white gutter between them), both halves shot in the same bathroom mirror from the same first-person POV at the same distance and framing. Same person in both: a woman with dark auburn hair pulled back into a low bun, tight framing on her right temple hairline. Same warm vanity light from above, same faintly toothpaste-flecked mirror, same cream tile visible at the edges.

LEFT side (Month 2 / BEFORE): She wears a soft grey cotton crewneck t-shirt, sleeve visible at the shoulder edge. Her right temple shows visible postpartum thinning — sparse wispy hairs, a see-through half-moon patch of scalp behind the temple. No makeup, faint under-eye shadow, skin slightly flushed.

RIGHT side (Month 5 / AFTER): She wears a **rust-colored ribbed knit sweater**, different fabric texture and neckline visible at the shoulder edge — the clear visual cue that months have passed. Same right temple, now visibly denser: a soft layer of new baby hairs about 1–2 inches long has grown in across the previously thin patch, no longer see-through, edges softer and filled. Same honest lighting, same no-makeup skin. Only the hair, and her top, have changed.

Both halves photorealistic, phone-camera grain, no filter, no glamour lighting, no beauty retouching. 2:1 landscape aspect ratio, 2048×1024.

---

## Card 2 — Amara T. · crown and part line (Week 1 → Month 4)

A single side-by-side split-image amateur smartphone photo (before left, after right, thin 3px white gutter between them), both halves shot overhead first-person POV with the phone held high, looking straight down at the top of the same woman's own crown at the same distance and framing. Same person in both: dark coily hair parted cleanly down the middle, warm brown skin, same cream duvet edge visible in the bottom of both frames, same morning bedroom light from the left window.

LEFT side (Week 1 / BEFORE): She wears a **black sleeveless tank top**, thin strap visible on her shoulder near the bottom of frame. The part line is wide — a visible strip of warm brown scalp shows through, especially at the crown where postpartum shedding has thinned coverage. No makeup, honest morning light.

RIGHT side (Month 4 / AFTER): She wears a **soft sage-green long-sleeve robe or sweatshirt**, different sleeve and neckline visible at the edge — clearly a different day, months later. Same crown, same part line placement, but the part is now visibly narrower: previously exposed scalp is mostly filled in with denser hair growth along both sides of the part, especially at the crown. Same cream duvet edge, same morning light direction. Only the density, and her top, have changed.

Both halves photorealistic, phone-camera grain, no filter, no glamour, no styling product visible. 2:1 landscape, 2048×1024.

---

## Card 3 — Jenna K. · baby-hair halo along the front hairline (Month 3 → Month 6)

A single side-by-side split-image amateur smartphone selfie (before left, after right, thin 3px white gutter between them), both halves shot in the same bathroom mirror at the same distance and framing. Same person in both: a woman with mid-length light brown hair pulled back into a loose ponytail, tight framing on her front hairline. Same overhead bathroom light, same ceramic mug of coffee out of focus on the counter behind her.

LEFT side (Month 3 / BEFORE): She wears a **white waffle-knit henley top**, collar and one visible button at the neckline. A halo of short, fine baby hairs sticks straight up and out along the entire front hairline, resisting the pulled-back style — some flattened by sweat, most sprung upward in every direction, catching the overhead light. No makeup, honest morning light, slightly greasy hair.

RIGHT side (Month 6 / AFTER): She wears a **dusty pink cardigan** over a plain camisole, different neckline and softer fabric visible at the collar — clearly a different day, months later. Same front hairline framing, same ponytail. This time the baby hairs have grown longer and integrated into the main hair — the frizzy halo has settled into a soft, fuller front hairline, still natural and slightly imperfect, no gel or styling product visible. Same lighting, same mug in the background. Only the hair, and her top, have changed.

Both halves photorealistic, phone-camera grain, no filter, no glamour. 2:1 landscape, 2048×1024.

---

## Workflow

For each card:
1. **Generate the split image directly** — Nano Banana Pro handles diptych prompts natively when you give it the "side-by-side, before left, after right" instruction.
2. If the split doesn't come out clean (uneven lighting, different-looking person, missing gutter), iterate: emphasize "same person, same face, same angle" and "different clothing on the right side" more strongly.
3. As a fallback: generate the LEFT (before) alone at 1:1, then generate the RIGHT (after) alone at 1:1 using the LEFT as image reference plus the same identity + new-clothing instruction, and stitch them together in any image editor with a 3px white gutter.
4. Upload the final 2:1 split image to Shopify Files.
5. Paste each URL into the PDP placeholders (see below).

## PDP placeholders

The PDP now expects **one split image per card**, not two:

| Card | Placeholder | Person |
|---|---|---|
| 1 | `BA1_SPLIT_URL` | Rachel · Month 2 → 5 |
| 2 | `BA2_SPLIT_URL` | Amara · Week 1 → Month 4 |
| 3 | `BA3_SPLIT_URL` | Jenna · Month 3 → 6 |

---

## Compliance note (unchanged, please re-read)

Generated before/after images with fake customer names are a Meta ad-policy and FTC endorsement risk in beauty and hair regrowth categories. Safer paths:

1. **Recommended:** offer 3 free kits to real postpartum moms in exchange for month-1 and month-4 crown photos with a signed release. Use those and their real quotes.
2. **If you use generated images anyway:** remove the fake names, label the section "Typical month-by-month progress," or watermark the images "Illustration."
