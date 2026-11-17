# reddit-research

A free Reddit research engine that Claude drives. It pulls **complete** threads (every hidden reply), follows the
links between threads to build a **web of related discussions**, and stores **quote-verified insights** (pains,
failed solutions, objections, beliefs, triggers, brand mentions, buying language) with links back to the source.

Costs nothing to run:

| Piece | What it uses | Cost |
|---|---|---|
| Reddit data | Your own browser profile, logged into Reddit once (the same trick the redditcommentscraper.com extension uses) | free |
| Fallback data | [Arctic Shift](https://arctic-shift.photon-reddit.com), a public Reddit archive | free |
| Analysis | Claude Code / Claude Desktop, which you already have; no API key and no per-call billing | free |
| Storage | One SQLite file on your PC | free |

No Reddit developer app is needed. Since mid-2026 new API apps need manual approval that takes weeks, and Reddit blocks
logged-out scripts. Reading through your own logged-in browser avoids both.

---

## Install on your PC (about 5 minutes)

You need: **Chrome or Edge** (every Windows PC has Edge), **git**, and
**Claude Code** (`npm install -g @anthropic-ai/claude-code`) or Claude Desktop.

**Windows** (PowerShell):
```powershell
git clone -b claude/sweet-einstein-jrcl1q https://github.com/Kengokuhebun/Kengokuhebun.git
cd Kengokuhebun\reddit-research
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

**macOS / Linux**:
```bash
git clone -b claude/sweet-einstein-jrcl1q https://github.com/Kengokuhebun/Kengokuhebun.git
cd Kengokuhebun/reddit-research
bash install.sh
```

The installer:
1. installs `uv` (a free Python manager) if you don't have it
2. installs the `rr` command
3. registers the MCP server with Claude Code
4. installs the research playbook skill

Then:

```bash
rr login     # a normal browser window opens on Reddit's login page: log in, then CLOSE the window
rr doctor    # checks the archive, your login, and a live Reddit request
```

The login window is a plain, separate browser profile with no automation attached, so Reddit sees a normal
login and your everyday Chrome is untouched. If Reddit ever shows "whoa there, pardner", wait 10 minutes and run
`rr login --fresh`. Your Reddit session stays on your computer, in `~/.reddit-research/browser-profile`. Requests are spaced 1.5 s apart
(about 40 a minute). To be extra careful, log in with a secondary Reddit account.

### Claude Desktop instead of Claude Code
Open Settings → Developer → Edit Config, and add:
```json
{ "mcpServers": { "reddit-research": { "command": "rr", "args": ["serve"] } } }
```
If Claude Desktop can't find `rr`, use its full path. Run `where rr` (Windows) or `which rr` (Mac) to find it.

---

## Use it

In Claude Code, just ask:

> Research postpartum hair loss on Reddit for my scalp oil dispenser. I want the failed-solutions ladder, objections,
> the moments that trigger buying, and verbatim language. Get at least 150 threads and show me the thread web.

Claude follows the playbook in `.claude/skills/reddit-research/SKILL.md`:
1. create a study
2. pick subreddits
3. discover seed threads
4. crawl the web of linked threads
5. read threads and save quote-verified insights
6. report

Everything is saved, so you can come back days later and say "continue the pp-hair study".

### Command line (works without Claude too)
```bash
rr fetch https://www.reddit.com/r/beyondthebump/comments/1w4szr6/ --format csv   # one full thread -> CSV
rr study pp-hair --brief "postpartum hair loss, scalp oil, biotin/minoxidil failures" --keywords biotin "rosemary oil"
rr subs postpartum
rr discover pp-hair -q "hair falling out after baby" -q "rosemary oil" -s beyondthebump -s FemaleHairLoss --time year
rr crawl pp-hair --max-threads 100
rr graph pp-hair              # builds the web and writes an interactive map (HTML)
rr search "dread shed" --study pp-hair
rr report pp-hair --kind failed_solution
rr export pp-hair --format md  # or csv, json, html, gexf, insights_csv
```
Files go to `~/.reddit-research/exports`.

### Settings
```bash
rr set source auto        # default: your browser if logged in, archive as fallback
rr set source arctic      # archive only (no login, slower search, data ~36h behind for scores)
rr set reddit_min_interval 2.5   # slow down further
rr set headless false     # watch the browser work
rr set browser_path "C:\Program Files\Google\Chrome\Application\chrome.exe"   # pick a specific browser
```

---

## How the thread web is built
Threads are connected when:

| Connection | How it's found | Why it matters |
|---|---|---|
| **link** | a comment or post links to another thread | people pointing each other to the "real" discussion |
| **crosspost** | Reddit crosspost data | the same pain point showing up in several communities |
| **same_link** | the same URL submitted in different places | how an article or product spreads |
| **shared_product** | the same product page linked (Amazon ASIN, Shopify product, YouTube video) | every thread about a competitor's product |
| **shared_brand** | the same brand website linked | brand mentions across communities |
| **similar** | similar wording (TF-IDF) | the same problem described in different words |
| **audience** | 3 or more of the same commenters (counted only; names are never shown) | where the same avatar hangs out |

The crawler expands best-first: relevance to your brief × engagement × closeness to the seed threads. It then groups
threads into communities, ranks hub threads (PageRank) and finds bridge threads, which join two groups and often
point to new angles.

## How it compares with redditcommentscraper.com
I took their Chrome extension apart (v4.17.3) with [REA](https://github.com/morluto/rea) and read its code. It calls
Reddit's own `.json` endpoints from your browser, uses `/api/morechildren` for hidden replies, and stops after 40
"continue this thread" stubs. Its paid CLI sends blocked requests through their own server.

| | redditcommentscraper | this tool |
|---|---|---|
| Comments per thread | 20 free, 1,000 paid | all of them, with coverage % reported |
| Threads per run | 1 | hundreds, resumable |
| Links between threads | none | 7 connection types, groups, hubs and bridges, interactive map |
| Search across everything | no | full-text, ranked by match and upvotes |
| Insight extraction | paid AI add-on | Claude, with every quote verified word for word |
| Price | $9.99–$199/month | $0 |

## Tests
```bash
uv run --extra dev pytest          # offline tests with a fake Reddit
uv run --extra dev pytest -m live  # also hits the real Arctic Shift archive
```

## Be a good citizen
This tool is for your own research. Keep the request pace, don't republish or resell the raw data, and talk about
patterns rather than individual users. Reddit's terms restrict automated collection and commercial use of its data.
You're responsible for how you use it.
