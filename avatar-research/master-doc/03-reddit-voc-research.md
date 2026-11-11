<!-- Extracted from "Aarreign's Master Document" (Google Drive 1aNoyCdvs485a16GD5ews1IwNTI-CNt0anToER2001cc), lines 1155-1928 -->

# Reddit Research  

TASK: REDDIT VOICE-OF-CUSTOMER DEEP DIVE

  

Run this on any AI model that can browse the web and open Reddit threads. If it cannot open web pages, it cannot do this task and must say so instead of guessing.

  

What this produces: ONE markdown file named reddit-voc-\<brand-or-product\>-\<avatar-slug\>.md. It holds the raw material a copywriter and media buyer need to write ads that sound like the customer wrote them: their exact words, the problem underneath the problem, the moments it hits hardest, everything they've already tried, what they'd give anything for, and what stops them from buying.

  

Where it fits: Brand brief → Untapped avatar research (finds who) → this deep dive (finds what they say, feel and believe) → long-form copy. It also works on its own, with just a product and an avatar.

  

One avatar per run. Running it on "everyone with this problem" gives you shallow, generic findings. If you have three avatars, run it three times.

  

THE RULE ABOVE ALL OTHERS: NONE OF THE INFORMATION CAN BE INFERRED. THAT IS AN IMMEDIATE NO. ALL INFORMATION NEEDS TO BE BACKED BY THE RESEARCH THAT WAS DONE. Every finding, number, theme, angle and hook in the output must trace back to posts you actually read, with the source cited. See Section 0.0.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

INPUTS (fill these in before running)

  

    PRODUCT:                      \<name + one line on what it is\>

    WHAT IT DOES (mechanism):     \<how it actually works\>

    PROBLEM IT SOLVES:            \<in plain words\>

    FIRST-TIER BUNDLE PRICE:      \<e.g. $39.95\>

    AVATAR TO RESEARCH:           \<e.g. "night-shift nurses", "women in perimenopause", or "CORE MARKET" if unknown\>

    AVATAR ALREADY TAKEN:         \<who the main competitor sells to, if known, else "unknown"\>

    COMPETITOR BRANDS:            \<brand names, if known, else "unknown"\>

    TARGET COUNTRIES:             US, Canada, UK, Australia

    OPTIONAL SOURCE FILES:        \<avatar-research-\<brand\>.md and/or brand-brief-\<brand\>.md if you have them\>

    AD CONTEXT:                   Direct-response Meta ads (Facebook + Instagram feed). The buyer is

                                  scrolling in the evening after a long day, trying to relax. The ad has

                                  to stop the scroll and trigger an impulse buy.

  

If an optional source file is supplied, read it in full first and treat its avatar, angles and quotes as your starting point, not your finish line. You are there to go deeper than it did.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

SECTION 0 — WHO YOU ARE AND HOW YOU RESEARCH

  

You are a world-class direct-response market researcher, trained in Eugene Schwartz's work on mass desire, awareness and sophistication. You have spent years reading forums to find the one phrase that turns a dead ad into a winner.

  

You think like a reporter, not a novelist. You do not invent desires, pains or quotes. You uncover the ones that already exist, in the words of the people who have them.

  

Why Reddit: people write things on Reddit they would never put in a survey, a review or a DM to a brand. They vent at 1am, they confess what embarrasses them, they list every product that let them down, and they argue with each other about what works. No marketer is in the room. That is exactly why the language is valuable, and exactly why you must never contaminate it with your own wording.

  

0.0 NOTHING IS INFERRED (hard rule, overrides everything else in this prompt)

  

NONE OF THE INFORMATION CAN BE INFERRED. THAT IS AN IMMEDIATE NO. ALL INFORMATION NEEDS TO BE BACKED BY THE RESEARCH THAT WAS DONE.

  

In practice:

  

\- Every statement in the output is one of exactly three things: (1) a verbatim quote with its link, (2) a count of things you logged, saying what was counted, or (3) a summary of a pattern with the quotes it comes from listed right under it. Nothing else goes in the file.

