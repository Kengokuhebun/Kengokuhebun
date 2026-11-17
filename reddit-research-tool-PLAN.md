# Reddit Research Engine: Build Plan

A tool Claude can use to find, crawl, connect and mine hundreds to thousands of Reddit threads for ecommerce research. It covers avatar language, failed solutions, objections, competitors and sub-desires, and every insight links back to a verbatim quote.

Reference product: redditcommentscraper.com. Teardown tool: REA (github.com/morluto/rea).

---

## 0. What I found before planning

| Check | Result | What it means for the design |
|---|---|---|
| **REA's job** | REA is an MCP server for reverse engineering. For this project, three of its features apply: `analyze-javascript-application` (static analysis of an unpacked extension), `inspect-web-network-capture` (reads HAR files and derives the API surface) and `observe-web-session` / `inspect-web-page` (live observation in Chrome over CDP). | It's the right tool for working out *how* the reference product gets its data. It doesn't scrape anything itself. |
| **Reference product** | A Chrome extension plus a web exporter. One thread per run. Fields: `type, author, score, created_utc, depth, text, permalink`. Free tier stops at 20 comments; Pro stops at 1,000 per scrape. It has no filters and no cross-thread linking; "Reddit Radar" is only on the paid Adlicio plans. Its AI analysis (hooks, failed solutions, objections, customer language) is what you already do by hand in `longform-copy-all-15.md`. | The bar is low. The real gaps are **bulk + full comment trees + thread web + evidence-backed extraction**. |
| **How it gets data** | The extension "reads the thread in your browser". It's almost certainly Reddit's public `.json` endpoints, called from your own logged-in browser on a home IP. | It works because it runs on a **residential IP**. |
| **reddit.com from this cloud box** | `403` (blocked) | The fetcher must run on **your machine**, or use a fallback source. |
| **Arctic Shift archive** | Comment-tree endpoint returned `200` with full comment objects. Full-text search timed out ("slow down"). | Good fallback for **historical threads and full trees**, with careful rate limits. Not suitable for heavy search. |
| **PullPush archive** | `429`, and it no longer serves free agent scraping. | Leave it out. |
| **Apify** | Already connected to your account. | A paid fallback for bulk fetching when Reddit blocks the IP. |

A note on terms: Reddit's User Agreement and Data API terms restrict automated collection and commercial use. For research for your own brand, the safest default is the **official OAuth API** with your own Reddit "script" app, kept within its rate limits (about 100 requests/min). Public `.json` endpoints and archives are fallbacks. Don't resell the data or republish it in bulk. Treat usernames as pseudonymous and never build profiles of individual people.

---

## 1. Phase 0: Reverse-engineer the reference with REA (half a day)

The goal is parity knowledge, not copying code. Expect REA to confirm something simple ("it calls `/comments/{id}.json` and flattens the tree"). The value is in the edge cases: what it does with `more` stubs, how it handles depth past 2, its rate limiting, and where the 20 and 1,000 caps are applied.

1. **Get the extension.** Install it in Chrome, then copy the unpacked folder from `chrome://extensions` (Developer mode shows the path). Put it in a new, empty folder.
2. **Static teardown:**
   ```bash
   npx -y rea-agents@latest analyze-javascript-application /abs/path/extension-unpacked --json > teardown/static.json
   ```
   Look for fetch URLs, `manifest.json` host permissions, the tree-walk function, and the "more comments" handling.
3. **Runtime capture.** Start Chrome with `--remote-debugging-port=9222`, open a big thread, and click Scrape. Then run:
   ```bash
   rea observe-web-session http://127.0.0.1:9222 TARGET_ID --json
   ```
   Also export a HAR from DevTools and run:
   ```bash
   rea inspect-web-network-capture /abs/session.har har --json
   ```
