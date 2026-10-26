# R5 — Yap video: B-roll + voiceover demo (not the AI UGC avatar)

A different format from the avatar skill: three quick demo cuts (no face, hands/hair/product
only) under a separate, naturally-read voiceover built from the winning Ad C copy. Per the
Master Doc's Variation Winners rule, this is a **FORMAT TRANSLATION** — the locked angle
(habit problem, not hair problem), mechanism, and Rule of One line all carry over unchanged.
Nothing about the copy's substance is new here, only the medium.

**Revision log (2026-10-26):** first Grok test came back good quality but janky, with the
dispenser's shape drifting between Shot 2 and Shot 3 and not matching the real product despite
reference images being attached. Section 0.5 below and the rewritten Shot 2/3 prompts exist to
fix that specifically — see the note at the top of 0.5 for why it happened.

---

## 0. The three visual beats (as briefed)

| # | Shot | What it's doing |
|---|---|---|
| 1 | Standard dropper applicator on the front hairline/scalp edge, oil dripping messily down the side of the forehead | Visualizes the Failed Solutions beat |
| 2 | Cut to the Ninu applicator coming through a voluminous, parted section of hair | Visualizes the Discovery/Mechanism beat |
| 3 | Cut to the applicator's tips being pressed and moved in a small circular motion against the back of her hand | Visualizes the tactile "you can feel exactly where it's going" claim — a texture/precision demo, not a scalp shot |

Plus one **mom avatar reference frame** — a single higher-fidelity establishing shot of her,
used to lock skin tone, hair texture and hand appearance so shots 1–3 read as the same woman
even though her face never appears in the cuts themselves.

---

## 0.5 Product lock — read this before generating Shot 2 or Shot 3

**Why the last test drifted:** most image/video models don't "remember" a reference image across
a conversation — they re-ground on whatever's attached to that specific generation call. If the
product was only attached once, or only early on, every later shot is being re-imagined from the
text description alone, which is exactly how the tip count and cap shape wandered between Shot 2
and Shot 3. Text description alone is also just weaker than it needs to be when a real reference
exists — the fix is to stop asking the model to redraw the product from words and start treating
the two images you just sent as the literal ground truth it copies.

**Do this for every Shot 2 and Shot 3 generation, not just the first one:**

1. Attach **both** reference renders (the full studio shot and the macro tip/drip close-up) to
   the generation call itself, every single time, even if it feels redundant.
2. Paste the product-lock description below alongside the images — the image plus the matching
   words lock it harder than either alone.
3. If the tool supports it, generate Shot 2 and Shot 3 as **image edits / image-to-image on top
   of the reference product photo** (i.e., "place this exact object into this new scene") rather
   than text-to-image from scratch. That's the single biggest lever for fidelity — editing a real
   photo preserves the object; generating fresh from a description re-invents it.
4. If Omni Flash offers a video mode that takes a still image as the first frame and only
   animates it ("image-to-video"), generate the *still* composite first, confirm it actually
   looks like the real product, and only then run the video/motion pass on that confirmed still.
   Don't let the video generation step design the product — it should only be moving an object
   that's already correct in frame one.

**Product-lock description (paste verbatim with the reference images):**

> The exact product in the attached reference images — do not redesign or reinterpret it. A clear
> acrylic/glass cylindrical chamber with straight sides, filled with transparent warm golden-amber
> oil. A matte, cream/off-white dome-shaped cap on top with very faint vertical ribbing, no gloss,
> no shine, no metallic sheen. Printed in small white sans-serif text down the right side of the
> chamber, a vertical ml scale reading 4ml, 3ml, 2ml, 1ml top to bottom with horizontal tick marks
> beside each number. At the base, exactly **five** slender, clear, rounded-tip hollow applicator
> prongs, each 2–3cm long, arranged in a tight circular cluster like a flower or showerhead head,
> each tip with a faint greenish-gold tint from the oil inside it, each capable of a single bead of
> oil forming and dripping at its rounded end. Keep the tip count at exactly five in every frame.
> Do not change the cap shape, color, or texture. Do not change the chamber's cylindrical shape,
> proportions, or the ml markings. This object's geometry must stay rigid and identical across
> every frame of the shot — it does not bend, warp, melt, or reshape itself, even while being
> moved or pressed against skin or hair.