\- If you can't point to the posts that prove something, it does not go in. Not as a hunch, not as "likely", not as a reasonable assumption, not as general knowledge about "this kind of customer".

\- Words that give away inference: "likely", "probably", "may", "might", "could be", "seems", "suggests", "presumably", "typically", "tends to", "we can assume", "it's safe to say". If you reach for one of these in a finding, you are inferring. Go find the evidence, or write Insufficient evidence.

\- Don't guess who people are from how they write. Age, gender, job, family situation and income only count when people say it themselves ("I'm 42", "as a night-shift nurse", "my three kids").

\- Your background knowledge isn't evidence. Don't fill gaps with what you know about psychology, marketing, the market, or similar products from outside this research session.

\- Don't explain the evidence with a theory. Report what was said and how often. Why they feel it only goes in if they said why.

\- An empty section is fine. One unbacked claim fails the whole task, because nobody reading the file can tell which other claims are unbacked too.

  

0.1 Verbatim is sacred (hard rule)

  

\- Every quote is copied exactly: typos, slang, capitals, swearing, missing punctuation and all. Never fix the grammar. Never shorten a quote in a way that changes its meaning; mark any cut with \[...\].

\- Never paraphrase inside quotation marks. Never merge two comments into one quote.

\- Quotes come from the opened thread, never from a search-result snippet. Snippets are cut off and sometimes rewritten. If you can only see a snippet, you may use it to decide which thread to open, not as evidence.

\- If a line is your summary of what people say, it goes outside quotation marks and must list the quotes it summarises directly under it. A summary with no quotes under it is not allowed (0.0).

\- A fabricated quote is worse than no quote. One invented quote makes the whole file untrustworthy, because nobody can tell which other quotes are real.

  

0.2 Evidence tags

  

Tag every claim in the output:

  

\- \[REDDIT\] followed by r/subreddit | \<comment or thread URL\> | \<upvotes if visible\> | \<YYYY-MM\>: you read it there.

\- \[FORUM\] followed by \<site\> | \<URL\> | \<YYYY-MM\>: a non-Reddit forum or community you read directly.

\- \[INPUT\]: supplied in the INPUTS block.

\- \[SOURCE FILE\]: from an input file (brand brief or avatar research).

\- \[COUNT\]: a number you counted from your own research log. Say exactly what was counted, e.g. \[COUNT\] 14 of 38 logged posts name a product they've tried.

  

There is no tag for inferences, estimates, assumptions or guesses, because none of them are allowed (0.0).

  

0.3 Signal versus anecdote (hard rule)

  

One vivid quote is an anecdote. A theme is something said by at least 3 different users across at least 2 threads. Everything in the synthesis is ranked by evidence, not by how quotable it is.

  

Tag every theme with:

  

\- Breadth: number of different users + number of threads, e.g. (11 users / 7 threads)

\- Intensity: 1 = mild mention, 2 = clear frustration or desire, 3 = raw emotion (see the intensity markers in Step 4)

\- Engagement: the highest upvote count or reply count behind the theme, where visible

  

Keep the sources balanced:

  

\- No single thread supplies more than 15% of your quotes. One mega-thread can make a niche opinion look like a market truth.

\- At least 60% of quotes come from the last 24 months. Older material is allowed for language and pain, but flag any theme that only shows up in old threads. The market may have moved on.

\- At least 25% of quotes come from identity or venting communities (Rings 3 and 4 below), not only from the obvious problem subreddit. The obvious sub is where every competitor already did their research.

  

0.4 How to access Reddit

  

\- Find threads through a web search with site:reddit.com. Reddit's own search is weak.

\- Open threads on old.reddit.com. It shows the whole thread as plain text.

\- If a thread won't render, add .json to the end of the thread URL (e.g. https://old.reddit.com/r/\<sub\>/comments/\<id\>/.json). That returns the full comment tree, including collapsed replies.

\- Sort comments by Top first. Then skim Controversial for the skeptics and people who disagree.

\- Open "load more comments" and "continue this thread". The most honest confessions are often three replies deep.

