# R18: Native image prompts for the R16 and R17 copy

Written 2026-11-03. Prompts are for Nano Banana (via Higgsfield or OpenRouter), written to the Nano Banana prompt conventions: natural language, lighting first, a camera spec, no inline flags. Aspect ratio and resolution are set in the generator, not in the prompt text.

Native styles and rules come from the master document's Native Image Ad prompt: phone-camera quality, real settings, no studio polish, product out of the image unless the shot is a product demo, and "never fake, stage, or exaggerate results."

## 0. Read this first: the colour-post format may not be your CPM problem

Hook1_OG and Hook3 are the same format (orange gradient, hook-only text). Their numbers from the screenshots:

| | Hook1_OG | Hook3 |
|---|---|---|
| Impressions | 1,281 | 1,241 |
| CPM | £83.83 | £21.35 |
| CTR (all) | 6.56% | 4.67% |
| CPC (all) | £1.28 | £0.46 |
| Link CPC (spend ÷ link clicks) | £2.39 | £0.53 |

Same format, similar impressions, a CPM about four times apart. So the format by itself doesn't explain it. I can't tell what does from here. These are the things I'd check in Ads Manager before blaming the creative:

1. **Ad set and audience.** Were both ads in the same ad set at the same time? An ad that mostly delivered in a different ad set or audience can have a very different auction.
2. **Breakdown by placement and by day.** Ads Manager > Breakdown > By Delivery > Placement, then Day. If Hook1_OG's spend sat in one placement (for example Stories) or in the days before you limited placements to Facebook and Instagram, that could explain it.
3. **Date range.** Hook1_OG earlier showed £190 CPM and now £83.83. A number that moves that much on about 1,200 impressions is unstable.

What this means for testing: keep the Hook3 colour post as the control for R16, because Hook3 is the one that delivered cheaply. If you also change the image, R16 stops being a clean copy test. New natives are for later rounds, each as one variable (image only, copy fixed).

That said, a photo native is a fair thing to test: it's a different format, it matches the master doc, and a mix of formats protects you if one format gets expensive.

## 1. Rules for every prompt below

- **No text inside the generated image.** Generators garble small text. Generate the photo clean, then overlay any words in HTML or Canva (the native-ad mockup skill renders text accurately).
- **No faces where we can avoid it.** Hands, backs of heads, rooms and objects look more real and avoid likeness issues.
- **No product unless the shot is a demo.** Prompts 1 to 4 have no product. Prompts 5 and 6 show it and need a real reference photo (section 3).
- **No hair before-and-after, no thinning or regrowth imagery, no scalp close-ups.** Compliance guardrail.
- **These are illustrative, not customer photos.** Don't label them as a customer's photo, and don't add fake comments, likes or timestamps.
- Aspect ratio: **4:5** is the main feed shape and takes the most room on mobile. Also generate **9:16** for Stories and Reels. 1:1 only as a fallback. Resolution 2k.
- Generate 4 variations of each and pick the least glossy. If it looks like a stock photo, it's wrong.

## 2. Prompts (no product in frame)

### Prompt 1: The 3am wet hands (Style 4 POV)

- Copy beat: the problem, the skip. Pairs with R16 and R17-A, R17-B, R17-C. Matches the hook "wet hands, in bed."
- Overlay: none, or the hook as a small white-bar caption (section 4).

```
The only light is the dim amber glow of a bedside nightlight from the right and a faint cool spill from a phone screen out of frame, mixed and uneven, the look of an unedited iPhone photo taken in a dark bedroom without flash. First-person point of view looking down at a woman's two hands resting palms-up on a rumpled grey cotton duvet. Her fingers glisten with a thin sheen of oil and there is a small dark oily smudge on the duvet beside her thumb. She wears a faded oversized cotton t-shirt sleeve. Natural hands with five fingers each, slightly tired, no rings, short plain nails. In the soft-focus background a baby monitor glows faintly green on the nightstand next to a glass of water. Shot on an iPhone 15 main camera, slightly grainy and soft, tilted a few degrees, mild noise in the shadows. Muted grey-green night colour, slightly underexposed. No face, no text on screens, no product, no packaging, no logos, no visible lighting equipment.
```

