# R21: What to do after the R16 test passes (stack, diversify, scale, scarcity)

Written 2026-11-04. Builds on R16 (the buyer-language test), R19 and R20 (offer), and the kill checkpoints in `ninu-kill-criteria.md`.

## 0. Two premises to adjust first

1. **"Validated" isn't established yet.** The orange colour post has 1 sale in about £107 (Hook1_OG) and one cheap-click ad (Hook3, 50 clicks, at most 1 add-to-cart). CTR and CPC are a hook read, not a buyer read. Until an ad produces purchases at a workable cost, treat the format and hooks as promising.
2. **You don't have enough data for cost caps yet.** You have 7 orders in total. Cost and bid caps need a stable, known CPA. Below that, a cap set too low simply stops delivery, and set too high it does nothing. Meta's usual guidance is about 50 optimisation events a week to exit the learning phase (my recollection, check the current Meta help page). At a £27 CAC that's roughly £190 a day. You're spending £20 to £25.

## 1. Passing R16 is not the same as scaling

R16 "pass" = 5 or more add-to-carts from about 225 sessions. At your funnel (about 58% of add-to-carts become orders) that's about 3 orders for about £160, a CAC near £55. That's better than today and still above break-even (£26.72). So a pass means "the copy helps, keep improving it", not "scale it".

## 2. The sequence after a pass

Each round changes one thing, runs to about 300 clicks (about £160 at £0.53 a click), and the winner becomes the new control.

| Round | Variable | Test | Reads on |
|---|---|---|---|
| 1 | Hook | 3 hooks on the R16 body (identity, pain, mechanism). Same image style | Add-to-cart per click, not CTR |
| 2 | Format | R16 body on photo native (R18 prompt 1), headline native, Notes native | Link CPC first, then add-to-cart per click |
| 3 | Offer on the page | Gift stack live (R20), once the gifts exist | Add-to-cart rate and CAC |
| 4 | Scarcity layer | Real deadline in the copy (section 5) | Purchase rate from add-to-cart, plus CAC |

Rounds 1 and 2 can run as separate ads in one test ad set only if you can afford about £50 per ad to read CPC. If not, run them in turn.

## 3. Creative diversity: what counts

Meta's ad system tends to reward creatives that are genuinely different from each other, not recolours of one (my reading of Meta's public comments on its ad ranking, not verified here). A new colour or wording on the same image is one creative, not two.

Concepts that are different enough to count, using assets that already exist or are specified:

| # | Concept | Format | Status |
|---|---|---|---|
| 1 | Habit story, orange post | Static | Built (Hook3) |
| 2 | 3am wet hands | Photo native | Prompt written (R18) |
| 3 | Notes screenshot | Static | Built (R13), R17-A copy |
| 4 | Headline "…more" native | Static | Prompt/spec written (R18) |
| 5 | Sung 3D video | Video | v3 built |
| 6 | What's in the box (gift stack flat-lay) | Photo | Needs real gifts and photos |
| 7 | Mechanism demo, press the tips | Short video or photo | Needs real product footage |
| 8 | Gift for a new mom (Christmas) | Static | New angle, see section 5 |

Production plan: batch the statics (2 to 4 are quick), launch in waves of 3 to 4, kill on the checkpoints (£14 with 0 link clicks, £28 with 0 add-to-cart, £42 with 0 checkout, £54 with 0 purchases). At about £50 per ad to read CPC, 8 concepts costs about £400. At £20 to £25 a day that's about three weeks. Be selective.

## 4. CBO and cost caps: when and how

**Gates to open a scaling campaign (my suggested numbers, adjust as data arrives):**
- At least 15 to 20 purchases from at least 2 different creatives, over at least 7 days.
- CAC at or below about £30 across them, with break-even at £26.72.
- Add-to-cart rate stable at or above about 2.5% on the page you're actually running.
- The ad account is paid up and PayPal is resolved.

**How:**
1. Duplicate the winners into a new campaign. Don't move them; moving resets learning.
2. Start **without** a cap. Let it find the cheapest purchases first.
3. **CBO needs budget.** CBO sends most spend to one or two ads and starves the rest. At £25 a day, CBO will do that. Use **ABO** for testing. Move to CBO only when daily budget reaches about £25 to £30 per ad you want to keep alive (about £100 a day for 4 ads).
4. Add a **cost cap** only after you have a stable CAC. Set it at about 1.2 times your average CAC, and never above break-even (£26.72). If the average is above break-even, you don't have a cap problem. You have a funnel problem.
5. If a cap stops delivery, raise it by about 10 to 20%. Don't edit budgets or caps more than once every 2 to 3 days.
6. **Bid caps** are more fragile than cost caps for a store this size. I'd skip them.
7. Optimisation event: keep Purchase. Optimising for add-to-cart or checkout gives Meta more events but can pull in the same non-buyers you're trying to filter out. Revisit only if you can't get enough purchase events.

## 5. Scarcity that is true (and what to avoid)

**Real and usable:**
- **The Early Black Friday deadline.** $49.99 ends Nov 10 and goes to $62.49 on Nov 11. That's a true deadline, if you change the price. Put it in the copy and the creative. Then **keep your word.** If the price doesn't move on Nov 11, every later deadline loses credibility.
- **Real calendar events.** Black Friday week (Nov 24 to 30) and Cyber Monday are legitimate, separate sales. Use a new, real offer for each. Don't re-run the same countdown.
- **A limited gift batch.** If you buy a fixed number of massagers and pouches, say so ("first 150 kits") and track it with real inventory on the gift item. Show a real count only if it's real. Then end the gift when it ends.
- **Christmas shipping cutoff.** "Order by Dec X to arrive before Christmas" is true urgency, but only after you confirm real delivery times with the supplier (your page says 6 to 12 days). This also opens an angle: a gift for a new mom, bought by a partner or friend.

**Avoid:**
- Fake stock counters, "only 3 left" with untracked inventory, and countdown timers that reset for each visitor. These are deceptive, can get you refunds and chargebacks, and are regulated. I removed the always-on "Low stock" pill from the page for this reason.
- Extending a "last day" without a real reason.

## 6. Cash and Q4

- CPMs rise from about Black Friday week into early December. Don't plan to scale into that window unless CAC is already below break-even.
- Rule of thumb: if spend since your last purchase passes £54, pause that ad.
- Reinvest from payout dates. Don't scale on money you don't have.

## 7. The next decision

Run R16 first. Then come back with the add-to-cart numbers and purchase count and we'll pick the round-1 hooks from them.