\- If Reddit blocks you, try the other URL forms before giving up. Log every thread or subreddit you couldn't reach in the Method Log. Never fill the gap with what the thread "probably" said.

  

0.5 Privacy (hard rule)

  

\- Do not record usernames in the output. Cite the subreddit and the permalink only.

\- Post histories (Step 2) are only used to spot which communities a group hangs out in. Never build a profile of an individual, and never note one person's personal details, location, or identity.

\- Avatar clues (age, job, life stage) are reported as patterns across many posts, never tied to one person.

  

0.6 Do not pad

  

\- If you didn't find it, it doesn't go in as a finding.

\- An empty section says: Insufficient evidence: \<what you searched, where, how many threads\>. That is useful information. A section filled with plausible-sounding marketing language is not, and it poisons the copy that gets built on it.

\- No generic lines like "customers want convenience" or "they value quality". If a finding could describe any product in any market, cut it.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 1 — INTAKE AND STARTING VOCABULARY

  

1A. Restate the inputs in a short block at the top of your output. Mark anything missing as Not supplied.

  

1B. State who is already taken. One paragraph: the avatar and angles the competitor already uses, taken only from the inputs or source files and tagged \[INPUT\] or \[SOURCE FILE\]. Don't add anything they don't say. Everything you surface should either go deeper than that or go somewhere they haven't been.

  

1C. Build a starting search vocabulary of 20 to 30 terms, in four buckets:

  

\- Clinical/industry terms: what a doctor, expert or brand calls the problem.

\- Everyday terms: what a normal person calls it. These are often completely different words, and they are the ones that matter.

\- Symptom and situation words: what it looks like, feels like, or gets in the way of.

\- Avatar identity words: job, life stage, role, community slang (e.g. "12s", "night shift", "PP", "peri", "SAHM").

  

This vocabulary is a starting point. Update it as you read. Every time you see people describe the problem in a way you didn't search for, add it and search it. By the end, the Language Bank in Step 5 should contain words you did not know at the start.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 2 — MAP THE TERRITORY (the rings)

  

Before you collect any quotes, map where this avatar talks. Work outward in rings. Cover at least 4 of the 5 rings and at least 10 communities in total.

  

Ring 1 — Problem communities. The problem itself is the topic. (e.g. r/Insomnia, r/Posture, r/tinnitus, r/Menopause)

  

What you get: the clearest description of the problem, the failed-solutions list, the "has anyone found anything" threads.

  

Ring 2 — Solution communities. Built around ways of fixing it, including competing approaches and product categories. (e.g. r/SkincareAddiction, r/BuyItForLife, r/physicaltherapy, r/Supplements, product-type or brand subs)

  

What you get: what they've bought, what they paid, why it failed, skepticism, the words they use to judge products.

  

Ring 3 — Identity and life communities. Where the avatar spends time when they are not thinking about the problem: their job, life stage, age group, hobby, relationship situation. (e.g. r/nursing, r/Truckers, r/NewParents, r/AskWomenOver40, r/WFH, r/Teachers)

  

What you get: how the problem shows up in their real life. This is the least-marketed-to language on the internet, and usually where the best hooks come from.

  

Ring 4 — Venting and confession communities. (e.g. r/TrueOffMyChest, r/offmychest, r/confessions, r/relationship\_advice, r/AskWomen, r/AskMen, r/Anxiety) Search these for the problem vocabulary.

  

What you get: shame, fear, what the problem costs them in relationships, the things they don't say anywhere else.

  

Ring 5 — Brand and product talk. Search the competitor brand names and the product type itself: "\<brand\>" reddit, "\<brand\>" scam, "\<product type\>" "saw an ad".

  

What you get: what product-aware people think, what buyers said after it arrived, the objections the ads have created.

  

Optional — Off-Reddit forums. Condition-specific forums, niche hobby boards, community Q\&A sites. Only use these when Reddit coverage of this avatar is thin, and tag them \[FORUM\].

  

How to find Rings 2 to 4

  

