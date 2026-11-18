# Hook test: dinner-ledger (2026-11-18)

Base: `Glowling_R1_BF26_C1-S1-dinner-ledger`, spec at `ad-specs/ad-spec-glowling-dinner-ledger.md`.
Rule: only paragraph 1 changes. Paragraphs 2-31, headline, description, button, link, UTMs and the image (fixed 4:5 version, `ads/launch/fixed-creatives/C1-S1-dinner-ledger_fix.jpg`) are identical in every cell.
Spec checks for the hook (all four pass): 45 words or fewer; contains the $847 total, a clock time, a weekday, and both names (Noah, Eli); 0 question marks, 0 exclamation marks, 0 contractions. Only facts already in the ad are used (no new numbers, names or events).

## Cells

**A. Control** (scene + total, unchanged, 45 words)
I added up what I had spent trying to keep my boys off the iPad before dinner. $847 since January. I made the list on my phone at 5:51 pm on a Wednesday, while Noah cried for Bluey and Eli pulled at the oven handle.

**H1. Number-first** (37 words). Slot changed: order of [TOTAL] and [DATED MOMENT]; the total opens the ad.
$847 since January. That is what I added up at 5:51 pm on a Wednesday, trying to keep my boys off the iPad before dinner, while Noah cried for Bluey and Eli pulled at the oven handle.

**H2. Item-first** (41 words). Slot changed: [SPEND STATEMENT] replaced by one ledger line from paragraph 6 (the easel); the total closes the hook.
A $142 easel. Used three times. In the garage. It was one line on the list I made at 5:51 pm on a Wednesday, while Noah cried for Bluey and Eli pulled at the oven handle. The list came to $847.

**H3. Result-first** (43 words). Slot changed: [SPEND STATEMENT] replaced by the 22-minute result from paragraphs 22-24.
I cooked for twenty-two minutes last Tuesday and the iPad never came out. Before that, $847 since January and nothing lasted. I made the list at 5:51 pm on a Wednesday, while Noah cried for Bluey and Eli pulled at the oven handle.

Reserve (not in this round): Discovery-first, opening on the friend's text (paragraph 14).

## Design (proposed, not built)
- New campaign `Glowling_R1_BF26_HOOK_TEST`, ad-set budgets, Canada only (US-dollar copy fits; no consent banner; cheapest CPM), ages 28-65+, same settings as the main campaign. One ad set per cell, so budgets stay equal.
- £6/day per cell = £24/day, 3 days = about £72.
- Judge on: link CTR, CPC and cost per landing page view (hook rate does not apply to static images). Flag-only: CTR under 0.7% after 1,500 impressions in a cell. Nothing paused automatically.
- Funding: current pace is about £70/day (CBO £40 + UK up to £30). Lifetime spend is about £300 against the £400 ladder step.

## Listicle
User confirmed the named testimonials are real: keep proof for each (screenshot, email or order) on file. Rebuild proceeds in parallel at no ad cost once the hooks are approved.
