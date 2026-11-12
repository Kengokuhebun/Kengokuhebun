# Ninu: avatar candidates, sizing and scores

Written 2026-11-12 using the mentor's method in `master-doc/01-find-avatars.md`: each candidate gets a market-size estimate (TAM, the number of US women per year who fit) and a score out of 25.

**Evidence base:**
- 33 Reddit threads the owner captured, about 1,300 comments, all read in full. Notes are in `raw/notes-01.md`, `raw/notes-02.md` and `raw/notes-03.md`, and the earlier write-ups are `00-drive-folder-findings.md` and `00b-drive-batch2-findings.md`.
- Population figures from the web searches listed under each TAM.

**Target country:** US only, because 94% of store sessions are from the US.

**Tags:**
- [REDDIT] = read in a thread.
- [SOURCE] = a population or prevalence figure, with its link.
- [ESTIMATE] = my own number. Each one is shown and should be read as a guess.
- [BRIEF] = from the store and ad data in the repo.

---

## Step 1. Who is already taken

[BRIEF] Ninu and every past ad were aimed at postpartum mothers with hair shedding, using the habit-and-delivery angle from Ad C. In Meta's data, those mothers didn't buy: 6 of the 7 purchases and 14 of the 16 add-to-carts came from women 55+.

[REDDIT] The generic applicator brands target young women with hair loss on r/FemaleHairLoss and r/tressless:
- Amazon applicator combs at "$8" to "$10", plus WL-YBOPRO
- Kitsch
- unbranded "$2" applicators from China
- "There are dozens of these types of scalp applicators on Amazon, TT, Temu etc."
- Someone in r/tressless asked whether the comments were bots, because they had seen "quite a few ads recently in here for this"

[REDDIT] Hair-loss treatment brands target the same young group and older women too: Hers, Nutrafol, Rogaine and Viviscal are all named repeatedly.

None of the threads mention an applicator brand speaking to women going through menopause about putting oil on the scalp.

---

## Step 2. Population and prevalence figures used

