# R4 — Image prompts for the new-creative ad set (4 ads)

One swipe reproduction (premium/catalog style, Kitsch design → Ninu product + brand colors)
and three Phase 5 natives (raw, documentary, POV, no visible product in 2 of 3).

---

## Ad 1 — Swipe reproduction: "Your messy oil routine's worst nightmare"

**What it is:** reproducing the actual Kitsch static ad (coral background, "/kitsch/"
wordmark, "IT SOLD OUT 5 TIMES" badge, "Your Bald Spot's Worst Nightmare" headline, 3
checkmark bullets, black SHOP NOW button, a diagonal product render dripping oil in the
bottom right) — not the earlier video frames. The graphic shell (wordmark, badge, headline,
bullets, button, warm sunburst background) is already built and rendered via HTML/CSS —
see `creatives/build-r4-swipe-shell.js` and
`creatives/png/R4-Ad1-Swipe-Reproduction/Ad1-Swipe-Reproduction__9x16.png`. That part needed
no AI image generation; it's pure layout and typography, reproduced pixel-precise.

**What's left:** the one thing that does need generation — an isolated product render of
the Ninu dispenser, posed diagonally like the reference, dripping oil, on a transparent or
easily-croppable background so it can be composited into the bottom-right "product zone"
of the shell.

**What changed from the reference, and why (per your brief: replace the product, refine
the colors to our brand, refine the copy):**

| Kitsch original | Ninu reproduction | Why |
|---|---|---|
| "/kitsch/" wordmark | Ninu's own wordmark (wide-tracked serif, established on the PDP) | Their specific mark is their IP; "refine to my brand" means our own identity, not a copy of theirs |
| "IT SOLD OUT 5 TIMES" badge | "30-DAY GUARANTEE" | We have no sales-history claim to make; this is a true, already-planned proof pill (see `swipes/kitsch-swipe-analysis.md`) |
| "Your Bald Spot's Worst Nightmare." | "Your messy oil routine's worst nightmare." | The body-attribute phrasing risks Meta's personal-attributes policy and was already flagged; the problem-focused version is the one already running across this campaign |
| Coral/pink background | Terracotta-to-espresso gradient with a warm gold sunburst | Matches Ninu's actual brand tokens instead of a competitor's color |
| Metallic/chrome applicator tips | Clear/frosted silicone tips | Our copy says "hollow silicone tips" everywhere — the product shot needs to match what the copy claims, not Kitsch's metal-tip design |
| Generic bullet copy (minoxidil, "quick and effortless") | Our actual mechanism claims, no em-dashes, AARREIGN-chiefed | Matches our product and our established voice |

### Product-shot prompt (transparent/isolated, diagonal drip pose)

```
A photorealistic, isolated product render on a transparent or seamless white background, suitable for compositing into an ad graphic. A scalp oil dispenser posed at a dramatic diagonal angle, roughly 35-40 degrees off-vertical, as if hand-held and tilted toward camera. The body is a clear glass/acrylic cylindrical chamber filled with warm golden-amber oil, with a cream-colored dome cap at the top of the visible portion. Printed vertically along the side of the chamber in small white lettering: ml markings reading 1ml, 2ml, 3ml, 4ml.

At the base of the chamber, five hollow, clear/frosted silicone applicator tips extend downward and slightly outward, each with a soft frosted sheen (not metallic, not chrome) — translucent silicone, catching warm light with a soft glow rather than a hard metal glint. Oil drips visibly from two or three of the tips: one tip has a large amber droplet caught mid-fall with a thin connecting thread, another has a bead just forming, a third has a thin rivulet running down its length.

A thin, narrow handle or rod extends up and out of frame from the top of the dome cap, implying the dispenser is being held, continuing the diagonal line established by the body (matching a hand-held sprayer/dispenser pose, same compositional energy as a cosmetics ad product shot, but no hand visible).

Lighting: warm, directional, golden-hour style light from the upper left, creating soft highlights along the glass and a warm amber glow through the oil, with soft shadow falloff. Shallow depth of field optional but keep the dripping tips and chamber in sharp focus throughout, since this will be cropped tightly in the final composite.

No background elements, no surface, no hands, no text, no logo — isolated product only, either on pure transparent (PNG with alpha) or plain white/light grey seamless, so it can be cleanly extracted and placed into a separate graphic design. High-end commercial product photography quality, sharp detail on the glass, the ml markings, and the oil droplets. Portrait-oriented crop, roughly 1000x1400, with the dripping tips positioned in the lower third of the frame and the rod extending toward the upper third.
```

**After you generate it:** send the image back and I'll composite it into the shell
(swap the placeholder dashed box for the real render) and re-export the final static at
9:16.

### Fallback prompt (if transparent/isolated generation doesn't come out clean)

Some models handle "transparent background" requests inconsistently. If the output keeps
adding a background despite the prompt, fall back to this version and we'll crop/key it
out in post:

```
Same product render as above, but on a solid, seamless, pure white (#FFFFFF) background with soft, minimal drop shadow directly beneath the dispenser only — no gradient, no texture, no props. Studio product photography on white, ready for background removal.
```

---

## Ad 2 — Native: "The Pillow"

**Phase 5 category:** The Evidence No One Else Sees + The Moment They're Alone With It.
**The sentence that drives the shot:** *"The thing that almost made me quit my scalp oil
routine wasn't the routine. It was what I woke up to the next morning."*

**The core question answered:** she's just stepped back into the bedroom after a 2am nursery
run. What does she see first? The pillow. Before anything else.