### Prompt 2: The towel (Style 1 specimen / proof)

- Copy beat: the cleanup. Pairs with R17-C (the oil-on-towel evidence photo from R15), R17-A ("The towel. The wet hands.").
- Overlay: none.

```
Flat overhead bathroom light at about 4000K, the ordinary look of a phone photo taken in a family bathroom at night, no flash. A white cotton bath towel is draped over the edge of a tub. Across its upper middle is a darker, damp, translucent oily patch roughly the width of a pair of shoulders, with a few small separate spots near the edge, a few dark drops on the grey bathroom floor tile below it, and a folded damp hand towel beside it on the tub edge. Slightly off-centre, slightly crooked framing, like someone took a quick photo to complain about it. Shot on an iPhone 14 main camera, ordinary phone sharpness, slightly warm tungsten cast from a bulb out of frame. Realistic everyday mess, no staging. No people, no hands, no text, no product, no logos, no brand colours.
```

### Prompt 3: The bottle at the back of the shelf (Hybrid bait)

- Copy beat: "The bottle would migrate to the back of the shelf." Pairs with every version.
- Overlay: none. The comment bait is that a viewer spots the bottle.

```
Soft cool daylight from a small bathroom window at the left, around 5000K, the plain light of a phone photo taken at midday. A cluttered white bathroom shelf in front of a tiled wall: a shampoo bottle, a conditioner, a pump hand soap, a tub of cotton pads, a hair clip, a toothbrush cup. Behind them, pushed to the back corner and half hidden, sits a small unlabeled amber glass dropper bottle with a thin film of dust on its shoulder, easy to miss but clearly there. The shelf is normal and slightly messy. Shot on an iPhone 15 main camera at a slight angle, a little soft at the edges, everyday framing, slightly off level. No people, no text, no brand names or readable labels on any bottle, no studio feel.
```

### Prompt 4: The clean pillowcase (Style 1 close-up)

- Copy beat: "Wet hands and a clean pillowcase." Pairs with R17-A.
- Overlay: none.

```
Low warm lamp light from camera left at about 2800K, the soft yellow glow of a bedside lamp, with the rest of the room falling into dim shadow, an unedited iPhone close-up taken in bed. Tight crop on the corner of a white cotton pillowcase with a faint soft crease. A small, pale, translucent oil mark about the size of a coin sits on the fabric near the seam, with a darker edge where the oil has soaked in. Beside it, the corner of a grey duvet and one lock of hair out of focus at the frame edge. Shallow depth of field the way a phone portrait mode renders it, slightly grainy, a little warm. Ordinary and unglamorous. No face, no hands, no text, no product, no logos.
```

## 3. Prompts that show the product (need a real reference)

The generator can't reliably invent the Ninu dispenser. Earlier rounds it drew it tilted, in the wrong colour, or turned the oil into a dropper bottle. Use one of these routes:

1. **Best:** photograph the real product with your phone, in the scene described. This is the most native image you can get, and it's accurate.
2. **Otherwise:** attach clear photos of the real dispenser as a reference image with high influence, and run the prompt below. Check every result against the QA list.

Product spec for the prompt and the QA check: a palm-sized upright cylinder, cream scalloped dome cap, clear reservoir with 1 to 4ml markings, a cluster of hollow translucent silicone tips at the base, 8ml reservoir. Check that it isn't tilted, the tips are at the bottom, the reservoir is clear, and no dropper bottle appears.

### Prompt 5: The nightstand (Style 2 real moment, for the GoFree bedside native)

- Copy beat: "It's about the size of my palm. I put it on the nightstand." Pairs with R17-B.
- Reference: attach the product photo.

```
Soft warm light from a single bedside lamp at camera right, around 2900K, the quiet yellow of a lamp turned low at night, the rest of the room dim. A close, slightly high-angle phone photo of a wooden nightstand: a half-full glass of water, a phone lying face-down, a hair tie, and in the middle the dispenser from the attached reference image standing upright, reproduced with absolute fidelity to its exact shape, proportions, cream scalloped cap, clear chamber with 1 to 4ml markings and translucent silicone tips at the base. It looks ordinary and slightly used, like it lives there. A soft blur of rumpled bedding in the background. Shot on an iPhone 15 main camera, slightly grainy, imperfect framing. Upright and straight, not tilted, no dropper bottle, no oil bottle, no text, no brand name, no studio lighting.
```