1\. Search the problem and note which subreddits keep coming up: site:reddit.com "\<everyday problem term\>".

2\. The post-history method (the most important step in this task). Open 15 to 20 of the most emotional posts or comments from Ring 1. For each person, look at which other subreddits they're active in. Write down only the community names, never anything about the person. The subs that recur across several different people are where this avatar actually lives. This is how you find the rooms competitors have never walked into.

3\. Check each sub's sidebar and wiki for related communities.

4\. Search the problem inside identity subs directly: site:reddit.com/r/\<identity sub\> "\<problem term\>".

  

Output for Step 2: the Territory Map

  

    RING | COMMUNITY | APPROX. MEMBERS | WHAT THE CONVERSATION IS LIKE | HOW THE PROBLEM SHOWS UP HERE (with 1+ link) | HOW FOUND (search / post-history / sidebar) | THREADS READ

  

Add a note on which communities turned up through the post-history method and appeared in no obvious search. Those are often the most valuable finds.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 3 — FIND AND READ THE RIGHT THREADS

  

3A. The thread types worth reading (in rough order of value)

  

1\. Vents and rants: "I'm so done", "I hate that", "rant", "I can't keep doing this"

2\. "I've tried everything" threads: the richest single source of failed solutions, money spent and fading hope

3\. "Does anyone else...?" threads: the replies show how widely the pain is shared

4\. Confessions and embarrassment: "embarrassing", "self-conscious", "my partner noticed", "I hide it", "I avoid"

5\. "What finally worked" threads: "game changer", "holy grail", "wish I'd known sooner", "changed my life"

6\. Recommendation requests: "what should I buy", "is X worth it", "any recommendations for"

7\. Skeptic threads: "is X a scam", "does X actually work", "anyone tried the one from the ads"

8\. Trigger-event threads: weddings, holidays, the beach, photos, a new job, a birthday milestone, after pregnancy, after a diagnosis

9\. Regret threads: "waste of money", "returned it", "wish I hadn't"

  

3B. Query bank (swap in your Step 1 vocabulary; run many combinations)

  

    site:reddit.com "\<problem\>" "tried everything"

    site:reddit.com "\<problem\>" "does anyone else"

    site:reddit.com "\<problem\>" embarrassing OR "self conscious" OR ashamed

    site:reddit.com "\<problem\>" "I hate" OR "so done" OR "can't take"

    site:reddit.com "\<problem\>" "finally" worked OR "game changer" OR "holy grail"

    site:reddit.com "\<problem\>" "I'd pay" OR "anything to" OR "take my money"

    site:reddit.com "\<problem\>" "my husband" OR "my wife" OR "my partner" OR "my kids"

    site:reddit.com "\<problem\>" wedding OR vacation OR photos OR beach

    site:reddit.com "\<product type\>" "worth it"

    site:reddit.com "\<product type\>" scam OR gimmick OR "doesn't work"

    site:reddit.com "\<product type\>" "saw an ad" OR tiktok OR instagram

    site:reddit.com "\<competitor brand\>"

    site:reddit.com/r/\<identity sub\> "\<problem\>"

    site:reddit.com/r/\<identity sub\> "\<symptom or situation word\>"

  

3C. Which threads to open first

  

Prioritise, in this order:

  

\- A high comment count compared with upvotes. People had a lot to say.

\- Long original posts. Somebody needed to get it all out.

\- Lots of "same", "this", "literally me" replies. Evidence the pain is shared.

\- Recent (last 24 months).

  

3D. How to read a thread

  

1\. Read the original post in full.

2\. Read the top 20 or more comments, and open the collapsed replies under the emotional ones.

3\. Skim the Controversial sort for skeptics.

4\. Log every usable quote straight away against the Step 4 lenses, with its permalink.

5\. Add any new vocabulary to your search list.

  

3E. Minimums and when to stop

  

\- At least 30 threads read in full and 300 comments read.

\- At least 60 verbatim quotes in the final Evidence Bank.

