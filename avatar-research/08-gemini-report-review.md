# Review of the Gemini VOC report (topical messy routine + hands)

Reviewed 2026-11-13. The source file is `raw/gemini-voc-topical-hands-2026-11-13.pdf`. It was run in Gemini, not Grok.

## What it delivered against the brief

| Target | Asked for | Got |
|---|---|---|
| H1 quotes | 60+ (25+ aged 50+) | about 10 (2 aged 50+) |
| H2 quotes | 25+ (10+ hair-specific) | 3 (0 hair-specific) |
| Quotes against | 10+ each | 3 |
| Sources | 15+ | 10 Reddit threads, 0 Amazon, 0 forums, 0 YouTube, 0 X |
| Links | Comment permalinks | **Thread-level links only.** Comments aren't linked. |

Gemini says itself that it missed the targets ("I extracted exactly 13").

## Verification status
- The 10 thread links embedded in the PDF:
  - r/FemaleHairLoss: 1c468jg, 1ff90rt, 1ssgb4z, 1xom6dv, qpzq7w, vmk4gd
  - r/Menopause: 1j27h5j, 1svsmmv, zo9p67
  - r/tressless: u1wi2k
- **I could not open them from here.** Reddit blocks this session.
- Treat every quote as **UNVERIFIED** until someone opens the thread and finds the exact words. AI research tools sometimes misquote or merge comments.

## What to throw out
1. **Sizing (section 6) is wrong or unsourced.**
   - "osteoarthritis of the hand affects nearly 60% of women over age 65" doesn't match published figures. Symptomatic hand OA is about 23% to 26% of older women (Women's Health and Aging Study; Framingham, via PMC3819994). Radiographic-only figures are higher.
   - The "10–20% pursue OTC topical treatments" figure is a guess with no source.
2. **Ad hooks (section 8) break our compliance rules.**
   - "Are you tired of your hair looking...", "If squeezing tiny dropper bottles hurts your hands" and "Designed for weak grips" are second-person or imply health conditions. Meta rejects ads that imply personal attributes.
   - "you were just using the wrong bottle" also leans on a quit-treatment story.
   - Rebuild any hook in first person, about delivery only.
3. **The H2 "hands" quotes are about general arthritis** ("I can't even make a fist anymore or open a water bottle"), not about hair products. They show the condition exists, not the pain with scalp products.

## What's useful (once verified)
1. **Home-made applicators are the clearest proof of the need.**
   - Women use a toothbrush, a Q-tip, a makeup brush in a cap, or foam on a plate to keep the product off their hair.
   - Their complaint is the extra steps: "it became such a chore to add the minoxidil to a small cap, dip the brush, apply the solution, wash the brush and the cap... I stopped doing it as regularly." That's Ninu's exact job in one tool.
2. **Mess means over-washing and skipping.**
   - "I have to wash my hair everyday (before minox it was every 2 days)"
   - "my hair is never really free of product"
   - "making my hair look greasy so I hate using it every day"
3. **Time:** "it took an hour, an actual 60 mins to cover all my head" (foam). This matches WebMD's twice-a-day complaints.
4. **The strongest counter-point.** A free technique works for some people: "I take the dropper and slide it along the scalp between the hair... Works great and barely makes the hair damp." So Ninu has to be clearly easier than "dropper done carefully". Our copy should acknowledge that it can be done carefully but most nights isn't.
5. **H2 conclusion matches ours.** The hands problem exists in this age group, but women don't link it to scalp products. Keep it as a supporting line, not an avatar.

## Combined verdict (with `06-older-buyer-avatars-minoxidil-and-hands.md`)

| | Evidence | Age-specific to 55+? |
|---|---|---|
| **H1: messy topical routine** | **Strong.** WebMD (verified, 25 women 55+), Gemini (unverified, about 10 quotes), our earlier Reddit notes | **Partly.** WebMD and our buyers say yes. Most Reddit quotes have no age. |
| **H2: hands** | **Weak.** General arthritis only | Yes, but not linked to hair products |

## Next
- **Verify quotes.** Open the 10 threads and confirm the quotes. That's about 10 minutes for whoever has Reddit access.
- **Amazon reviews still haven't been researched.** This needs a review-export tool, for example the Apify actor once that connector is back, on Women's Rogaine 5% foam and 2% solution, Kirkland women's minoxidil, and scalp applicators. Filter for messy, greasy, dropper, hands and age words.
- **Buyer email.** It's still the most direct answer to why they bought.
