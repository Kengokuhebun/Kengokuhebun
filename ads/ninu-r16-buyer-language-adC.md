# R16: Buyer-language body for Ad C (one body test, everything else fixed)

Basis: `ads/ninu-core-copy-resource-breakthrough-advertising.md` (sections 3 to 6). Hypothesis: the story copy attracts readers who enjoy it but don't intend to buy, so the body needs mechanism in use, objection handling, a test, a price reason and a disqualifier before the offer.

## What stays identical (the control)

- Creative: Hook3 native image, "baby up 3 times. wet hands, in bed. skipped my scalp oil again"
- First paragraph of the primary text (hook and lead are one unit, per the master doc)
- Headline: Your messy oil routine's worst nightmare
- Link description: Free US shipping · 30-day guarantee
- CTA: Shop Now, with the tagged link (so orders keep their ad ID)
- Audience, placements (Facebook and Instagram only), budget

## What changes

The body from the second paragraph down. This is a bundled body change, so a win won't tell us which part did it. If it wins, split it in the next round.

| Change | Schwartz | Why |
|---|---|---|
| Mechanism moves up and becomes a step-by-step | ch 3, 7, 11 | She asks "how does it work?" right after the problem |
| Dropper and fingers named, each answered | ch 12 | Destroys the alternatives by method, not by brand |
| "What it won't do" paragraph | ch 13 | Disqualifies non-buyers, adds belief |
| Price stated as what she gets and a per-night figure | ch 10 | Changes what she compares it to |
| Price reason (Early Black Friday date) | ch 11 | A price needs a reason |
| Guarantee turned into a test, placed last | ch 7, 14 | Risk reversal is the closing argument |
| "Hair doesn't absorb oil. Skin does." removed | ch 9 | An absolute that a knowledgeable reader can dispute |

## Primary text (438 words)

I had the castor oil. I had the rosemary. I believed in the routine. I just couldn't make myself do it consistently.

I'd do it four nights in a row. Then the baby would be up three times and I'd get into bed with wet hands and skip it. Then I'd skip a second night. The bottle migrated to the back of the shelf and I told myself I'd start over Sunday.

I never started over Sunday.

It wasn't discipline. It was the routine. Oil on my fingers before I touched anything. Running down my neck. Soaking into the towel on my shoulders. By the time I finished one section I was already thinking about the cleanup.

A chore at 10pm after a full day with a baby is a chore that gets skipped.

Here's what I figured out. A dropper puts the oil on your hair. Fingers put it on your hands, your neck and the towel. Almost none of it was reaching my scalp, which is the only place I wanted it.

So I switched to a dispenser with hollow silicone tips. Here's how it works.

You part your hair. You press the tips against your scalp along the part. The oil releases right there, on the skin. Nothing runs. Nothing drips. Then you move down the part and do the next one. There's a clear chamber with 1 to 4ml markings, so you can see how much you're using.

One hand. About two minutes. It works with the oil I already had.

The first night I thought: oh. This is what it's supposed to feel like.

By the end of the first week I hadn't skipped a night. That had never happened.

Here's what it won't do. It won't make your oil work harder, and it won't do the routine for you. It makes the routine easy enough that you actually do it. If you don't want to oil your scalp, this isn't for you.

If you do, here's the kit: the dispenser, 60ml of scalp oil (about a month of nights) and a satin sleep bonnet. $49.99, with free US shipping. That's about $1.67 a night to start.

It's $49.99 until Nov 10 for our early Black Friday sale. On Nov 11 it goes to $62.49.

And you can test it properly. Use it every night for 30 days. If the routine isn't easier and the oil isn't landing where I said it would, you get your money back.

The habit was always there. The routine just needed to be easier than the reason to quit.

Make tonight the easy one. Tap Shop Now.

## Line-by-line source and compliance

| Line | Source | Check |
|---|---|---|
| Lead, skipping, towel, cleanup, "chore at 10pm" | Ad C (R8 control), unchanged or lightly trimmed | Existing converted copy |
| "A dropper puts the oil on your hair... almost none of it was reaching my scalp" | Rewrites Ad C's "hair doesn't absorb oil, skin does" as experience | Behaviour claim; no absolute |
| Hollow silicone tips, press along the part, oil releases on the skin, clear chamber, 1 to 4ml | Ad C mechanism paragraph and product spec | Unchanged facts |
| "Nothing runs. Nothing drips." | Ad C | Existing claim |
| "One hand. About two minutes. Works with the oil I already had." | Ad C ("Two minutes") | Existing; "about" softens it |
| "I hadn't skipped a night" | Ad C | First-person brand voice, not a testimonial |
| "What it won't do" paragraph | New; Schwartz ch 13 | Adds no claim; narrows one |
| Kit contents | PDP kit checklist | Ebook deliberately left out (delivery not built) |
| "$1.67 a night" | 49.99 divided by 30 | Arithmetic only |
| "Until Nov 10... Nov 11 it goes to $62.49" | Existing offer line | **True only if the Shopify price and the page `TIER` kit price actually change on Nov 11** |
| 30-day test and refund | Store guarantee | Does not describe a return process, which I haven't confirmed |
| No em dashes, no questions, no exclamation marks | Master doc writing rules | Checked |

Do not run this copy until the Nov 11 price change is set up, or delete the two price-reason lines.

## Test design

| | Control | Variant |
|---|---|---|
| Name | A1_C_Hook3_Control | A1_C_Hook3_BuyerBody |
| Body | Ad C, 428 words | the text above |

- Same ad set if budget allows; if not, same budget in two separate ad sets so Meta isn't splitting one learning phase. At roughly £20 a day total, that means £10 each, which is thin. I'd rather run them in turn on one ad set: control a few days, then variant.
- Judge in this order: (1) link CPC, which should not move because the creative and first lines are unchanged; (2) add-to-cart per link click; (3) cost per add-to-cart; (4) purchases.
- Kill checkpoints: £14 with 0 link clicks, £28 with 0 add-to-cart, £42 with 0 checkout, £54 with 0 purchases.
- Sample size: about 100 link clicks is enough to read link CPC. It is NOT enough to read add-to-cart rate. At a 0.7% add-to-cart rate, 100 clicks gives about 1 add-to-cart, so telling 0.7% from 2.5% needs roughly 300 to 400 clicks per ad (about £160 to £210 each at £0.53 a click). At £20 to £25 a day, that means one clean test at a time, or comparing one ad against the 0.7% baseline instead of a parallel control.
- What would confirm the hypothesis: link CTR roughly equal across the two and add-to-cart per click clearly higher on the variant.
- What would not: both flat, which points back to the page, price or trust.
- Sample caution: Hook3 has 50 clicks and at most one add-to-cart so far. This is a direction, not a result.

## Options to test later (one variable per round)

1. Headline: "Scalp oil that lands on your scalp, not your towel" / "One hand. Two minutes. Oil on the skin, not the towel."
2. Hook that filters: "if your scalp oil is at the back of the shelf, read this"
3. Product named inside the first 125 characters, before Meta's "See more" fold
4. Short version (about 120 words): lead, mechanism, kit, price, guarantee
5. The "hair doesn't absorb oil" line on its own against the experience-only version
