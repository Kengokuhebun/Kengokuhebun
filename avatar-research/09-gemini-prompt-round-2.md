# Gemini prompt, round 2: verify and finish the research

Use **Gemini Deep Research**. Paste each part as its own message, in order, in the same chat. Splitting it into 3 smaller jobs fixes the main problem with round 1, which ran out of room after 13 quotes.

---

## Part 1: verify round 1 (paste first)

```
You are a meticulous research verifier. In a previous answer you gave me quotes from the Reddit threads below. I need each quote checked against the live page. Accuracy matters more than volume.

For EACH thread below:
1. Open the thread and read the post and ALL comments, including collapsed ones and "more replies".
2. Find each quote I list for that thread. Copy it again EXACTLY as written on the page, including typos.
3. Give the COMMENT PERMALINK, the specific comment's URL, not the thread URL. On Reddit it looks like /r/SUB/comments/POSTID/comment/COMMENTID/.
4. Give: username, date (month and year), upvotes, and any age or life-stage clue anywhere in that user's comment ("I'm 58", "post-menopause", "grandkids"). If none, write "none".
5. Mark each quote: VERIFIED (exact words found), CHANGED (found but the wording differs; show the real wording), or NOT FOUND.
6. Then list any OTHER comments in the same thread about the APPLICATION being messy, greasy, dripping, time-consuming, getting on the hair or face, needing a workaround tool, skipping or quitting, or about hand or grip problems. Give each one as a verbatim quote with its comment permalink, date, upvotes and age clue.

Threads and the quotes to check:
- https://www.reddit.com/r/FemaleHairLoss/comments/vmk4gd/ : "When I put it on it feels a bit sticky and in the morning when I wake up my hair is really greasy" ; "minox is my last hope and having greasy hair all the time just messed up everything for me"
- https://www.reddit.com/r/FemaleHairLoss/comments/1xom6dv/ : "I have this thing when my hair gets dirty , it gives me a headache" ; "But now my hair is never really free of product."
- https://www.reddit.com/r/FemaleHairLoss/comments/1ssgb4z/ : "it became such a chore to add the minoxidil to a small cap, dip the brush, apply the solution, wash the brush" ; "having it drip down my scalp and sometimes on my face, plus getting it on my hands, was a bigger chore"
- https://www.reddit.com/r/FemaleHairLoss/comments/1c468jg/ : "I have to wash my hair everyday (before minox it was every 2 days)"
- https://www.reddit.com/r/FemaleHairLoss/comments/1ff90rt/ : "it took an hour, an actual 60 mins to cover all my head" ; "it would totally melt because of the heat from my hand holding it" ; "I take the dropper and slide it along the scalp between the hair"
- https://www.reddit.com/r/FemaleHairLoss/comments/qpzq7w/ : "Do you find the Q-tip soaks up most of it and wastes some?"
- https://www.reddit.com/r/Menopause/comments/1j27h5j/ : "makes the crown of my head greasy"
- https://www.reddit.com/r/tressless/comments/u1wi2k/ : "I will be 50 in June i quit all treatment cause i got tired" ; "left a nasty texture to my hair" ; "dries the fuck outta my scalp and hair while making my hair look greasy"
- https://www.reddit.com/r/Menopause/comments/1svsmmv/ : "I can't even make a fist anymore or open a water bottle"
- https://www.reddit.com/r/Menopause/comments/zo9p67/ : "awful not being able to even grip things properly"

Output: one table with columns: Thread | Quote (verbatim) | Status | Comment permalink | Username | Date | Upvotes | Age clue | Notes.
Then a second table for the NEW quotes found in step 6, same columns.
If you cannot open a page, write "COULD NOT OPEN" for that thread. Do not guess.
```

---

## Part 2: go deeper on Reddit, older women only (paste after Part 1 is done)