---

## 1. Voiceover script (built from the Ad C winner, condensed to spoken yap length)

Same hook logic, same Failed Solutions → Discovery → Mechanism → Rule of One → CTA spine as
the long-form winner, cut down to ~45-55 seconds of natural spoken pacing. Grade-5 words,
contractions, no em-dashes — same voice as every chiefed ad in this account.

> I used to just drip oil on my head and hope for the best.
>
> Every night, same thing. Oil running down my forehead before it even touched my scalp. I'd wipe it off with my sleeve and keep going like that was normal.
>
> I tried using less. I tried doing it over a towel. None of it really fixed anything, because the problem was never how much oil I used. It was how I was putting it on.
>
> Then I found this. It goes straight through the part, right onto your scalp. Not on your hair. Not on your face.
>
> The tips are hollow, and they press right onto your skin, so you can actually feel exactly where the oil's going. One hand. Two minutes. No mess.
>
> The habit was always there. The routine just needed to be easier than the reason to quit.
>
> If you're still dripping oil down your face every night, this is the part you've been doing wrong.

**Direction for the read:** conversational, slightly tired, talking-to-camera-while-doing-something
energy — not a polished VO artist read. Natural pauses where the commas sit. The line "I used to
just drip oil on my head and hope for the best" is the hook; it needs the same flat, deadpan,
slightly resigned delivery that's been working in the native ads, not an enthusiastic ad-read tone.

---

## 2. First-frame image prompts

