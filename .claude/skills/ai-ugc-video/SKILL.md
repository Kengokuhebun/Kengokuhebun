---
name: ai-ugc-video
description: Build realistic AI UGC video ads (GPT Image 2 for sheets, Seedance 2.5 for video) from an avatar brief, a product image and an optional real UGC reference clip. Use when the user wants to make, adapt or prompt an AI UGC ad, creator/product reference sheets, a Seedance UGC prompt, or turn a real UGC clip into a text-described style reference.
---

# AI UGC Video Workflow

Produces a ~20s vertical (9:16) talking-head UGC clip for Reels, TikTok, Meta ads and Shorts. Output is a set of pastable prompts, not generated media. Based on the "AI UGC Ad Workflow" playbook (Youri van Hofwegen), adapted after a real run.

Core rule: the video model only copies what it can see. Everything the ad shows (product states, face, outfit) must exist on a reference image, and everything it should *not* invent must be forbidden in words.

## Inputs to collect (ask only for what's missing)

1. **Product**: name, description, photo if any. Blank/generic bottle is fine for portfolio work.
2. **Avatar**: age, build, look, outfit, and the room she/he is in (match the creator to the room).
3. **Concept**: the pain point or angle, in first-person experience terms.
4. **Reference UGC clip** (optional): for framing, movement and lighting.
5. **Platform and language**: default Reels/TikTok/Meta/Shorts, English.
6. **Length**: default 20s, 5 beats.

## Step 0: Read the reference clip (if one is given)

Do NOT tell the user to upload the video to Seedance (it was too expensive). Convert it to text instead:

1. `ffprobe` for duration and size.
2. Extract a contact sheet into the scratchpad: `ffmpeg -v error -i <clip> -vf "fps=1/3,scale=240:-1,tile=6x5" -frames:v 1 sheet.jpg`, then Read the image.
3. Note: shot size, camera behaviour (propped / handheld / locked), cut rhythm, gesture rhythm, how the product is held and raised, insert shots, lighting (direction, softness, white balance), background.
4. Also map the clip's structure (hook, reveal, benefit, convenience, CTA) to the target length.
5. Never copy the reference person's face, clothes, product, captions, promo code or claims. Only style and structure.

## Step 1: Product sheet (GPT Image 2)

Settings: Image, GPT Image 2, quality high, 4K, 16:9, Auto Polish off. Attach the real product photo as an input when available.

Template (adjust panel count to the states the ad shows):

```
A single catalogue product sheet photograph of one {PRODUCT}, shown in {N} panels arranged as a clean grid of {C} columns by {R} rows, thin even white gutters between panels, every panel showing the identical {PRODUCT}, a small dark gray caption in plain sans-serif under each panel naming the view.

The product: {SHAPE, MATERIAL, COLOURS, CAP/LID DETAILS}. {BRAND TEXT spelled letter by letter, OR "completely blank: no label, no sticker, no brand name, no logo, no text, no barcode, no printing of any kind"}. Nothing else is printed on it. The product is identical in shape, colour, proportion and markings in every panel. The ONLY text in the image is the small gray captions.

Panels, left to right, top row then next rows: FRONT, BACK, LEFT SIDE, RIGHT SIDE, TOP CLOSED, BOTTOM, THREE-QUARTER, {EVERY STATE THE AD SHOWS: OPEN, POURING, IN HAND, CONTENTS IN PALM...}, {WORDMARK close-up if branded}.

Seamless light neutral gray studio backdrop identical in every panel, soft even diffused catalogue lighting, subtle soft contact shadow only, true colour, no reflections of a studio or photographer, crisp real material texture, photographed not generated.
```

Rules: every state used on camera gets a panel; limit counts ("exactly three capsules", "the only bare switch, no second gap"); say nothing else is printed.

## Step 2: Creator sheet (GPT Image 2)

Settings as above. Three parts pasted as ONE prompt:

- **Part 1**: person and outfit. Be specific and imperfect: skin tone variation, lines, freckles, a mole, hair with a few silver strands, no makeup, "an ordinary, believable real person, not a model". State age as a number plus "a mature adult face" for 40+.
- **Part 2**: three panels. LEFT: full body front view, no head/neck/hair, empty hollow collar, full headroom. CENTER: full body rear view. RIGHT: tight chest-up identity-lock portrait.
- **Part 3**: 18% neutral gray seamless backdrop, flat shadowless light, no contact shadow, matte skin, true skin tone, 50mm, film grain, photographed not generated.

(Full text of the three parts is in `supplement-ugc-prompt-kit.md` in the repo root.)

### Lessons from the real run

- Age drifts young. Add "clearly 42 years old, not a teenager, fine lines, nasolabial folds, silver strands, mature adult skin". If it still drifts, re-run with the sheet attached and a "change only the age" instruction.
- The strict headless 3-panel sheet can come out looking too AI/plastic. Fallback that worked: use a plain multi-view reference of the same woman (front, side, back, face visible) instead of the strict sheet. Then edit the video prompt so it only describes what is actually visible in that image (no freckles, mole or earrings that are not there) and says "the front-view panel" instead of "the right-hand portrait panel".
- If the face drifts between video shots, crop a tight face shot and add it as @Image3 ("match it exactly").
- Do not use a real person's photo as the avatar; design a new one.

## Step 3: Video prompt (Seedance 2.5)

Settings: Video, Seedance 2.5, text to video, creator image first (@Image1), product image second (@Image2), 1080p, 9:16, 20s, audio on, Auto Polish off. Paste as ONE prompt. No video upload.

Structure:

1. **References paragraph**: describe @Image1 (face, hair, outfit) and @Image2 (product) in words even though attached, and say what must not change ("no label, no text, nothing in the scene carries any text or logo").
2. **Scene and style paragraph**: room, wall, lighting written in words (copied from Step 0: e.g. "soft, even, diffused daylight from a large window out of frame at camera-left, no hard sun patches, neutral-to-slightly-cool white balance, slight sheen on forehead and nose, no studio light, no grading").
3. **Camera and framing paragraph**: shot size, camera behaviour as an explicit decision (propped near-static with slight drift, or handheld selfie), gesture rhythm, jump cuts every 3 to 5s, one close-up product insert. Product rule: held beside the face at shoulder height, never covering mouth, nose or eyes.
4. **Beats** (default 5): 
   - 0-4s hook, no product in hands, gesturing
   - 4-8s product raised beside face, one short line
   - 8-13s personal routine/result, product at chest height
   - 13-16s silent close-up insert (open the product, show contents)
   - 16-20s soft CTA ("link's in my bio"), reach toward phone, frame tilts
5. **Audio**: voice clear, dry, phone-mic character, lip-synced, "nothing spoken outside the quoted lines", quiet room ambience, product sound lands in a speech gap, "No music, no voiceover, no captions, no on-screen text".

Rules: every spoken line in quotes; about 2.5 words per second (about 50 words for 20s); say how many beats the product is handled in; no "cinematic" or polish words.

Fallback if a 20s take drifts: two 10s generations (beats 1-3, beats 4-5) with the same images.

## Step 4: After generation

- Add word-by-word captions in an editor (CapCut etc.). Never ask the model to render text.
- Dub to other languages with a lip-sync dub tool only if needed (default is English only).
- QA: product text/label not invented, product never covers the mouth, face and hair match across cuts, exact capsule/part counts, lip-sync holds on every line.

## Compliance (supplements, health, beauty)

- Scripts use first-person experience only. No claims to treat, cure or prevent anything, no numbers, no before/after.
- Clients supply their own approved claims and disclaimers.
- Label portfolio pieces as AI-generated concept demos and follow each platform's AI-content disclosure.
- Don't reuse another creator's promo code, name or claims.

## Output format

Give the user: (1) the product sheet prompt, (2) the creator sheet prompt, (3) one pastable video prompt, (4) a two-line upload/settings note. When the user only asks for "the prompt", return just the pastable block plus the upload order.
