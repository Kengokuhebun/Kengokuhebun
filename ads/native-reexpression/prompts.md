# Native re-expression test (draft, for approval)

## Why this test

Placement-matched CPM data from the Ritual Swipe campaign (2026-11-25): in the identical Facebook feed placement, the 8 designed/recreated statics paid **£150.60 CPM**; the 4 gradient text-posts paid **£30.40 CPM** — a 5x gap, repeating across every placement. `RS_01_selfie` is the only ad with any real funnel movement (5 add-to-cart, 1 purchase) but is still paying £183 CPM, one of the worst in the set. The hypothesis: Meta's auction is penalizing creative that reads as a designed ad (square format, baked-in marketing text pills) regardless of how well the underlying concept converts.

**Declared single variable: format.** Same proven angle, same hook, same offer, same audience, same campaign — only the visual format changes, from square + baked-in overlay text to vertical + no overlay text, phone-authentic framing. `RS_01_selfie` stays running as the control for this comparison (per the account's own standard: hold everything but one variable, same method as the UK hook test).

## Build method — changed from the Ritual Swipe set

- **No on-image marketing text at all.** The Ritual Swipe set added pills/headlines in code after generation; this set drops that step entirely. Any text in frame must be something a real phone would put there (a lock-screen clock, a stray notification, nothing invented) — never a headline, offer or pill. The hook and offer live only in the ad's primary text, same as the gradient posts already do.
- **Vertical 4:5 (1080 x 1350), not square.** 4:5 is Meta's recommended native-feed ratio and still displays reasonably in Stories/Reels, unlike the 1:1 squares that likely got cropped or treated as lower-quality in those placements.
- **Phone-authentic imperfection, deliberately**: natural handheld framing (not centered/symmetric), real indoor lighting (no studio light), visible grain, a slightly messy real room. No stock-photo polish.
- Same avatar as the Ritual Swipe set for continuity (early-to-mid 40s woman, shoulder-length light-brown hair, natural skin with visible texture, no heavy makeup, casual dark top — looks like a real parent, not a model).
- Nano Banana Pro (Kie, 18 credits/image, 2K), image_input = avatar reference + real Glowling board photo, so the product stays faithful. No AI-label text on the images; set Meta's AI-content label at upload if required.
- Four concepts, not eight — the Ritual Swipe set spread £60/day across 12 ads and starved 8 of them; keep this test small enough that each ad can actually get a read.

## Concepts

### N1: The proven moment, re-shot native (closest match to RS_01_selfie)
Same angle as the current winner, no pills.
Prompt: "Authentic vertical phone photo, 4:5, of [avatar] in a warm cluttered family kitchen with wooden cabinets and window light, caught mid-laugh as she holds up a clear acrylic LED drawing board on a white stand toward the camera, the board's edge glowing softly with a simple neon drawing, markers scattered on the counter behind her, real iPhone front-camera look, slightly off-center framing, visible grain, no text, no graphics, nothing overlaid."
Primary text (unchanged proven hook): "My 5-year-old asks for this by name. Plug it in, hand him the markers — that's the whole setup."

### N2: Real-moment, third person (not a selfie — candid, caught in the act)
Ties directly to the flagship ad's own proof moment (22 minutes of cooking, iPad never came out).
Prompt: "Candid vertical phone photo, 4:5, taken from a few feet away in a home kitchen at early evening, a young child standing at a kitchen counter on a step stool, focused on drawing on a clear acrylic LED board with a glowing neon line, a parent visible out-of-focus in the background cooking at the stove, warm kitchen light, slightly blurred motion at the edges, unposed, off-center composition, no text, no graphics."
Primary text: "I cooked for twenty-two minutes last Tuesday and the iPad never came out. He was at the counter the whole time, drawing on this."

### N3: Unboxing moment, raw
Prompt: "Raw vertical phone photo, 4:5, overhead angle, of an opened cardboard box on a kitchen table, a clear acrylic LED drawing board partly lifted out, a few neon markers still inside loose packaging, a child's hand reaching into frame toward the markers, harsh overhead kitchen light, slightly messy table with mail and a coffee mug nearby, candid and unstaged, no text, no graphics."
Primary text: "This showed up Tuesday. By Wednesday it was the only thing in the toy basket getting touched."

### N4: Night / wind-down moment
Ties to the product's real night-light use case (PDP's own "Four ways to use it" section — not tied to any removed testimonial, a genuine product feature).
Prompt: "Low-light vertical phone photo, 4:5, of a child's bedroom at night, a clear acrylic LED drawing board standing on a nightstand with a soft glowing drawing left on it, faint warm lamp glow nearby, phone-camera flash artifacts and grain typical of a low-light handheld shot, slightly tilted framing, no text, no graphics."
Primary text: "We leave his last drawing up overnight now. Bedtime stopped being a fight over the tablet."

## Ad set plan

- Same campaign pattern as Ritual Swipe: one ad set, these 4 ads only, CBO-funded from the existing `Glowling_R2_BF26_RitualSwipe_CBO` campaign (no new campaign, no budget change) — or a small dedicated budget if you'd rather isolate it from the current campaign's CBO entirely. Recommend the former, since it keeps this a clean one-variable addition to an already-running test rather than a new confound.
- Names: `RS_N1_proven-native`, `RS_N2_candid-kitchen`, `RS_N3_unboxing`, `RS_N4_nightlight`.
- Link, UTM, pixel, CTA all unchanged from the current campaign.
- Read plan: same method as the UK hook test and the Ritual Swipe read — CTR, CPC, and crucially **CPM against `RS_01_selfie`'s £183 benchmark**, since CPM is the specific variable this test is built to move.

## Still needs from you before build

1. Approve the 4 concepts/copy (or tell me what to change).
2. Confirm ad set placement: fold into the existing Ritual Swipe campaign (recommended) or a separate test.
3. You (or Nano Banana Pro on your end) generate the 4 images from these prompts — same workflow as the Ritual Swipe set: drop them in a Drive folder and tell me, or generate here if you'd rather I do it directly.