Same house style as every other creative in this account: raw, unposed, phone-camera quality,
Phase 5-tested ("would this make sense posted with 'ugh, dealing with this again' as the
caption?"). "Higher quality" here means sharper detail and more deliberate lighting control for
a frame that has to hold still and look good as a video's opening frame — not a shift toward
a styled, produced look.

### 2.1 Mom avatar reference frame (identity anchor, not necessarily a visible cut)

```
A photorealistic, high-detail portrait of a woman in her early-to-mid 30s, postpartum mom
aesthetic, soft warm skin tone, slightly tired but makeup-free, dark-to-medium brown hair worn
down and slightly undone, wearing an oversized soft grey or oatmeal sweater or robe. Seated on
the edge of a bed or bathroom counter in natural morning light from a window to one side. Her
hands are visible in her lap, bare, unmanicured, the same hands that will appear in the product
demo shots.

Lighting: soft, natural, directional window light, slightly warm color temperature, minimal
shadow harshness. Shot style: higher-fidelity amateur phone photo quality — sharp focus on her
face and hands, natural skin texture visible (not airbrushed), slight depth of field falloff in
the background, which is a soft, ordinary bedroom or bathroom, lived-in but not messy.

No makeup glam, no styled hair, no posed smile — a caught, natural expression, looking slightly
off-camera or down, not directly performing for the lens. This frame exists to lock her exact
skin tone, hair texture and hand appearance for use as a visual reference across other shots in
this sequence.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### 2.2 Shot 1 — "The mess" (standard dropper applicator, dripping)

```
A raw, unposed close-up amateur phone photo, first-person-adjacent angle, in a bathroom mirror
or over-the-sink framing. A woman's hand holds a plain glass dropper/pipette applicator above
her hairline at the front edge of her scalp, squeezing out amber-colored oil. A visible drip of
oil has escaped past her hairline and is running messily down the side of her forehead, near her
temple, catching the light. Her hair at the hairline is slightly damp and matted from oil.

Her face is mostly out of frame or softly blurred at the edge — the focus is the dropper, the
hairline, and the drip of oil, not her full face. Bathroom counter clutter softly visible and
out of focus below: a makeup bag, a hair tie, ordinary mess.

Lighting: ordinary bathroom vanity light, slightly harsh and overhead, unflattering in a
realistic way, no warm filter. Shot style: phone camera quality, sharp focus on the dropper and
the drip, slight motion blur acceptable on the hand since this is mid-action, not a still pose.

This should read as an annoying, slightly gross mid-routine moment, not a styled beauty shot.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### 2.3 Shot 2 — "The fix" (Ninu applicator through voluminous parted hair)

**Attach both reference renders + the product-lock text from section 0.5 with this prompt.**

```
Using the exact dispenser shown in the attached reference images (clear cylindrical chamber,
cream dome cap, five clear hollow tips in a tight cluster, warm amber oil visible inside, ml
markings down the side — do not redesign it, do not change the tip count or cap shape), place it
into this new scene:

A raw, unposed close-up amateur phone photo, high detail, shot from slightly above and behind a
section of thick, voluminous brown hair that's been parted with fingers to expose the scalp. The
same reference dispenser is held with its tip cluster pressed flat against the scalp, right in
the part, oriented so the full cluster of five tips is visible and in focus — not angled away,
not obscured by hair, not cropped mid-cluster. The surrounding hair is held back and voluminous
on either side, framing the product but not touching or overlapping the tips.

A single clean drop of oil is visible right at the point of contact between the tips and the
scalp skin — contained, not smeared across the hair. The hair itself looks healthy, thick and
shiny, framing the shot. The hand holding the dispenser is visible but secondary — soft focus is
fine on the hand/fingers, but the dispenser itself must stay sharp and exactly match the
reference.

Lighting: soft, warm, natural, slightly brighter and cleaner than Shot 1 — this is the "it's
working now" moment, so the light should feel calmer and more controlled, same bathroom or
bedroom setting, different mood.

Shot style: phone camera quality but sharper and steadier than Shot 1. No logos, no text overlay,
no invented branding — only the real product's actual shape as shown in the reference.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### 2.4 Shot 3 — "The feel" (gentle press-and-glide demo on the hand)

**Attach both reference renders + the product-lock text from section 0.5 with this prompt.**
Motion simplified from the first version — a single press-and-glide instead of a multi-rotation
circular massage, since the more complex gesture is likely what caused the morphing in the Grok
test.

```
Using the exact dispenser shown in the attached reference images (clear cylindrical chamber,
cream dome cap, five clear hollow tips in a tight cluster, warm amber oil visible inside, ml
markings down the side — do not redesign it, do not change the tip count or cap shape), place it
into this new scene:

A raw, unposed extreme close-up amateur phone photo of the reference dispenser's five-tip cluster
pressed flat against the back of a woman's hand (same hand/skin tone as the mom avatar reference
frame), tips facing straight down into the skin so the full cluster is visible from the side, not
foreshortened or hidden. A faint, controlled bead of oil sits right where the center tip touches
the skin — contained, not smeared.

The hand and dispenser fill most of the frame, in sharp focus; the rest of the shot (lap, robe
sleeve, soft background) is loosely out of focus. This is a tactile, almost ASMR-adjacent beat —
the point is making the viewer feel the precision and gentleness of the contact, not a big motion.

Lighting: soft, warm, close, slightly intimate — a single source from one side, gentle shadow
under the hand.

Shot style: phone camera macro-adjacent quality, slight handheld waver acceptable, no studio
polish, no text, no logo callouts, no invented branding — only the real product's actual shape.