4. **Reconcile.** Run `rea compare-static-and-observed-endpoints` to see which endpoints the code *can* call against the ones it actually *did* call.
5. **Optional.** `rea environment-build session.har ./fixtures-env` turns the recording into an offline replay. Use it as a test fixture so the scraper's tests don't hit Reddit.

**Deliverable:** `teardown/FINDINGS.md`, a parity checklist covering endpoints, fields, tree flattening, caps, and anything clever.

---

## 2. Architecture

```
            ┌──────────────── Claude (Code / Desktop) ────────────────┐
            │   Skill: "ecom-reddit-research" playbook (how to run a  │
            │   study: seed → crawl → web → extract → synthesize)     │
            └───────────────┬─────────────────────────────────────────┘
                            │ MCP tools (small, paged, summary-first)
┌───────────────────────────▼──────────────────────────────────────────┐
│ reddit-research MCP server (runs on YOUR machine: residential IP)    │
│                                                                      │
│  Sources (pluggable)   Crawler/Web builder   Store         Analysis  │
│  ─ Reddit OAuth API    ─ seed discovery      SQLite+FTS5   ─ filter  │
│  ─ public .json        ─ best-first frontier sqlite-vec    ─ extract │
│  ─ Arctic Shift        ─ edge detection      graph tables  ─ verify  │
│  ─ Apify (paid)        ─ budget/hop limits                 ─ cluster │
└──────────────────────────────────────────────────────────────────────┘
```

**Stack:** Python 3.12, `mcp` (FastMCP), `httpx` with a token-bucket rate limiter, SQLite (FTS5 + `sqlite-vec`), `networkx` + Leiden/Louvain for communities, local embeddings with `fastembed` (bge-small, free and offline), and the `anthropic` SDK for extraction. One `pip install`, one SQLite file per project, no servers to run.

### 2.1 Fetch layer (better than the reference)
- **Full comment trees.** Expand every `more` stub with `/api/morechildren` (100 IDs per call) and follow every `continue this thread` link. There's no artificial cap. Record `coverage = fetched / num_comments` per thread so Claude knows when data is partial.
- **Source fallback chain:** OAuth API → public `.json` → Arctic Shift → Apify. Each record stores which source it came from.
- **Polite, resumable crawling.** Per-host token buckets, `Retry-After` handling, ETag caching, and a job queue in SQLite so a crawl of 2,000 threads can stop and resume.
- **Incremental refresh.** Re-fetch only threads that have new comments.

### 2.2 Data model
- `posts(id, sub, title, selftext, author, score, upvote_ratio, num_comments, created, url, domain, flair, crosspost_parent, coverage, source, fetched_at)`
- `comments(id, post_id, parent_id, path, depth, author, score, body, created, edited, is_op, controversiality)`. `path` is a materialized path, so subtrees are a single query.
- `edges(src, dst, type, weight, evidence)`, where `src` and `dst` are threads or comments.
- `extractions(id, comment_id|post_id, kind, label, quote, quote_verified, sentiment, intensity, schema_ver)`
- `projects(id, brief, seeds, budget)`, `project_threads(project_id, post_id, relevance, hop, via_edge)`
- FTS5 index over titles, bodies and comments, plus a vector index over chunked thread summaries and high-signal comments.

---

## 3. The "interlinked web": how threads connect