### Prompt 6: The part (Style 3/4 demo, POV from behind)

- Copy beat: "You part your hair. You press the tips against your scalp along the part." Pairs with R16 and the mechanism paragraph in every R17.
- Reference: attach the product photo. Check it carefully: hands and product are the failure points.

```
Soft overhead bathroom light at about 4500K, even and slightly flat, the look of a phone photo taken by a friend standing behind her. A rear view of a woman sitting on the edge of a bed, her head and shoulders in frame, healthy shoulder-length brown hair in a natural centre part. With one hand she holds the dispenser from the attached reference image, reproduced with absolute fidelity to its shape and proportions, pressing the hollow silicone tips lightly against her scalp along the part. Her other hand is not visible. Her face is not visible. The hair looks normal and full, nothing about it suggests thinning. A plain wall and a lamp softly out of focus beyond her. Shot on an iPhone 15 main camera, slightly soft, natural, unposed. Natural hand with five fingers, no dropper bottle, no oil bottle, no text, no logos, no studio lighting.
```

## 4. Headline-style natives (Style 5), from the copy's own lines

The master doc's headline style: a plain white bar, large black text, ending in "…more", over a simple relevant photo, so it looks like a cut-off Facebook post. Generate the background with Prompt 1, 3 or 4 and add the words in HTML. Lines below are verbatim from the copy:

| Headline on the bar | Source | Background |
|---|---|---|
| Baby up 3 times. Wet hands, in bed. Skipped my scalp oil again…more | Hook3, R8 | Prompt 1 |
| A chore at 10pm after a full day with a baby is a chore that gets skipped…more | Ad C, R13, R16 | Prompt 3 |
| Every mom in my fb group did her nightly oil for six months straight. I made it eleven nights…more | R17-C | Prompt 4 |
| I never started over Sunday…more | Ad C | Prompt 3 |

Layout: bar across the top of a 4:5 canvas, black Helvetica-style text on white, about 54px, left-aligned, no logo, no brand colours, "…more" in grey on the last line.

## 5. The Notes native needs no image generator

The iOS Notes screenshot is rendered from HTML, so its text stays accurate. The existing one is in `creatives/png/R13-Notes-Native/` (title "skipped my scalp oil again"). For R17-A, re-render it with the R17-A text through `creatives/build-r13-notes-native.js`. Don't add fake timestamps, like counts or comments. It's brand voice, not a customer post.

## 6. Which image goes with which copy

| Copy | Lead image | Alternates |
|---|---|---|
| R16 (Ad C buyer body) | Hook3 colour post (control, keep) | Prompt 1 |
| R17-A (Quilty Notes) | the Notes native | Prompt 4, Prompt 2 |
| R17-B (GoFree bedside) | Prompt 5 | Prompt 1, Prompt 3 |
| R17-C (TryVera advertorial) | Prompt 2 (towel) | Prompt 3, headline native |

## 7. How to test the formats (one variable)

Copy fixed (use R16, or whichever body won), image changes:

| Ad | Image |
|---|---|
| Control | Hook3 colour post |
| Variant 1 | Prompt 1 (3am hands), 4:5 |
| Variant 2 | Headline native: "Baby up 3 times…more" over Prompt 1 background |

Read in the master doc's order: link CPC first (the hook and creative read), then add-to-cart per link click, then purchases. Watch CPM, but treat anything under about 1,000 impressions as noise. Checkpoints: £14 with 0 link clicks, £28 with 0 add-to-cart, £42 with 0 checkout, £54 with 0 purchases.

## 8. Cost and next step

Nano Banana 2 is about 1.5 credits per image on Higgsfield, so 4 variations of 4 prompts is roughly 24 credits. I haven't generated anything. Say the word and I'll run Prompts 1 to 4 (the ones with no product) through Higgsfield, show you the results, and render the headline versions.