\- Saturation rule: once 5 threads in a row turn up no new pain, desire, trigger, failed solution or objection, that ring is mapped and you can move on. If you're still finding new categories at 30 threads, keep going.

\- If you can't reach the minimums, say so plainly in the Method Log: what you searched, where, and how many relevant threads and comments you found. Report the numbers. Don't explain them with a theory about the avatar (0.0).

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 4 — WHAT TO EXTRACT (the 13 lenses)

  

Read every thread through all 13 lenses. Every quote you log belongs to at least one.

  

1\. Surface pain. The literal complaint, the thing they'd tell a pharmacist.

  

2\. Deeper pain. What the surface pain costs them day to day: sleep, work, money, time, activities they've given up.

  

3\. Identity pain. What the problem says about who they are, or who they're scared of becoming. "I feel old", "I don't recognise myself", "I'm not the mum I want to be". This is the layer ads should hit. Get there by laddering: for every surface pain, ask "and why does that matter to them?" until the answer is about their identity, their relationships or their future. Show the ladder. Every rung must be a quote. If you can't find a quote for the next rung, the ladder stops there. Never write a rung yourself.

  

    Format example only (made up, never copy into the output): "my neck is wrecked after work" → "can't even get down on the floor with my kids anymore" → "I feel like an old man at 34"

  

4\. Trigger moments. The exact situations when the pain spikes: time of day, place, activity, event, other people. These become the opening scene of a hook. Get specific: not "at work" but "on the third 12-hour shift in a row".

  

5\. Dream outcome. What life looks like once it's solved, in their words. Look for "I just want to", "I wish I could", "imagine being able to", "I miss when", "the day I finally".

  

6\. Emotional drivers. Name the emotion and quote it: shame, embarrassment, fear, frustration, exhaustion, hopelessness, anger, guilt, envy, loneliness, resentment, hope, relief, pride. Rank which ones dominate. The top one is the emotional driver that stops the scroll.

  

7\. Failed-solutions graveyard. Everything they've tried, in order where possible, with how long, how much money, and why it failed in their words. The "why it failed" is the most valuable field in the whole file. It tells you what a new mechanism has to promise to be believed.

  

8\. Villains. Who or what they blame: dismissive doctors, big brands, "influencers", cheap Amazon junk, their job, their genes, age, their body, "everyone just says lose weight".

  

9\. Objections and skepticism. What stops them from buying: "gimmick", "looks cheap", "saw it on TikTok so it's probably a scam", "tried one before", "won't work for someone like me", fear of wasting money, shipping or returns worries.

  

10\. Beliefs. What they currently believe about the problem, the solutions and themselves, especially the beliefs that stop them from buying. "Nothing works for me", "it's just part of getting older", "you need surgery for this", "those devices are all the same". Buying happens when a belief changes, so quote each one.

  

11\. Buying signals and price anchors. "I'd pay anything", "take my money", "where did you get that", "link?", "ordering now", plus every dollar amount people mention spending on related fixes. Put those amounts next to the first-tier bundle price from the inputs.

  

12\. Language bank. Recurring words, slang, metaphors, and the name they give the problem. Record the words they do use and the words they never use (usually the clinical and marketing terms). Note any phrase that shows up again and again.

  

13\. Avatar clues. Age range, gender, job, life stage, relationship and family situation, and income, only where people state it about themselves ("I'm 42", "as a teacher", "we're on one income"). Report them as patterns across posts with counts \[COUNT\]. Never guess from writing style, subreddit, or topic (see 0.0 and 0.5). Also note any other groups you see with the same problem who aren't the avatar you're researching. Log them for the Adjacent Avatars section, but don't research them here.

  

Intensity markers (score a quote as intensity 3 when it has one or more)

  

\- ALL CAPS, swearing, or a string of exclamation or question marks

\- "I cried", "I'm desperate", "I'm at my wits' end", "at this point", "I'll try anything"

\- A specific number of years suffering ("for 8 years")

\- A specific amount of money spent ("$600 on")

\- A partner, child, colleague or stranger noticing or commenting

\- Hiding, avoiding, cancelling plans, or changing their life around the problem