```
Same rules as before: verbatim quotes only, a comment permalink for every quote, never invent or merge quotes, and say plainly when you find nothing.

TASK: Find Reddit comments from women who are CLEARLY aged 50 or over (they state their age, say post-menopause, mention grandchildren or retirement, or post in an over-50 or over-60 subreddit) talking about APPLYING something to their scalp: hair oil, rosemary oil, castor oil, minoxidil or Rogaine (liquid or foam), or scalp serums.

What I want them to be talking about:
- mess (on the hair, hands, face, neck, pillow, towel)
- greasy or dirty-looking hair, washing more often
- time and tedium, twice-a-day routines
- forgetting, skipping, cutting back to once a day, quitting because of the routine
- home-made application tools (toothbrush, Q-tip, makeup brush, cotton ball, applicator bottle, someone else applying it)
- difficulty seeing the scalp, reaching the back of the head, or using droppers or foam with stiff, painful or shaky hands

Start with these threads (read every comment):
- r/FemaleHairLoss "Minoxidil is annoying to apply": https://www.reddit.com/r/FemaleHairLoss/comments/1m5117d/
- r/FemaleHairLoss "Anyone else find minoxidil application annoying/messy?" (search for it)
- r/AskWomenOver50 "Does anyone have a super itchy scalp?": https://www.reddit.com/r/AskWomenOver50/comments/1rl2dyz/
- r/AskWomenOver50 "How is your scalp feeling after turning 55?": https://www.reddit.com/r/AskWomenOver50/comments/1l164bf/

Then search these subreddits with the terms: rogaine, minoxidil, hair oil, scalp oil, rosemary oil, castor oil, dropper, foam, greasy, applicator:
r/AskWomenOver50, r/AskWomenOver60, r/AskWomenOver40, r/Menopause, r/Perimenopause, r/FemaleHairLoss (posts where the author states age 50+), r/GreyHair, r/SilverHair, r/finehair, r/AskOldPeople, r/Arthritis, r/rheumatoid, r/osteoarthritis, r/EssentialTremor.

Target: 40 verbatim quotes from women 50+ (stop at 40). No more than 6 quotes from any one thread.

Output, one table: Quote (verbatim) | Comment permalink | Subreddit | Age clue (exact words) | Date | Upvotes | Product | Pain type (MESS-HAIR / GREASY / DRIPS / PILLOW-TOWEL / TIME / SKIP-QUIT / WORKAROUND / HANDS / SEE-REACH) | Workaround named.
Then: a count of quotes per pain type, and a list of the 10 most useful threads with links and comment counts.
Then: "Searches with no results", listing the subreddits and terms that found nothing.
```

---

## Part 3: reviews outside Reddit (paste after Part 2 is done)

```
Same rules: verbatim only, a direct link to the review or the product's review page plus the reviewer name and date, no invented numbers, and say plainly what you couldn't access.

TASK: Find product reviews by people aged 50+ (or with a stated age, "my mother", "senior", "arthritis", "grandma") about APPLYING scalp products.

Sources, in this order:
1. Drugs.com reviews for minoxidil topical (shows age in some reviews): filter or scan for women and older reviewers.
2. Amazon: Women's Rogaine 5% Foam; Women's Rogaine 2% Solution; Kirkland Minoxidil for women; scalp oil applicator bottles; "scalp applicator" comb bottles; roller-ball scalp applicators; minoxidil applicator. Read the 1–3-star and "most helpful" reviews. Look for: messy, greasy, drip, dropper, hands, arthritis, grip, squeeze, waste, forehead, pillow, sticky, "I'm 6", "I'm 7", senior.
3. Walmart, Target, Ulta and Costco reviews of the same products.
4. The Kitsch Scalp Oil Applicator review page (mykitsch.com): reviews that mention age, arthritis, hands or "easy to use".
5. Forums: Mumsnet (search "rogaine", "minoxidil", "hair oil"), HealthUnlocked arthritis communities, AgingCare.

Target: 30 verbatim reviews (stop at 30), at least 10 with an age or senior clue and at least 5 about hands or grip with hair or scalp products.

Output, one table: Review (verbatim) | Link | Site and product | Reviewer name and date | Star rating | Age clue | Pain type | Workaround or tool mentioned.
Then: for each applicator product you found (name, price, star rating, number of reviews, link), give its top praise and top complaint in reviewers' own words.
Then: "Could not access", listing the sites that blocked you.
Do NOT estimate market sizes. Do NOT write ad hooks.
```

---

## When it's done
Send me all 3 outputs as text or PDF. I'll:
1. merge them with `06` and `08`,
2. score the avatar,
3. write ads from the verified quotes.
