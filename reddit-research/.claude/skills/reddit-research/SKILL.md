---
name: reddit-research
description: Run ecommerce market research on Reddit with the reddit-research MCP tools. Find the threads where an avatar talks about a problem, map how those threads link together, and mine verbatim pains, failed solutions, objections, beliefs, triggers and buying language with links back to the source. Use when the user asks to research a product, niche, avatar, competitor or angle on Reddit, or to find customer language or failed solutions for copy.
---

# Reddit research playbook

The `reddit-research` MCP server gives you a local database of full Reddit threads, the links between them, and a
quote-verified insight store. Your job: run a study end to end and come back with evidence the user can write copy
from. Every quote you report must come from `insights_report` / `save_insights` (they reject paraphrases).

## 1. Frame the study
Ask (or infer from the user's files) for: product, avatar, and what they want to learn. Then:
`create_study(name, brief, keywords)`. The brief drives relevance scoring, so name the problem, the avatar and the
known products/solutions in plain words. Keywords: symptoms, product types, competitor brands, ingredients.

## 2. Find where the avatar talks
- `find_subreddits` for the avatar's life stage AND for the problem (e.g. r/beyondthebump + r/FemaleHairLoss).
- `discover_threads` with 4-8 queries written the way people talk ("hair falling out after baby", not
  "postpartum telogen effluvium"), across 3-6 subreddits. Use `time_range="year"` for current language, "all" for depth.

## 3. Build the web
- `crawl_web(study, max_threads=25)`; repeat until you have 100-300 threads or candidates run out. It follows links
  inside comments, crossposts and other submissions of the same link (max_hops=2 by default).
- `graph_overview(study)`: read the groups. Name each with `name_group` (e.g. "minoxidil dread", "oil mess").
  Hubs = threads everyone points to (read these first). Bridges = threads joining two groups (often new angles).
- If one group is thin but important, run `discover_threads` again with its key terms.

## 4. Mine (the main loop)
Repeat until `threads_left_to_analyze` is 0 or you have enough signal:
1. `next_threads_to_analyze(study, 3)`
2. `read_thread(id, mode="top")`. Use `mode="all"` with `offset` paging for threads that are dense with signal.
3. `save_insights(study, items, analyzed_thread_ids=[...])` with one item per distinct finding:
   - `kind`: pain, desire, failed_solution, objection, belief, trigger, brand, price, buying_intent, question,
     identity, language, angle, other
   - `label`: a SHORT normalized name reused across threads ("biotin", "shedding panic", "fear of dread shed")
     so the report can count how many different people said the same thing
   - `quote`: copied exactly (use `...` to skip words). `source_id`: the `c:<id>` / `p:<id>` tag
   - `note`: optional: sentiment for brands, sub-desire mapping, why it matters
4. If a save is rejected, re-copy the quote exactly from the thread text; never "fix" it into a paraphrase.

Use `search_corpus` to size a pattern across everything fetched (e.g. `"rosemary oil" messy`, `minoxidil NEAR(shed)`).

## 5. Report
- `insights_report(study, kind=...)` per kind. Support = distinct people, which matters more than upvotes.
- Deliver: failed-solutions ladder (in the order people try them), top pains/triggers, objections, beliefs to
  dismantle, competitor sentiment, a language bank of verbatim phrases, and 3-5 angle hypotheses, each with
  support counts and source links.
- `export_results(study, "md")` writes the full report; `"html"` writes the interactive thread-web map;
  `"insights_csv"` for spreadsheets.

## Rules
- Only report quotes that came back from the tools. If support is 1-2 people, say it's anecdotal.
- Treat usernames as private: never profile or single out individuals; talk about patterns.
- Check `status` first in a new session; studies persist between sessions.