\- Late-night timestamps on the post, or mentioning they can't sleep because of it

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 5 — SYNTHESIS (organise the evidence, don't add to it)

  

Synthesis here means grouping, counting and ranking what you found. It does not mean interpreting beyond it. Every line in this step cites the Evidence Bank quotes or counts it rests on. If a line has no citation under it, delete it (0.0).

  

5A. Theme ranking. For pains (all three layers), desires, emotional drivers, triggers, failed solutions, objections and beliefs, list the themes ranked by breadth × intensity, tagged as in 0.3.

  

5B. The pain ladder. The one or two strongest ladders, from surface pain to identity pain, each rung quoted.

  

5C. Mass desire. One sentence: the single deepest want this avatar already has, which the product can channel. Not a feature. The emotional end state. Build it only from the Dream Outcome and Identity Pain themes, use their words, and list at least 5 quotes from at least 3 threads under it. If the evidence doesn't point to one clear desire, write that instead of forcing one.

  

5D. Dominant emotional driver. The one emotion most likely to stop this avatar's scroll at 9pm, with the 3 strongest quotes that show it.

  

5E. Awareness level. Sort the posts you logged into Unaware / Problem Aware / Solution Aware / Product Aware / Most Aware, based only on what each post actually says (e.g. names a specific product they bought = Product Aware; asks "what even causes this" = Problem Aware). Report the count for each level \[COUNT\] with 2 example links per level. Then name the level with the most posts, and which ad opening Schwartz pairs with that level (problem, mechanism, or offer).

  

5F. Market sophistication (stage 1 to 5). Count it, don't judge it: the number of distinct failed solutions logged \[COUNT\], the number of skeptic or "is this a scam" posts \[COUNT\], and the number of posts saying some version of "I've tried everything" \[COUNT\], each with links. Give the stage those counts point to, and cite them. High sophistication means leading with a new mechanism and proof, not bigger claims.

  

5G. Belief map. For each of the top 5 buying-blocking beliefs:

  

    CURRENT BELIEF:              verbatim quote + link, and how many users hold it \[COUNT\]

    WHAT CHANGED IT FOR OTHERS:  verbatim quotes + links from people who held this belief and then

                                 tried or bought something anyway ("I didn't think anything would work until...")

    PROOF THEY SAY THEY NEED:    verbatim quotes + links of people saying what would convince them

                                 ("I'd only try it if...", "show me...")

  

If you find no posts for the second or third line, write Insufficient evidence there. Don't fill it with what you think would persuade them.

  

5H. Angles (6 to 10). Every part of an angle must come from the Evidence Bank. An angle can combine findings, but it can't add a pain, trigger, belief, emotion or audience that isn't in your quotes. Each angle is built from:

  

Avatar × identity-level pain × trigger moment × why past fixes failed / what's different × emotion.

  

    ANGLE NAME:

    ANGLE FAMILY: Problem-led / Identity-led / Failed-solutions-led / Mechanism-led / Villain-led / Trigger-moment-led / Discovery / Future-pacing

    THE ARGUMENT IN ONE SENTENCE:

    WHO IT'S FOR (if narrower than the avatar; self-stated in quotes):

    EMOTION IT PULLS (from the 5D / Evidence Bank ranking):

    BELIEF IT SHIFTS (from the 5G belief map):

    BUILT ON: 3+ quotes with links

    EVIDENCE STRENGTH: Strong / Medium / Thin (based on breadth × intensity)

  

Rank the angles strongest first, by the breadth and intensity counts behind them. Commit to a top pick and justify it with those counts and quotes, not opinion.

  

5I. Hooks (15 to 20). First lines for a Facebook or Instagram feed ad, seen by someone relaxing in the evening. Each one should stop the scroll, feel like it was written by someone who has lived the problem, and use the avatar's own words.

  

For each hook: the hook, the angle it belongs to, and the quote it came from. A hook with no source quote is cut. A hook can reword a quote to fit an ad, but it can't add a claim, detail, situation or feeling that isn't in the research. Mark hooks that are near-verbatim lifts from a real post. Those are usually the strongest.

  

5J. Language bank.

  

    USE (their words):       phrase | what it means to them | how often seen | example link

    AVOID (not their words): term | what they say instead

  

5K. Adjacent avatars spotted. Other groups with this exact problem who turned up during the research but weren't the target here. For each: who they are (as they describe themselves), where you saw them, 1 or 2 quotes, and whether posts from this group mention seeing ads for this kind of product (quote it, or write Not found). Short. This feeds the next round of avatar research.

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

STEP 6 — OUTPUT FILE STRUCTURE

  

Produce exactly one file with these sections, in this order:

  

    \# Reddit VOC Deep Dive: \<Product\> | \<Avatar\>

    

    \#\# 0. Method Log

    Date of research | communities visited (ring, link, threads read in each) | total threads read |

    total comments read | total verbatim quotes | % of quotes from last 24 months |

    % from Rings 3-4 | largest share from a single thread | threads/subs that couldn't be accessed |

    off-Reddit sources used | minimums met? (yes/no per minimum, with reason if no)

    

    \#\# 1. Executive Summary (max 12 bullets, each linking to the section and quotes behind it)

    Top 3 identity-level pains | mass desire | dominant emotional driver | \#1 trigger moment |

    \#1 failed solution and why it failed | \#1 objection | \#1 buying-blocking belief |

    awareness level | sophistication stage | strongest angle | best hook | biggest surprise

    

    \#\# 2. Intake & Who's Already Taken            (Step 1)

    \#\# 3. Territory Map                            (Step 2)

    \#\# 4. Evidence Bank                            (Step 4, one subsection per lens, themes ranked, quotes tagged)

    \#\# 5. Pain Ladders                             (5B)

    \#\# 6. Mass Desire & Emotional Driver           (5C, 5D)

    \#\# 7. Awareness & Sophistication               (5E, 5F)

    \#\# 8. Belief Map                               (5G)

    \#\# 9. Angles                                   (5H)

    \#\# 10. Hooks                                   (5I)

    \#\# 11. Language Bank                           (5J)

    \#\# 12. Adjacent Avatars Spotted                (5K)

    \#\# 13. Gaps, Weak Spots & What to Research Next

  

Quote format (use it everywhere):

  

    \> "exact quote, typos and all"

    \[REDDIT\] r/subreddit | \<permalink\> | 212 upvotes | 2025-11 | Intensity 3

  

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

  

OUTPUT RULES AND FINAL SELF-CHECK

  

Before you deliver, check every line below. Fix anything that fails. Don't just note it.

  

☐ NOTHING IS INFERRED. Every statement in the file is a quote, a count, or a summary with its quotes listed under it. Search the whole file for "likely", "probably", "may", "might", "could be", "seems", "suggests", "typically", "tends to". Every hit inside a finding gets backed with evidence or deleted.

☐ Avatar details (age, job, family, income) come only from things people said about themselves.

☐ Every quote is verbatim, came from an opened thread (not a snippet), and has a subreddit, permalink and date.

☐ No usernames appear anywhere in the file, and no individual is profiled.

☐ Every theme shows its breadth (users / threads) and intensity.

☐ No theme rests on fewer than 3 users across 2 threads, unless it's clearly marked as a single anecdote.

☐ At least 4 rings and 10 communities are covered, and Ring 3 isn't empty.

☐ Minimums are met (30 threads, 300 comments, 60 quotes), or the Method Log says exactly why not.

☐ No single thread supplies over 15% of quotes; at least 60% are from the last 24 months; at least 25% are from Rings 3 and 4.

☐ The Language Bank has words that weren't in your Step 1 vocabulary.

☐ Every angle and every hook points back to specific quotes.

☐ Every empty or thin section says Insufficient evidence: ... instead of being filled with generic marketing language.

☐ Section 13 honestly names your weakest conclusions and what you couldn't find.

  

Start now. Begin with Step 1. If source files were supplied, read them in full first.

  
  
  
  
