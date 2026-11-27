# BFCM bottom-funnel statics (2026-11-27), built on the V1 winner image

Base image: `ads/native-reexpression/final/V1_selfie-sticky.jpg` (V1_selfie-sticky: same woman and kitchen, laughing, lit board in hand, stack of 3 sealed boxes, yellow handwritten sticky "BUY 2 GET 1 FREE"). Winner DNA: real adult, kitchen, glowing board, offer visualised by the 3-box stack, handwritten offer in the scene, native look, no overlay pills.

Locked (all 4): primary text, headline, description, SHOP_NOW, destination, targeting. Primary text: My 5-year-old asks for this by name. Plug it in, hand him the markers — that's the whole setup. Headline: The toy that doesn't go in the garage. Description: Buy 2, Get 1 FREE + free tracing book. Ends Cyber Monday.

Single variable per ad (one edit to the V1 image each). Model: Nano Banana Pro, image_input = the V1 image, 4:5, 2K.

Edit instruction for all: "Use the attached photo as the exact base. Keep the woman, her expression, the kitchen, the lit board with the CREATE drawing, the stack of three boxes, the camera angle, the lighting and the framing identical. Change only the following:"

- BF1_black-friday: the yellow sticky note text becomes three lines of black marker handwriting: BLACK FRIDAY (smaller, top) / BUY 2 GET 1 FREE. Move the note up slightly so all the text is fully visible.
- BF2_free-book: the sticky note text becomes: BUY 2 GET 1 FREE / + FREE TRACING BOOK (second line smaller). All text fully visible.
- BF3_three-for-two: the sticky note text becomes: 3 BOARDS / FOR THE PRICE OF 2. All text fully visible.
- BF4_child: the sticky note stays exactly as is. Add a 5-year-old boy standing beside her at the counter holding a neon marker and grinning at the camera.

Scarcity: all 4 get a white pill 'Ends Cyber Monday' (top right) added in code by `ads/bfcm-statics/add_banner.py` after generation (brand-truth deadline only, locked across all 4; V1 without it is the control). Preview: `ads/bfcm-statics/preview/V1_banner-preview.jpg`.

Notes: if the sticky text comes out garbled, regenerate; fallback is for me to composite a new note in code. Meta: set the AI-content label at upload if required. Upload names: BF1_black-friday, BF2_free-book, BF3_three-for-two, BF4_child.

Launch plan (after sign-off): new ABO campaign about £25/day, one ad set, these 4 ads, to end of Cyber Monday. CBO untouched.