Aspect ratio: 9:16 vertical, 1080x1920.
```

---

## 3. Video direction — shot-by-shot, second-by-second

For feeding each first frame into an image-to-video model as a separate generation, then cutting
the three clips together in post and laying the VO + captions over the top. Total run time ~18-20
seconds of visual, looped or held on the last frame if the VO script runs slightly longer.

**General rule for Shot 2 and Shot 3 after the Grok test:** keep the motion to exactly one simple
action, on exactly one moving element, with a static or near-static camera. Two things moving at
once (camera + product, or hand + product) multiplies the chance of the model losing the
product's shape mid-motion. Add this line to the video-generation prompt itself for both shots:
*"The dispenser is a rigid object and must keep its exact shape, tip count, and cap shape in
every frame — it does not bend, melt, warp, or change form during the motion."*

### Shot 1 — 0:00–0:06 (6s)
- **0:00–0:02** — Static-ish handheld hold on the dropper at the hairline, oil visibly dripping. Minimal camera movement, slight natural handheld sway, like someone filming themselves in a mirror.
- **0:02–0:05** — The drip continues down past the temple; hand makes a small, slightly frustrated wipe motion with the back of the wrist, not a deliberate gesture, more a reflex.
- **0:05–0:06** — Quick, slightly jarring hard cut (not a dissolve) into Shot 2 — the cut itself should feel like an interruption, matching the "then I found this" turn in the VO.

### Shot 2 — 0:06–0:13 (7s)
- **Camera:** fully static, locked off. No pan, no push, no handheld sway — remove camera motion
  entirely from this shot so the only thing the model has to track is the product.
- **0:06–0:10** — The dispenser, already in contact with the scalp at the part, makes one slow,
  continuous downward glide of a few centimeters along the part line. This is the only motion in
  the shot. Oil visibly releases at the point of contact as it moves; hair stays out of the way,
  not moving.
- **0:10–0:13** — All motion stops. Hold completely still on the contained drop at the tip — a
  dead-still beat before the cut, matching the calmer mechanism pacing in the VO. A still hold is
  also the safest way to avoid the model drifting the product shape further the longer it moves.

### Shot 3 — 0:13–0:19 (6s)
- **Camera:** fully static, locked off, same reasoning as Shot 2.
- **0:13–0:17** — One slow, single press-and-glide: the tip cluster, already resting on the back
  of the hand, glides a short straight line (not a rotation) across maybe 2cm of skin, then stops.
  No circular motion — a straight glide is a simpler trajectory for the model to hold the object's
  shape through than a multi-rotation massage, which is the likely source of the jank in the first
  test.
- **0:17–0:19** — Hold on the final still frame, completely static (this can double as the
  freeze/end-card frame for the CTA text overlay in post).

**Transitions:** hard cuts only between all three shots — no crossfades, no swipe transitions. The
jump-cut rawness is part of the native read; a smoothed transition would make it feel produced.

**Audio layer (added in post, not baked into the video generation):** the VO script above, timed
so "I used to just drip oil on my head and hope for the best" lands within Shot 1, "Then I found
this" lands on the hard cut into Shot 2, and "you can actually feel exactly where the oil's going"
lands over Shot 3. No music under the voiceover, or at most a very quiet, low-key ambient bed —
this format's credibility comes from sounding like a real clip, not an ad.

---

## 4. Notes

- This is a cheap, fast test by design given the budget situation — one VO script, three short
  generations, no new copy to write or validate. If it performs, the natural next variation is a
  second VO read (different voice/pacing) over the same three visual cuts, not new visuals.
- Keep the mom avatar frame as a locked reference across all three shots so skin tone and hand
  appearance stay consistent if you regenerate any single shot later.
- No face, no baby, no medical/regrowth claims — same compliance posture as every other creative
  in this account.
- **Recommended order for Shot 2 and Shot 3 specifically:** generate the still image first and
  check it against the reference before spending a video generation on it. A still that already
  has the wrong tip count will only get worse once it's animated — catch the drift at the cheaper,
  faster step. Shot 1 doesn't need this check since it's a generic dropper, not the Ninu product.
- If Omni Flash still drifts after attaching the references on every call, the more reliable
  fallback is compositing: cut the real product out of one of these two reference renders
  (background removal) and paste that exact cutout into a generated hair-part or hand background,
  so the product in frame one is literally the same pixels, not a re-drawn copy. That guarantees
  fidelity at the cost of a manual compositing step — worth doing if two more prompt-only attempts
  still don't hold the shape.
