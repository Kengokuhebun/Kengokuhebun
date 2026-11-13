# NotebookLM research kit: topical messy-routine avatar (55+) and hands angle

NotebookLM can only read sources you add to the notebook. It doesn't browse the web on its own. That's actually useful here: every answer is tied to a source with a click-through citation, so nothing can be made up. The work is in 3 steps: **1. add sources, 2. set the instructions, 3. run the 5 prompts in order.**

---

## STEP 1: Add sources (about 20 minutes)

NotebookLM often can't read Reddit pages from a link. For each Reddit thread, the most reliable way is:
1. Open the thread in your browser.
2. Expand all comments ("View more comments" and "more replies").
3. Save the page as PDF (Ctrl/Cmd+P, then Save as PDF).
4. Upload the PDF.

That's what you did for the menopause research, and it worked.

**A. Reddit threads (save each as PDF; the more, the better)**

Verify Gemini's quotes:
- https://www.reddit.com/r/FemaleHairLoss/comments/vmk4gd/
- https://www.reddit.com/r/FemaleHairLoss/comments/1xom6dv/
- https://www.reddit.com/r/FemaleHairLoss/comments/1ssgb4z/
- https://www.reddit.com/r/FemaleHairLoss/comments/1c468jg/
- https://www.reddit.com/r/FemaleHairLoss/comments/1ff90rt/
- https://www.reddit.com/r/FemaleHairLoss/comments/qpzq7w/
- https://www.reddit.com/r/Menopause/comments/1j27h5j/
- https://www.reddit.com/r/tressless/comments/u1wi2k/
- https://www.reddit.com/r/Menopause/comments/1svsmmv/
- https://www.reddit.com/r/Menopause/comments/zo9p67/

Highest value (big application-pain threads):
- https://www.reddit.com/r/FemaleHairLoss/comments/1m5117d/ ("Minoxidil is annoying to apply", 93 comments)
- Search r/FemaleHairLoss for "Anyone else find minoxidil application annoying/messy" and save it
- https://www.reddit.com/r/FemaleHairLoss/comments/1wcxff6/ ("Minoxidil Applicator", 135 upvotes)
- https://www.reddit.com/r/FemaleHairLoss/comments/1stomyv/ ("How to apply minoxidil properly over entire scalp?")

Older women (age context):
- https://www.reddit.com/r/AskWomenOver50/comments/1rl2dyz/ (itchy scalp, 188 comments)
- https://www.reddit.com/r/AskWomenOver50/comments/1l164bf/ (scalp after 55)
- https://www.reddit.com/r/AskWomenOver50/comments/1kjm6u6/ (age 76 Rogaine user)
- https://www.reddit.com/r/AskWomenOver50/comments/1i5eksp/

Find 10 more yourself:
- Use Reddit's search box inside each subreddit: r/AskWomenOver50, r/AskWomenOver60, r/Menopause, r/FemaleHairLoss, r/GreyHair, r/Arthritis, r/rheumatoid.
- Search these terms: `rogaine`, `minoxidil`, `scalp oil`, `rosemary oil`, `dropper`, `foam`, `greasy`.
- Pick threads with 20+ comments where people talk about **applying** the product.

**B. Review pages (add as website links; if a link fails, save the page as PDF)**
- https://reviews.webmd.com/drugs/drugreview-minoxidil-topical-rogaine (pages 1 to 6, each saved as PDF; we've already extracted 25 reviews from women 55+)
- https://www.drugs.com/comments/minoxidil-topical/ (all pages)
- https://www.mykitsch.com/products/scalp-oil-applicator (reviews section)
- Amazon: Women's Rogaine 5% Foam, Women's Rogaine 2% Solution, a minoxidil applicator bottle and a scalp oil applicator comb bottle. Open each product, click "See more reviews", filter to 1–3 stars, and save 2 to 3 review pages per product as PDF.

**C. Use NotebookLM's "Discover sources" (the + Add > Discover button)**

Paste each of these and add the relevant results:
- older women messy minoxidil application greasy hair
- arthritis hands difficulty squeezing dropper bottle hair products
- women over 60 scalp oil routine tips
- rogaine foam hard to use arthritis

**D. Our own research files (upload these too)**

These are in the GitHub repo:
- `avatar-research/06-older-buyer-avatars-minoxidil-and-hands.md`
- `avatar-research/08-gemini-report-review.md`
- `avatar-research/00b-drive-batch2-findings.md`

Label them so NotebookLM knows they're our notes, not customer quotes.

---

## STEP 2: Set the notebook's instructions

In the chat panel, click **Configure** (the settings icon), choose **Custom**, and paste:

```
You are a strict voice-of-customer researcher for a scalp oil applicator brand. Rules for every answer:
1. Quote customers VERBATIM only, copied exactly from the sources, with a citation to the exact source passage. Never paraphrase a customer and present it as a quote. Never combine two people's words.
2. Only use customer quotes from Reddit threads, review pages and forums. Files named 06-, 08- or 00b- are OUR OWN NOTES: use them for context, never as customer quotes.
3. For every quote, state the AGE SIGNAL found in the source (exact age, an age band such as "65-74", or a life-stage clue such as "post-menopause", "retired", "grandkids"), or write "age unknown". Never guess an age.
4. Separate what customers SAY from your own interpretation. Label interpretation "Analyst note:".
5. If the sources don't contain something, say "Not found in sources". Do not fill gaps.
6. No health claims, no hair-regrowth claims. We only care about the experience of APPLYING products to the scalp.
Use tables when asked. Keep answers dense; no filler.
```