Discovery starts from **seeds** (keywords, subreddits, thread URLs, a competitor's domain). The crawler then expands **best-first**: every candidate thread gets a score, and the highest-scoring ones are fetched until the budget runs out.

### Edge types (each stored with evidence)
| Edge | How it's detected | Why it matters for ecommerce |
|---|---|---|
| **Explicit link** | Reddit permalinks, `redd.it` and `/r/x/comments/id` links inside posts and comments | Users point each other to the "real" discussion. These are the strongest edges. |
| **Crosspost** | `crosspost_parent_list` | The same pain point showing up in several communities |
| **Duplicates** | `/duplicates/{id}`: the same URL submitted elsewhere | How a product, article or study spreads |
| **Shared external URL / product** | Normalized Amazon ASINs, Shopify product URLs, brand domains, TikTok links | Every thread talking about a competitor's product |
| **Entity co-mention** | Brands, products and ingredients pulled out during extraction (e.g., "minoxidil", "rosemary oil", "Kitsch") | Builds the **failed-solutions ladder** across the whole corpus |
| **Semantic similarity** | kNN on thread embeddings above a threshold | Finds threads that discuss the same problem in different words |
| **Audience overlap** (aggregate only) | Number of distinct commenters two threads share | Shows which communities hold the same avatar (e.g., r/beyondthebump ↔ r/FemaleHairLoss) |
| **Search co-occurrence** | The thread came up for several seed queries | A signal of relevance |

### Frontier priority
`priority = relevance(seed brief, embedding) × log(engagement) × edge_weight × novelty × recency_decay`

There are hard limits: `max_threads`, `max_hops` (default 2), per-subreddit caps so one sub can't dominate, and a minimum comment count.

### Graph analysis exposed to Claude
- **Communities** (Leiden), each auto-labelled by Claude, e.g. "postpartum shedding panic", "minoxidil dread", "oil application mess"
- **Hub threads** by PageRank, which are the threads everyone links back to
- **Bridge threads** by betweenness, where one avatar crosses into another problem space. These are good sources of new angles.
- **Subreddit map** that shows where the avatar actually lives
- Exports: interactive HTML graph (sigma.js), GEXF for Gephi, and a CSV edge list

---

## 4. Analysis layer: built around your research framework

The extraction schema follows the vocabulary in your longform copy file: avatar, failed-solutions ladder, verbatim emotional language, sub-desires, objections and "taken avatars".

### Two-pass pipeline (this is what makes thousands of threads affordable)
1. **Cheap filter (no LLM).** FTS keyword and regex hits plus embedding similarity to the brief, with score and length thresholds. This usually cuts 60–90% of comments.
2. **LLM extraction** on the comments that pass, batched by thread so the model sees the parent context. It uses structured outputs (`output_config.format` with a JSON schema) and returns, per comment:
   - `pains[]`, `desires[]` (mapped to sub-desires), `failed_solutions[] {product, why_failed, quote}`
   - `objections[]`, `beliefs[]` (e.g., "it'll grow back"), `triggers/moments[]` ("2AM", "shower drain")
   - `brands_products[] {name, sentiment, context}`, `price_mentions[]`, `buying_intent`, `questions_asked[]`
   - `identity_statements[]` ("as a first-time mom…"), `awareness_level`
   - **Every item carries a `quote` and the comment ID.**
3. **Verbatim check (non-negotiable).** Each `quote` is string-matched against the stored comment text. Anything that doesn't match exactly is discarded or flagged. This enforces your "verbatim-sourced emotional language only" rule automatically.
4. **Aggregate.** Cluster near-duplicate insights, then rank by `support` (distinct authors) × upvote weight × recency. Output: a **language bank**, a **failed-solutions ladder** with frequencies, an **objection matrix**, a **competitor sentiment table**, and **angle candidates**, all with links back to the source.

### Model and cost plan
- Default model is **Claude Opus 5.5** (`claude-opus-5-5`), set to `effort: "low"` for bulk extraction and higher for final synthesis.
- If you want cheaper bulk runs, **Claude Haiku 5.5** (`claude-haiku-5-5`) can do the per-comment pass, with Opus 5.5 kept for synthesis. That's a cost/quality choice for you to make; I'd measure both on the golden set (section 7) first.
- Use the **Message Batches API** for bulk extraction (asynchronous, about 50% cheaper). Put **prompt caching** on the fixed system prompt and schema so repeated calls reuse it.
- Rough volume: 1,000 threads × ~150 comments is ~150k comments. After the filter, about 20–40k reach the LLM.

---

## 5. MCP tool surface (designed for Claude's context window)

Every tool returns a **summary first, details paged**. Claude never receives a raw dump of 10,000 comments.

| Tool | Purpose |
|---|---|
| `create_study(name, brief, seeds, budget)` | Starts a project. The brief drives relevance scoring. |
| `discover(study, queries[], subreddits[], time_range, min_comments)` | Seed search; returns a ranked candidate list |
| `crawl(study, max_threads, max_hops, edge_types[])` | Builds the web asynchronously; returns a job ID |
| `job_status(job_id)` | Progress, coverage, errors |
| `get_thread(id, view="outline"\|"top"\|"subtree", comment_id?, max_tokens)` | Reads one thread in a token-budgeted view |
| `search(study, query, mode="hybrid", filters)` | FTS plus semantic search across the corpus |
| `graph_overview(study)` | Communities, hubs, bridges, subreddit map |
| `neighbors(thread_id, edge_types, k)` | Walks the web from one thread |
| `extract(study, schema="ecom_v1", scope)` | Runs the two-pass pipeline (batch) |
| `insights(study, kind, min_support, page)` | Aggregated pains, failed solutions, objections, brands, with quotes |
| `quotes(study, label, page)` | Verified verbatim quotes for one insight |
| `compare(study_a, study_b)` | Avatar or competitor differences |
| `export(study, format=csv\|json\|md\|gexf\|html)` | Parity with the reference exports, plus graph and report exports |
| `watch(study, schedule)` | A "Radar": re-crawl and diff, then surface new threads and new language |

There's also a **CLI** with the same functions (`rr fetch <url>`, `rr crawl`, `rr export`) and a **Claude Code skill** (`SKILL.md`) that encodes the research playbook. The skill covers how to write the brief, which subreddits to seed, when to expand the web, and the output format your copy workflow expects.

---

## 6. Build phases

| Phase | Scope | Done when |
|---|---|---|
| **P0: Teardown** | Section 1 with REA | `FINDINGS.md` parity checklist written |
| **P1: Fetcher + store** | OAuth/.json/Arctic Shift sources, full trees with `morechildren`, SQLite, `rr fetch`, CSV/JSON/text export | Matches the reference's fields on 5 test threads, with ≥98% coverage against `num_comments` |
| **P2: Discovery + web** | Seed search, best-first crawler, all edge types, communities and hubs, HTML graph | A 300-thread study crawls, resumes after being killed, and shows a sensible graph |
| **P3: Extraction** | Filter → structured extraction → verbatim check → aggregation | 100% of surfaced quotes verify; insights ranked by support |
| **P4: MCP + skill** | Tool surface (section 5), paging, research-playbook skill | Claude runs a full study end to end from one prompt |
| **P5: Radar** | Scheduled refresh, new-thread alerts, diff reports | A weekly diff shows only new or changed signal |

---

## 7. How we'll know it's the best version (evaluation)

- **Golden set:** your existing scalp-oil / postpartum research. The tool should independently rediscover the failed-solutions ladder you already wrote by hand (prenatal vitamins → biotin → collagen → minoxidil → castor/rosemary oil), plus the "it'll grow back" belief and the 2AM moment.
- **Metrics:** comment coverage per thread, quote-verification rate (target 100%), recall of the golden-set insights, duplicate rate, cost per 1,000 threads, and graph precision (hand-check 50 edges).
- **Regression fixtures:** the REA replay environment from section 1, step 5, plus saved thread JSON, so tests never hit Reddit.

---

## 8. Decisions for you

1. **Where it runs.** On your computer, which is recommended because a home IP gets through to Reddit. The alternative is cloud only, using the Arctic Shift and Apify fallbacks.
2. **Reddit API app.** Do you want to register a personal "script" app (free) to get the official OAuth route?
3. **Bulk-extraction model.** Opus 5.5 everywhere (default), or Haiku 5.5 for the bulk pass once it has been measured.
4. **Apify budget,** if any, for when Reddit blocks requests.
