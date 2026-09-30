# Ninu — Logo Generation Prompts

Written for Nano Banana Pro / Nano Banana 2. Also works with Ideogram, Midjourney v6/v7, and Flux with minor tweaks.

## Before you generate — read this once

**Image generators are unreliable at clean, exact typography.** They'll get the letterforms close but often add extra characters, distort spacing, or invent a serif detail that doesn't exist. The realistic workflow is:

1. Generate 6–10 variants from the prompt below.
2. Pick the direction you like most (letter proportions, tracking, weight).
3. **Rebuild the final wordmark in a real font tool** — Figma, Canva, Adobe Illustrator — using the actual font (Cormorant Garamond is what the PDP uses and it's free on Google Fonts). This is what makes it production-ready.
4. Export SVG + PNG in cream, ink, and white versions for every place you'll need it (favicon, header, packaging, invoices, Meta Business page).

If you want a one-shot AI logo without the rebuild step, use **Ideogram** — it's currently the most reliable image model at getting typography exactly right.

---

## Prompt 1 — Primary wordmark (matches the PDP header)

```
An elegant editorial wordmark logo. The word "NINU" written in a refined thin serif typeface (like Cormorant Garamond, Didot, or Bodoni), all capital letters, with very wide letter-spacing so the letters read as "N  I  N  U" with generous air between each character. Deep espresso ink color (#241812) on a warm cream background (#F5EFE6). The letters are crisp, precise, and calm — spa/apothecary energy, not fashion-loud. No decorative flourishes, no icon, no tagline, no additional characters. Perfectly horizontally centered, generous whitespace above and below. Aesop, Le Labo, Hermès Beauty mood. Photorealistic print quality. Square 1:1 composition.
```

**What to watch for in generation:**
- Extra letters (some models will add an "M" or a stray dot — regen or crop)
- Uneven letter-spacing between pairs (reroll if I-N is tighter than N-I)
- Sans-serif drift — if it comes back looking like Futura, add "definite serif with subtle stroke contrast" to reinforce

---

## Prompt 2 — Stacked/monogram lockup (for narrow spaces)

Use this for favicons, IG profile pictures, or wax-seal-style stamps on packaging.

```
A minimal serif monogram-style logo. The single letter "N" in a refined thin serif capital (Cormorant Garamond or Didot family), deep espresso ink color (#241812), centered inside a thin single-line circle of the same color, on a warm cream background (#F5EFE6). The letter and circle are both drawn with the same delicate line weight. No shadows, no gradients, no additional text or ornament. Feels like a hand-pressed wax seal or an apothecary shop mark. Square 1:1 composition.
```

**Use case:** favicon, Meta ad watermark, Shopify product tab icon, seal on the satin bonnet bag.

---

## Prompt 3 — Wordmark + descriptor (for the landing page hero, optional)

```
An elegant editorial two-line wordmark logo. TOP LINE: the word "NINU" in a thin serif capital typeface (Cormorant Garamond, Didot family), all caps, wide letter-spacing, deep espresso ink color (#241812), large and centered. BOTTOM LINE: the small-caps descriptor "SCALP RITUAL" underneath, in the same serif but half the size, wide letter-spaced, also espresso ink, centered directly under the wordmark. A single thin horizontal hairline of the same color separates the two lines. Warm cream background (#F5EFE6), generous whitespace around, no other elements. Aesop / Le Labo apothecary mood. Square 1:1.
```

**Use case:** landing page hero above the fold, business card, packaging front label.

---

## Prompt 4 — Alt color / dark-mode version

Same as Prompt 1 but flipped for dark backgrounds — good for Instagram Reels covers or a dark-theme footer.

```
An elegant editorial wordmark logo. The word "NINU" written in a refined thin serif typeface (Cormorant Garamond, Didot family), all capital letters, very wide letter-spacing so the letters read as "N  I  N  U" with generous air between each character. Warm cream color (#F0E6D8) on a deep espresso ink background (#241812). The letters are crisp, precise, and calm — apothecary mood, no decorative flourishes, no icon, no tagline. Perfectly horizontally centered, generous whitespace. Square 1:1.
```

---

## Color and font reference (already in the PDP)

Copy these into whichever tool you rebuild in:

| Element | Value |
|---|---|
| Ink (primary logo color) | `#241812` |
| Cream (background) | `#F5EFE6` |
| Terracotta accent (only if adding a colored version) | `#B85A3E` |
| Cream on dark | `#F0E6D8` |
| Font | Cormorant Garamond (free — Google Fonts) |
| Weight | 400 or 500 (regular / medium — not the ultra-thin 300) |
| Letter-spacing | 0.28em (very wide, like "N   I   N   U") |
| Case | All caps |

## After you pick a direction

Ping me and I can:
- Sketch the SVG code for the chosen wordmark so you can drop it straight into the PDP nav (replacing the current `.ninu-logo` styled text) — this is the cleanest way to get a crisp logo everywhere
- Generate a favicon set (32×32, 180×180 Apple touch, 512×512 PWA) in the right formats for Shopify
- Draft a small brand-guide doc so future ads and packaging stay on-brand