```
A raw, unposed amateur smartphone photo taken from a standing first-person POV at the foot of a bed, late at night, in a dim bedroom lit only by the soft blue-white glow of a baby monitor screen on the nightstand and a sliver of hallway light through a half-open door. The shot is angled down and slightly forward, as if someone just walked back into the room and is looking at the bed before getting back in.

The focal point, sharp and well-lit relative to the rest of the dark frame: a pillow on the near side of the bed with a visible amber-toned oil stain soaked into the fabric, a few strands of hair stuck to the stain, the pillowcase rumpled and slightly twisted. The sheets around it are messy, half-kicked, lived-in — not styled.

In the soft, out-of-focus background: a shape of a person under the covers on the far side of the bed, turned away, sleeping, no face visible, just a dark silhouette under a blanket. The baby monitor on the nightstand shows a faint glow and a small readout light. A glass of water, maybe a phone charger cable, ordinary bedside clutter, all soft and dark.

Shot style: phone camera at night, high ISO grain, slightly underexposed except where the monitor and hallway light fall, no flash, no filter, no staging. The pillow stain is the only thing in clear focus. This should look like a photo someone took half-asleep, almost without thinking, not a deliberate composition.

Aspect ratio: 9:16 vertical, 1080x1920. Also generate 1:1 and 1.91:1 crops keeping the stained pillow as the dominant, sharpest element in frame.
```

**What NOT to let the model do:**
- No visible faces, including the husband's — Phase 5 rule, performed emotion reads as acting
- No visible product anywhere in frame — this is a consequence shot, not a demo
- No dramatic or horror-movie lighting — this should read mundane and real, not staged-scary
- No text overlay baked into the image

---

## Ad 3 — Native: "The Crib"

**Phase 5 category:** The Evidence No One Else Sees. Hands-only per your brief — no faces.
**The sentence that drives the shot:** *"My husband picked our daughter up out of her crib
and came out holding a handful of my hair. Oily hair."*

```
A raw, unposed amateur smartphone photo, close-up and hand-focused, no faces in frame. A man's hand and forearm, out of a soft-focus nursery background, holding a few strands of hair between his thumb and fingers, the hair visibly damp and slightly oily with a faint sheen catching the light. His hand is positioned near a white crib rail, which is in the foreground at the bottom edge of the frame, slightly out of focus.

Background: a muted, softly blurred nursery — pale sage or cream walls, the warm glow of a small nightlight, the edge of a changing table or dresser barely readable in the blur. Shallow depth of field, the hand and the strands of hair are the only sharp element in the frame.

Lighting: soft, warm, low-level nursery nightlight glow, slightly underexposed, no harsh shadows, no flash. The mood is quiet confusion, not alarm — like someone just noticed something odd mid-task and paused.

Shot style: phone camera quality, slight grain, no filter, no staged studio lighting, no visible product anywhere in frame. This should look like a photo someone took one-handed, fast, to show someone else later, not a composed shot.

Aspect ratio: 9:16 vertical, 1080x1920. Also generate 1:1 and 1.91:1 crops keeping the hand and hair strands centered and sharp.
```

**What NOT to let the model do:**
- No faces — the brief and Phase 5 both call for this
- No visible product
- No baby visible in frame (keep it to the hand, the hair, the crib rail — implying the baby was just lifted out, without showing the baby, keeps this from reading as alarming/unsafe)

---

## Ad 4 — Native: "The Scarf"

**Phase 5 category:** The Moment They're Alone With It, from her own POV (per the Phase 5
POV rule — her own eyes, not an observer's).
**The sentence that drives the shot:** *"Every morning before we left the house, I wrapped
my head. Not for the cold. To hide what my scalp oil routine actually looked like."*

```
A raw, unposed amateur smartphone selfie taken in a hallway or bathroom mirror, first-person POV, morning light. A woman in her early-to-mid 30s, wearing an oversized soft grey or oatmeal sweater, is mid-motion wrapping a patterned scarf around her hair and the top of her head, both hands raised, tying it at the back. Her hair underneath looks slightly flat and oily at the roots where visible at the scarf's edge. No glamour, no makeup, slightly tired morning expression, not posed for the camera — caught mid-task.

Background, softly out of focus behind her in the mirror reflection: the end of a hallway, a front door, and the soft blurred shape of a man standing near the door with a stroller, waiting — no distinct face, just a soft silhouette and the shape of the stroller. Warm but ordinary morning light through a window or front door glass.

Shot style: phone camera selfie quality, slightly soft focus, natural harsh morning light (not flattering, not styled), no filter, no beauty retouching, visible grain. The scarf-wrapping motion should look caught mid-gesture, not a finished, composed look.

Aspect ratio: 9:16 vertical, 1080x1920. Also generate 1:1 and 1.91:1 crops keeping her head/hands and the scarf as the dominant sharp element, with the blurred doorway scene visible but secondary.
```

**What NOT to let the model do:**
- No clear second face (the husband should stay a soft, unidentifiable silhouette — this keeps the focus on her, not on him)
- No visible product
- No glamour or "pretty" styling on the scarf-wrap — it should read practical/hiding, not fashion

---

## Shared production note

All three natives should pass the Phase 5 test before you finalize: *would this image make
sense posted with "ugh, dealing with this again" as the caption?* If any generation comes
back looking styled or composed, push the prompt harder on "unposed," "caught mid-task," and
"phone camera quality" rather than accepting a prettier result — a too-polished version of
any of these three will read as an ad, not a document, and loses the thing that makes them
work.