Set the response length to **Longer**.

---

## STEP 3: Run these 5 prompts, one at a time

Copy each answer into a Google Doc as you go. NotebookLM chat history isn't permanent, and you can also click "Save to note".

### Prompt 1: Verify Gemini's quotes
```
Check whether each of these quotes appears in the sources, word for word. For each give: the quote, FOUND EXACT / FOUND DIFFERENT (show the real wording) / NOT FOUND, which source it is in, and any age signal from that same comment.
1. "When I put it on it feels a bit sticky and in the morning when I wake up my hair is really greasy"
2. "minox is my last hope and having greasy hair all the time just messed up everything for me"
3. "my hair is never really free of product"
4. "it became such a chore to add the minoxidil to a small cap, dip the brush, apply the solution, wash the brush"
5. "having it drip down my scalp and sometimes on my face, plus getting it on my hands, was a bigger chore"
6. "I have to wash my hair everyday (before minox it was every 2 days)"
7. "it took an hour, an actual 60 mins to cover all my head"
8. "it would totally melt because of the heat from my hand holding it"
9. "I take the dropper and slide it along the scalp between the hair"
10. "Do you find the Q-tip soaks up most of it and wastes some?"
11. "makes the crown of my head greasy"
12. "I will be 50 in June i quit all treatment cause i got tired"
13. "I can't even make a fist anymore or open a water bottle"
14. "awful not being able to even grip things properly"
Output as a table.
```

### Prompt 2: The messy application pain (main avatar)
```
Find every customer quote in the sources about the experience of APPLYING a product to the scalp (minoxidil/Rogaine liquid or foam, hair oil, rosemary oil, castor oil, scalp serum) where the person describes any of these pains:
MESS-ON-HAIR (product on the hair not the scalp) / GREASY (dirty, sticky, greasy-looking hair) / OVERWASH (washing more because of it) / DRIPS (onto face, forehead, neck, eyes) / PILLOW-TOWEL (on bedding, towels, clothes) / TIME (tedious, long, twice a day) / SKIP-QUIT (forgetting, skipping, cutting to once a day, quitting because of the routine) / WORKAROUND (toothbrush, Q-tip, makeup brush, cotton ball, applicator bottle, someone else applying it).
Make a table with columns: Quote (verbatim) | Source | Age signal | Product | Pain type(s) | Workaround named | Emotion words.
List women with an age signal of 50+ FIRST, then everyone else. Aim for at least 40 rows if the sources contain them. After the table, count quotes per pain type, split into "age 50+" and "age unknown or under 50".
```

### Prompt 3: Hands and grip (supporting angle)
```
Find every customer quote in the sources where someone describes difficulty with their HANDS (arthritis, stiffness, pain, weak grip, tremor, numbness) when using droppers, squeeze bottles, foam cans, pumps, applicators or any hair, scalp or small-bottle product. Also include quotes about not being able to SEE the scalp or REACH the back of the head.
Table: Quote (verbatim) | Source | Age signal | What product or task | Specific difficulty | Workaround.
Then say clearly: how many of these quotes are specifically about HAIR or SCALP products versus other products (eye drops, jars, bottles)?
```

### Prompt 4: Evidence against
```
Find quotes that CONTRADICT these two ideas:
(1) "Applying scalp products is messy and tedious enough that people skip or quit", for example people who say application is easy, quick, not messy, or that they found a simple method that works.
(2) "Hand problems make scalp product applicators hard to use", for example older people who say droppers or foam are easy for them.
Table: Quote (verbatim) | Source | Age signal | Which idea it contradicts | Their method.
Analyst note: what does this mean for a product that claims to make application easier?
```

### Prompt 5: Final report
```
Using ONLY the quotes you found in the previous answers (with their citations), write a final report with these sections:
1. VERDICTS: Main avatar ("women 55+ find applying scalp products messy and tedious, and skip or quit") and Hands angle: STRONG / MEDIUM / WEAK each, with a one-line reason and the number of supporting quotes from people aged 50+.
2. WHO SHE IS: age, what she applies, how often, built only from quotes.
3. TOP 5 PAINS, ranked by how often and how intensely they appear, each with 3 verbatim quotes and their age signals.
4. WHAT SHE'S TRIED AND WHY IT FAILED: each workaround tool, with quotes.
5. HER EXACT WORDS: 25 short verbatim phrases (under 15 words each) that could be used in first-person ad copy, each with its source.
6. OBJECTIONS: what would make her doubt a new applicator, with quotes.
7. TRIGGER MOMENTS: when she decides to look for a better way, with quotes.
8. GAPS: what the sources don't answer, and where to look next.
No market-size estimates. No ad hooks.
```

---

## STEP 4: Send it back here

Export the notes, or copy the 5 answers into one Google Doc and share it, or download it as PDF and upload it. I'll check a sample of the quotes against the PDFs, score the avatar, and write the ads from the strongest verified quotes.