| Figure | Value | Source | Caveat |
|---|---|---|---|
| US women aged 55 to 64 (2024) | 21,069,250 | [SOURCE] [FRED LFWA55FEUSA647S](https://fred.stlouisfed.org/series/LFWA55FEUSA647S) | Working-age series. I could not find a verified 45 to 54 or 65+ figure this session, so those groups are **left out**, which keeps every TAM conservative |
| US women entering menopause each year | about 1.3 million | [SOURCE] [StatPearls / NCBI NBK507826](https://www.ncbi.nlm.nih.gov/books/NBK507826/) | An estimate, not a census count |
| Women in perimenopause or menopause reporting hair symptoms | 84% (itchy scalp 44%, dry scalp 24%) | [SOURCE] [BJD 2026 abstract, England, n=1,457](https://www.citedrive.com/en/discovery/bh26-characterizing-hair-changes-in-menopause-symptom-patterns-and-help-seeking-behaviours/) | A conference abstract from England, used as a stand-in for US women |
| Postmenopausal women aged 50 to 65 with female pattern hair loss | 52.2% | [SOURCE] [Menopause 2022, PubMed 35357365](https://pubmed.ncbi.nlm.nih.gov/35357365/) | Small study at one Thai clinic, n=178 |
| US women who oil their hair | 25% | [SOURCE] [YouGov, Aug 2025, n=1,236](https://yougov.com/en-us/articles/52808-us-hair-care-trends-2025-consumer-concerns-routines-and-market) | All adult women, not split by age |
| US women with pattern hair loss (AGA) | about 30 million | [SOURCE] [JDD](https://jddonline.com/articles/dermatology/S1545961624P1360X) via search results | All ages |
| Share of women using topical minoxidil | **not found** | none | Any number I use for this is [ESTIMATE] |

---

## Step 3. TAM: US women per year who fit each candidate

The mentor's bar is 500,000.

**A. Woman in or after menopause whose hair and scalp have changed**
- 21.07M women aged 55 to 64 [SOURCE]
- × 84% with hair symptoms [SOURCE]
- × 20% for whom it's urgent, not mild [ESTIMATE]. This is conservative because the Reddit intensity is high ("I hate myself, cannot bear to look in the mirror").
- = **3.54M**. Clears the bar.
- For comparison, counting only women *entering* menopause: 1.3M × 84% × 20% = 218k a year. Women in this stage stay in it, so the "in stage" figure above is the one used for scoring.

**A1. ...with a dry or itchy scalp, who already oils her hair**
- 21.07M [SOURCE]
- × 44% with itchy scalp [SOURCE]
- × 25% who oil their hair [SOURCE]
- × 30% for whom it's urgent [ESTIMATE]. Reddit shows it waking women at night, with 188 comments in one thread.
- = **0.70M**. Clears the bar. This assumes the itch and oiling figures are independent of each other [ESTIMATE].

**B. Recently diagnosed with AGA, aged 35+**
- 30M [SOURCE]
- × 70% aged 35+ [ESTIMATE]
- × 15% for whom it's urgent [ESTIMATE]
- = **3.15M**. Clears the bar. Two of the three factors are my estimates, so treat this one with caution.

**C. Woman aged 50+ using topical minoxidil**
- 30M [SOURCE]
- × 10% using topical minoxidil [ESTIMATE, no source found]
- × 50% aged 50+ [ESTIMATE]
- × 40% for whom application is a real struggle [ESTIMATE]
- = **0.60M**. Clears the bar on paper, but **mostly my estimates**.

**D. Woman aged 55+ going grey**
- 21.07M [SOURCE]
- × 25% who oil [SOURCE]
- × 10% for whom it's urgent [ESTIMATE]
- = **0.53M**. Only just clears the bar.

**E. Woman who stopped using rosemary oil**
- 21.07M [SOURCE]
- × 25% who oil [SOURCE]
- × 30% who quit [ESTIMATE]
- × 30% for whom it's urgent [ESTIMATE]
- = **0.47M**. Below the bar.

**F. Woman with a weak grip or arthritis:** not sized. No Reddit evidence was found.

**TAKEN. Postpartum mothers:** not re-sized. The Meta data shows they don't buy.

---

## Step 4. Scores out of 25

Each column is scored 1 to 5:
- **Size:** the TAM above.
- **Pain:** how urgent the problem is on Reddit.
- **Spend:** whether they'd pay the kit price.
- **Reach:** how easily Meta can find them.
- **Open:** how untouched the space is (5 = no competition).

| Rank | Avatar | Type | TAM per year | Clears 500k | Urgent desire | Size | Pain | Spend | Reach | Open | **Total** | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **A. Woman in or after menopause whose hair and scalp have changed** | Life stage | 3.54M | Yes | PASS | 4 | 4 | 4 | 4 | 3 | **19** | PRIORITY |
| 2 | **A1. ...with a dry, itchy scalp at night, already oiling** | Life stage (part of A) | 0.70M | Yes | PASS | 3 | 5 | 4 | 3 | 4 | **19** | PRIORITY |
| 3 | B. Recently diagnosed with AGA, 35+ | Life stage | 3.15M | Yes | PASS | 4 | 4 | 3 | 3 | 2 | **16** | PRIORITY, but the voices are young (below) |
| 4 | C. Aged 50+ using topical minoxidil | Group | 0.60M (mostly estimates) | Yes, weakly | PASS | 3 | 4 | 3 | 3 | 2 | **15** | **TEST** (downgraded for compliance) |
| 5 | D. Aged 55+ going grey | Life stage | 0.53M | Just | **FAIL** | 3 | 2 | 4 | 4 | 3 | 16 | **TEST** (the rules cap it) |
| 6 | E. Stopped using rosemary oil | Group | 0.47M | **No** | **FAIL** (no evidence) | 2 | 2 | 4 | 3 | 4 | 15 | **TEST** (the rules cap it) |
| 7 | TAKEN: postpartum mothers | Life stage | not re-sized | n/a | PASS | 4 | 4 | 2 | 5 | 1 | 16 | Taken, and Meta shows they don't buy |
| 8 | F. Weak grip or arthritis | Group | not sized | n/a | FAIL | n/a | n/a | n/a | n/a | n/a | n/a | AVOID (no evidence) |

**Why the scores are what they are:**

- **A, Pain 4.** Their own words:
  - "I hate everything about how I look. I don’t recognize myself anymore."
  - "My hair has always been my best feature" (two women, aged 66 and 69)
  - "The pain of thin greying hair is horrible."
- **A, Spend 4.** They already pay:
  - $96 shampoo ("Holy hell is this expensive")
  - Nutrafol, Hers, extensions, $125 keratin treatments
- **A, Reach 4.** All 7 of your buyers came through Meta, mostly on Facebook Feed at 55+.
- **A, Open 3.** Supplement and medicine brands target them. In the threads, nobody sells them a way to apply oil.
- **A1, Pain 5.**
  - "drives me crazy at night when I'm laying in bed"
  - "My dermatologist says it’s all in my head"
  - "I have tried everything"
  - The thread has 188 comments.
- **A1, Open 4.** Every remedy in the threads is a shampoo or a prescription. Women apply oil with their fingers.
- **A1, Reach 3.** There's no clean Meta interest for itchy scalp, so the creative has to do the filtering.
- **B, Open 2.** Hers, Nutrafol, Rogaine and dozens of applicators all target this group. The ages in the evidence are 15 to 40, so it doesn't match who bought.
- **C, why only TEST.** About 12 users aged 50 to 76 are confirmed, but:
  - Selling Ninu as a minoxidil applicator moves it into a drug context.
  - Ninu hasn't been tested with minoxidil liquid.
  - Applicators already sell for $2 to $10.
- **D, why it fails.** The grey-hair threads are about frizz on the lengths and feeling invisible, not the scalp.
- **E, why it fails.** No woman in any thread says she gave up on rosemary oil. There are only 2 weak mentions in total.

---

## Step 5. The one angle to test per avatar

These are hooks for testing, not finished ads. Every hook below is reworded from a real quote, and the source quote is underneath it.

### 1. A. Woman in or after menopause whose hair and scalp have changed

- **TAM:** 3.54M a year. **Verdict:** PRIORITY.
- **Primary desire:** to recognise herself again.
- **Awareness:** problem aware. She knows something changed and has already tried supplements, shampoos and minoxidil.
- **Emotional driver:** grief and disbelief ("Is this my life now?").
- **Angle family:** identity led, then mechanism.
- **The argument in one sentence:** Your hair changed, your routine didn't, and the oil you rely on is landing on your hair instead of your scalp.
- **Hook:** "My hair was always my best feature. Then menopause happened."
- **Built on:**
  - "My hair has always been my best feature. [...] Now, I don't recognize it." [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1owbf6d/)
  - "I hit menopause early [...] I am now 66 and I have no idea wtf to do with it." [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1owbf6d/)
  - "WTH?!?!? Anyone else? Is this my life now?" [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1qxsy28/)

### 2. A1. ...with a dry, itchy scalp at night, already oiling

- **TAM:** 0.70M a year. **Verdict:** PRIORITY.
- **Primary desire:** a calm scalp at bedtime, without oily hair.
- **Awareness:** solution aware. She already oils her scalp with her fingers.
- **Emotional driver:** frustration at doctors who dismiss it.
- **Angle family:** trigger moment, then mechanism.
- **The argument in one sentence:** If you oil your scalp at night, put it on the skin and not through your hair, in two minutes with one hand.
- **Hook:** "My dermatologist said it was all in my head. My scalp disagreed at 11pm."
- **Built on:**
  - "My dermatologist says it’s all in my head." [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1rl2dyz/)
  - "drives me crazy at night when I'm laying in bed" [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1l164bf/)
  - "I tried applying oil to my scalp on the itchy parts only." [REDDIT](https://www.reddit.com/r/Perimenopause/comments/1hykg1v/comment/mklerqs/)
  - "I've been using Rosemary oil at night." [REDDIT](https://www.reddit.com/r/AskWomenOver50/comments/1rl2dyz/)
- **Compliance:** delivery claims only. Never say Ninu stops or relieves itching.

### 3. B. Recently diagnosed with AGA, 35+

- **Angle:** failed solutions. The dropper wastes it on your hair.
- **Hook:** "So much would get on my hair instead."
- **Built on:**
  - OP quote [REDDIT](https://www.reddit.com/r/FemaleHairLoss/comments/1vrn16i/)
  - "the stupid dropper [...] put most of the medication in my hair vs on my scalp" [REDDIT](https://www.reddit.com/r/FemaleHairLoss/comments/1w2jkcv/)
- **Note:** the evidence is from women under 40. Test this only if A and A1 fail.

### 4. C. Aged 50+ using topical minoxidil

- **Angle:** habit. This is Ad C's angle, and it's proven here: "is the #1 reason I've stayed consistent" [REDDIT](https://www.reddit.com/r/FemaleHairLoss/comments/1wcxff6/)
- **Hook:** "The task I'd find any excuse to skip now takes two minutes."
- **Built on:**
  - "Suddenly this usually annoying task I’d find any excuse to skip is quick and even pleasant? Like a mini massage at the end of the day." [REDDIT](https://www.reddit.com/r/FemaleHairLoss/comments/1oduxup/)
- **Before testing:** check compliance and test Ninu with minoxidil liquid.

### 5 to 8. D, E, TAKEN and F

No angle. Each is either capped at TEST or has no evidence.

---

## Strategic recommendation

- **Launch with A, the woman in or after menopause, and test A1's night-time scalp hook against A's identity hook in the same ad set.** That's one variable, the hook, with the same body and offer. A matches the ages of everyone who bought and is the largest group that clears the bar. A1 is where the pain is sharpest and where women already oil their scalps with their fingers.
- **Move to C after proof, and only after the compliance and product-fit checks.** It has the strongest evidence for the habit angle that sold Ad C.
- **A and C share the same emotional driver** (consistency, and feeling like herself), so the Ad C body copy can carry both if the hook changes.

---

## Method log and honesty notes

- **Read:** 33 threads, about 1,300 comments, in 7 subreddits: r/FemaleHairLoss 20, r/AskWomenOver50 10, r/AskWomenOver40 2, r/Perimenopause 1, r/minoxidil 1, r/tressless 1. Some threads overlap. The 2 image-only PDFs were read as page images, and comments hidden behind "more replies" were not captured.
- **Amazon reviews:** none read. That's 0% against the mentor's 10% cap.
- **Below the mentor's minimums:**
  - The mentor wants 15 threads per avatar. Only A and B reach that. A1 has 4 scalp threads.
  - Ring 3 and Ring 4 communities beyond r/AskWomenOver* haven't been read: r/Menopause and venting subreddits.
- **Weakest numbers:**
  - Every "urgent" share is my estimate.
  - Topical minoxidil usage has no source at all.
  - Women aged 45 to 54 and 65+ are left out of every TAM, so A and A1 are understated.
- **Still unproven:** a woman over 55 saying in her own words that she keeps skipping oiling because it's messy. The habit evidence comes from minoxidil users of unknown age.
- **Next research:**
  - r/Menopause threads on scalp or hair oil (leads are listed in `raw/notes-03.md`).
  - "Minoxidil is annoying to apply" (93 comments).
  - Competitor reviews on Amazon for the applicator comb B0CKXF5QPF and WL-YBOPRO.
