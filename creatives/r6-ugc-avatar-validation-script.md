# R6 — AI UGC avatar format validation (single video, single hook)

Purpose: validate whether the avatar-UGC *format* converts for this product at all, before
spending on hook variants inside it. Competitor's best-performing ad for a comparable product
is UGC — worth a direct test. Per the Master Doc's Variation Winners rule, **UGC video =
FORMAT TRANSLATION**, which requires the locked angle to carry over unchanged. So this round
changes exactly one thing: the medium. Everything else — angle, mechanism, Rule of One line,
offer, and specifically the hook — is the same copy that has already converted three times
(original static control, Orange_Textincrease, Purple_Textincrease), word for word adapted to
spoken delivery.

**Why this hook and not a cheaper-performing one:** HookD/Social-Compare has better CPM/CPC
numbers, but it hasn't converted yet. Pairing an unconfirmed hook with an unconfirmed format
would make a weak result impossible to diagnose — you wouldn't know if the hook or the format
failed. This hook is the one with actual purchases behind it across three different
executions, so if the avatar version also converts, that's a clean format signal. If it
underperforms, see the read-criteria caveat at the bottom before concluding the format doesn't
work.

---

## 1. Script (adapted verbatim from `ads/ninu-dissect-winner-adC.md`)

Same beat structure and proportions as the reusable blueprint (section 10 of that file), same
Rule of One line and offer paragraph verbatim (both FIXED per that doc's section 9), condensed
and rephrased only where written-post rhythm needed to become spoken rhythm.

> I actually do my scalp oil every night now. Six months ago? Not a chance.
>
> I had the castor oil. I had the rosemary oil. I believed in the whole routine, I just could not make myself actually do it.
>
> I'd do it like four nights in a row, and then the baby would be up three times, and I'd just skip it. I'd tell myself I'd start over Sunday. I never started over Sunday.
>
> Oil on my fingers, running down my neck, soaking into the towel on my shoulders. A chore at 10pm after a full day with a baby is a chore that gets skipped.
>
> Then I found this. *(hold up the dispenser here)* It's got these hollow silicone tips. You press it right onto your scalp, along the part, and the oil goes straight there. Not on your hands. Not down your neck. Works with the oil I already had.
>
> First night I used it, I thought, oh. This is what it's supposed to feel like.
>
> By the end of the first week, I hadn't skipped a single night.
>
> The habit was always there. The routine just needed to be easier than the reason to quit.
>
> It's the Ninu Kit. Dispenser, 60ml scalp oil, a satin bonnet, forty-nine ninety-nine. Free shipping, thirty-day money-back guarantee.
>
> You try it, tonight takes two minutes and you stop skipping. You don't, Sunday comes around again.

~210 words, ~75-90 seconds at natural conversational pace. Slightly longer than a typical
15-30s UGC hook clip, but this isn't a hook-isolation round — it's testing whether the full
converting message holds up spoken, so the whole thing stays intact rather than being cut down.

**Delivery direction:** casual, talking to a phone propped up or held at arm's length, not a
polished ad-read. Natural pauses where the sentence breaks sit. Let the self-talk lines ("I'd
tell myself I'd start over Sunday. I never started over Sunday.") land with a small, dry,
almost rueful beat — that callback repetition is doing real work in the original copy and
should read as a genuine aside, not a scripted punchline.

---

## 2. Avatar persona

Same postpartum-mom identity already established across every native creative in this account
— keep it consistent, don't introduce a different-looking person:

- Early-to-mid 30s, postpartum mom aesthetic, soft warm skin tone, makeup-free or very
  minimal, slightly tired but not styled
- Dark-to-medium brown hair, worn down, slightly undone
- Oversized soft grey or oatmeal sweater/robe, same wardrobe register as the R4/R5 creatives
- Ordinary home setting — bedroom, bathroom, or living room, lived-in not styled, natural
  light
- Holds/shows the Ninu dispenser physically at the point marked in the script, same product
  reference as `creatives/r5-yap-video-prompts.md` section 0.5 if your avatar pipeline supports
  prop/product insertion

Use your existing AI UGC avatar pipeline to generate this — same persona brief as above, this
script as the voice/lip-sync track.

---

## 3. Test setup

- **New ad, new ad set**, small test budget — **not** pulled from the £85 proven pool or the
  £15/day HookD retest. Suggest £10-15/day, same checkpoint structure as every other test in
  this account.
- Checkpoints (same account-wide thresholds): £10.77 (0 link clicks) / £21.54 (0 ATC) / £32.31
  (0 IC) / £53.85 (0 purchases, hard stop)
- Single ad, single hook — do not launch 3 hook variants in this round. If this video
  converts or shows efficient top-funnel numbers, that's the gate to open a hook-isolation
  round inside the avatar format next.

---

## 4. How to read the result

- **Converts at or under break-even (£26.72), ideally near target (£21.38):** clean format win
  — avatar UGC works for this product, worth building the hook-variant round next.
- **Doesn't convert, but CPM/CPC/CTR look notably better than this hook's static-ad history
  (CPM £136.55, CPC £4.22, CAC £88.62 last time it ran):** ambiguous but encouraging — the
  format may be helping even though this particular hook is still working against it. Worth a
  second round pairing the avatar format with HookD/Social-Compare's cheaper-performing content
  before concluding anything about the format itself.
- **Doesn't convert and the efficiency numbers look just as bad as the static version's
  history:** this specific hook may simply be the common factor across both failures — not
  strong evidence against the avatar format. Re-test the format with a different hook before
  ruling it out.
- **Hits the £53.85 hard stop with 0 purchases AND efficiency numbers that are worse than
  anything else in the account:** that's the one combination that's a real signal against the
  format itself, not just against this hook.
