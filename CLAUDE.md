# Ecommerce / Marketing Ops — Reference Index

This session is also used for the user's ecommerce native-image-ad product validation and
copywriting work (unrelated to the GitHub-profile README this repo otherwise holds). The user
maintains a shared Google Drive "Master Doc" folder with the operating playbooks for this work.
Read this file at the start of any session touching that work, and pull the relevant section from
Drive on demand rather than re-deriving the workflow from scratch.

## Where things live (Google Drive)

- **"Aarreign's Master Document"** (Google Doc, id `1aNoyCdvs485a16GD5ews1IwNTI-CNt0anToER2001cc`,
  owner `decommerce2@gmail.com`, shared with the user) — the full prompt library. ~222k characters;
  read it via `mcp__Google_Drive__read_file_content`, it will exceed inline token limits, so use
  `jq`/python on the saved file per the tool's own overflow instructions, or grep the section you need.
- **"Master Doc" folder** (id `16AFdG34gjM6gqM57jHvsX9L1YPzsO6UU`) contains:
  - `Marketing Books` subfolder (id `1Zcee5vIqKTPeI8BJ0VB-7MvzFNG1Z7PM`) — currently **empty**.
    Breakthrough Advertising (Schwartz) and Great Leads (Masterson/Forde) are NOT here yet; the
    Longform Copy prompt's intake still needs those pasted directly when it's run.
  - `native image pdf` subfolder (id `1gmIuJ8rzofRGL3YQIZTy5sH5P4AHxd5u`) — has
    `native-style-headline.pdf` and possibly more (paginate if needed).

## Master Document contents (by section, line numbers as of 2026-09-26)

| Section | What it is |
|---|---|
| Brand Audit | Competitor research prompt → outputs `brand-brief-<brand>.md`. Evidence-tagged ([OBSERVED]/[INFERRED]/[UNVERIFIED]), needs 30+ ads before concluding "what's working," ranks by runtime/rank/duplication/reach delta. |
| Find Avatars | Untapped-avatar generation prompt. Hard rules: burning-desire test, TAM estimation, evidence tags. |
| Reddit Research | VOC-mining prompt for Reddit. Hard rule: nothing inferred, verbatim only, privacy rules for quoting real users. |
| Longform Copy | The direct-response copywriter persona (5-step intake: Breakthrough Advertising → Great Leads → avatar research file → brand brief → offer/destination Q&A). No em dashes outside P.S./CTA, verbatim VOC only, one avatar per piece, diagnosis card + 3 ranked hooks + full piece + VOC trace + verification checklist. |
| Product Images | Prompt for generating product photography prompts. |
| Native Images | 20-image native ad system prompt: no product visible in-image, phone-camera quality only, image is the hook/copy is the sell. |
| Shrine Theme | Shopify theme-editing workflow (product.json → paste into Claude Code). |
| Dissect Winner | Reverse-engineers a competitor's winning ad/copy — cites everything, counts patterns, writes no new copy. Uses the same six lead types (Great Leads) + five awareness states (Schwartz) vocabulary as Longform Copy. |
| Reword Winners / Variation Winners | Iterates on your own winning copy — a "Winning Copy Variation Engine." |
| Advertorials / Listicles / Quizzes | Funnel-page builders that sit between the ad and the product page. |
| Swipe File (Native Ads, Tab 14, Animation Ads, VSL Ads) | Reference swipe examples by format. |
| Landing Pages | Landing page prompt/structure. |

## How to use this

- When the user references "the master doc," "the playbook," or names one of the above prompts by
  name (Brand Audit, Find Avatars, Reddit Research, Longform Copy, Dissect Winner, etc.), pull that
  section from the Drive doc rather than asking them to re-paste it, unless it's genuinely faster
  for them to paste an update.
- The user's actual product work this session: validating ecommerce products for native image ads
  (scalp oil dispenser / postpartum hair loss avatar was the deepest one so far — avatar research,
  Reddit VOC mining, and an angle-brief doc already exist as Claude artifacts from prior sessions).
- Brand name for the scalp dispenser product is still undecided as of 2026-09-26 — don't assume "Ecovia."
