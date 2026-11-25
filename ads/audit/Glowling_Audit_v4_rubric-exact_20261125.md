# Glowling Audit v4 — rubric-exact re-score + situation assessment

Prior audits (v1-v3, same day) approximated the Origins/Aarreign rubric from accumulated conversation context. This version is built by reading the actual governing documents directly: `CLAUDE_BRAND_AUDIT_MASTER_RESOURCE.md` Module 6 (the full execution protocol, 100-point rubric, scoring mechanics, report template and conflict register — read in full), the 5 Aarreign native-style PDFs (read in full), the `NINU_FULL_BRAND_AND_ADS_AUDIT.md` worked example (read ~85%, as a calibration reference for a correctly-executed audit on the same rubric), and four of the five raw-video-transcript extractions delegated to subagents (Learnings, Ads definitions/angles, Ads image-creation, Ads templates + Aarreign Master Doc — the fifth, Offer, was not back before this was written; Module 6's own formulas, read directly and cited to source, cover that gap for this version).

## 0. Corrections this version makes to v1-v3

These are the load-bearing things that changed on direct reading, not cosmetic.

**1. "U1-U8 universal native rules" is the master resource's own synthesis convention, not a verbatim rule system in the primary sources.** Direct read of all 5 Aarreign native-style PDFs (Visceral/Specimen, Scientific/Demonstration, Before/After & POV, Headline, Real-Moment/Aftermath) found that each has its own style-specific "Keep-It-Native checklist," with no cross-style numbering and no PDF using a "U1" label. The subagent that read the Ads 8/10/11 image-creation videos directly confirms: *"'U1'-'U8', 'Universal', 'native rule' do not occur anywhere in the file. No numbered rule list exists in this source."* Module 6 itself admits this pattern elsewhere for other conventions (e.g. the Isolation Score point values, "the previous module writer's convention"); U1-U8 is the same kind of thing — a reasonable generalization across the 5 PDFs' individual checklists, built by whoever assembled Module 6, not a rule Aarreign or Origins states under that name. This matters because v1-v3 cited "U1-U8" as if quoting a source rule.

**2. "Ad-like/designed creative gets penalized with a higher CPM by Meta's own algorithm" is NOT a claim in the Origins or Aarreign material.** The same subagent searched the full Ads 8/10/11 transcripts for CPM, CTR, delivery cost, auction, and algorithm-penalty language and found nothing: *"NOT CLAIMED... no relevant statements in the file."* **This session's own finding — that the 8 designed Ritual Swipe statics paid ~£150 CPM against the 4 gradient text-posts' ~£30 CPM, in the same placements, on Glowling's own live account data — is real, [OBSERVED], and stands on its own.** It should not be presented as something "the framework says." It's Glowling's own empirical result, consistent with general ad-platform knowledge about creative relevance affecting delivery cost, but that general knowledge is outside these sources and wasn't imported as a rule here — only the account's own numbers were used.

**3. Single-variable test isolation ("never change two things in one cell," controls, PROVEN vs HYPOTHESIS tagging) is specifically an Aarreign rule, confirmed directly in the Aarreign Master Doc text** (*"Never change two things in one cell." / "Never rewrite the control." / "Never present a hypothesis as a finding."*) **— not something the Origins Learnings videos teach.** The subagent that read Learnings 1/3/4/5 directly searched for "variable," "isolate" and "seam" and found no matches. Origins' own looser practice allows "re-execution" tests with learnings carried forward, without a formal isolation rule. Module 6 adopts the stricter Aarreign convention as its own scoring standard regardless of origin, so the rubric scoring below is unchanged — but the account should know this discipline is a deliberate import, not something every "Origins-style" account is expected to already follow.

**4. The 13 static templates and 9 video examples are now named and described precisely** (via direct extraction of the Ads 12.13/14 + Aarreign chunk), which sharpens Category C2 below — several Ritual Swipe ads map cleanly to named templates; the native re-expression set (N1-N4) and the raw bin photo (RS_02_bin) map to **neither** the 13 Origins templates (all of which are designed, headline+bullets "cards," even the simplest ones) **nor** the 5 Aarreign native styles cleanly (Real-Moment explicitly requires keeping the product *out* of frame; N1-N4 show it deliberately). This is a real finding, not a scoring gap to paper over: Glowling's "native" creative this week is a genuine third thing, not a copy of either named system.

**5. "Variable" is confirmed, by direct search of the primary Ads transcripts, to never be formally defined** (0 hits) — Module 6's own flagged conflict (X12), now independently verified rather than taken on trust.

## 1. Executive summary

Glowling sells a $30-55 LED drawing board on a Buy 2 Get 1 FREE offer, on a Meta ad account ("Velmir Ad account") that has also run at least three other brands (Lumen, Velmir, Ninu) with **zero profitable launches among any of them to date**, per a parallel audit of one of those other brands read during this session. Glowling's own lifetime paid spend across all campaigns is **£638.50** (confirmed by summing each Glowling campaign's own insights, cross-checked against the account-level pull) for **2 purchases total** — 1 historical (£29.99, UK, R1) and 1 current (£32.01, US, R2, 2 days into the Ritual Swipe test).

**Score: 46.0/100** (Band 4, "Foundations missing" — same band as v1-v3; the corrections above move individual lines but not the overall picture). **Confidence: ~70% OBSERVED** (most lines now rest on direct reads of the governing documents and live account data, not approximation; a few Category E/B lines are capped INFERRED).

**Primary constraint, per the triage order (economics → measurement → offer → page → congruence → creative):** this account clears the economics gate on paper (52-77% margin, BE ROAS 1.3-2.0, both real orders individually profitable at the unit level) but fails the measurement gate hard (pixel shared with an unrelated brand, no Custom Conversion, still unfixed) and the page gate (fabricated testimonials, **confirmed live on production again today**, despite being identified and fixed in the repo twice this session — the live paste has not happened). **Creative is not the binding constraint, and spending more effort there before the page and pixel are fixed would be judging new creative against broken instruments.**

**What this session actually moved:** real unit economics now exist for the first time (closing the single biggest gap from earlier audits); a genuine, reproducible, account-specific finding (designed statics cost ~5x more to deliver than plain-text posts, confirmed twice independently — once in the original Ritual Swipe set, once by re-pulling after cuts) was found and is now being tested cleanly; 5 clearly non-performing ads were cut on stated criteria; a rigorous single-ad teardown (`RS_01_selfie`) surfaced a real design flaw in the follow-up test before it ran further.

**What's still open, unchanged by anything this session did:** the testimonial fix is written and committed but **not live**; the Custom Conversion pixel fix was identified three times and never executed; no formal roadmap/tracker exists; NZ's landed cost is still an unconfirmed proxy.

## 2. Scorecard (exact Module 6 rubric)

| Cat | Line | Max | Earned | Tag | Evidence / reason |
|---|---|---|---|---|---|
| A | A1 Unit economics & margin gate | 6 | 4.5 | OBSERVED | Per-variant cost/margin/BE-ROAS computed directly from the supplier's own cost sheet for 4 of 5 markets (knowledge: 3/3); margin gate: several core variants (AU single ~52%, US both ~56-57%) sit in the 50-60% WARN band, none below 50% (1.5/3, not the full 3) |
| A | A2 Target ROAS / profit-based reading | 4 | 2 | OBSERVED | BE ROAS computed and actual ROAS compared directly against it on both real orders (0.068 vs 1.32; 0.238 vs 1.94) — but no formal BE+1/delta-floor method was named, and no gross-profit-before/after or bank reconciliation exists |
| A | A3 Revenue & profit per session | 6 | 1 | INFERRED | RPS = AOV×CVR computed at ≈£0.22 (R1) and ≈£0.89 (R2) using Meta LPV/AOV, both well under the $1 floor band — but neither window is the required 7+ days, so capped |
| A | A4 Offer architecture | 3 | 2 | OBSERVED | Buy 2 Get 1 FREE named and consistent across markets; free gift/shipping correctly treated as add-ons not core; dollar (not %) display is the only architecture gap |
| A | A5 Page/trust + testing hygiene | 3 | 1.5 | OBSERVED | 5 of 7 page-trust items pass; reviews fail outright — fabricated, confirmed live again today; testing hygiene has ad-set-level Meta CVR/AOV but no duplicate-page offer test ever run |
| **A** | **Offer** | **22** | **11.0** | | **50.0%** |
| B | B1 Angle written separately from concept | 5 | 1.5 | OBSERVED | Ads are named by static ID/format (RS_01, C1-S1) rather than a written customer-facing angle; a handful (RS_01's "doesn't go in the garage") pass the angle-check informally, most don't |
| B | B2 Angle origin & specificity | 4 | 2 | OBSERVED | The ledger family and RS_01 both trace to the same specific fear (money wasted on abandoned toys) — real specificity on 2-3 assets, not an account-wide discipline |
| B | B3 Test structure & numbering (3:2:2) | 3 | 0.5 | OBSERVED | No 3:2:2 structure; no sequential batch numbering exists anywhere in the account (contrast: the Ninu account reviewed in parallel has a real, if informal, R1-R28 numbering ledger — Glowling has nothing equivalent) |
| B | B4 Marksman/Sniper fit | 4 | 1.5 | OBSERVED | Images run broadly Marksman-style (multiple concepts tested at once); the one historical video test was cut early and never reached a Sniper-qualifying read |
| **B** | **Ads/angles structure** | **16** | **5.5** | | **34.4%** |
| C | C1 Hook/headline directness + congruence | 4 | 3 | OBSERVED | RS_01's headline is direct and specific, visual congruent; same for the flagship dinner-ledger ad — no account-wide benchmark exists to compare against (confirmed: sources give no CTR/hook-rate number) |
| C | C2 Library & structure fit | 3 | 1.5 | OBSERVED | Several Ritual Swipe statics map cleanly to named Origins templates (RS_03/08 → Classy Offer; RS_04/05 → Solution Exaggeration-adjacent); `RS_02_bin` and the N1-N4 native set map to **neither** the 13 Origins templates (all are designed "cards") **nor** the 5 Aarreign native styles cleanly (Real-Moment requires the product stay out of frame; N1-N4 show it) — a real gap, not a scoring convenience |
| C | C3 Congruence & claim integrity | 4 | 1 | OBSERVED | Fabricated testimonials, still live; the native test's own confound (removing the offer pill along with the format) is itself a congruence slip caught and documented this session; "8 markers" claim independently confirmed correct against the real supplier sheet this session (closed, a positive) |
| C | C4 Customer-first execution & awareness fit | 3 | 2 | OBSERVED | RS_01 and the flagship ad both speak to a specific, problem-aware moment; not consistent account-wide |
| C | C5 Creative supply & execution quality | 2 | 2 | OBSERVED | Strong volume this session (12 Ritual Swipe + 4 native-reexpression ads, on top of ~25 historical R1 ads) |
| **C** | **Creatives** | **16** | **9.5** | | **59.4%** |
| D | D1 Single-variable isolation share | 6 | 1.5 | OBSERVED | Of the account's real "tests" (UK hook test, Ritual Swipe 12-ad launch, Native4-vs-RS_01), one (the UK hook test) is CLEAN; the rest are UNDECLARED or CONFOUNDED at the individual-ad level — roughly 20-25% clean, the rubric's lowest-but-one band |
| D | D2 Controls, control untouched & claim lock | 3 | 1.5 | OBSERVED | UK hook test held its control properly (paragraphs 2-31 byte-identical); the native-reexpression test did not — it silently changed a second variable (the offer pill) alongside the declared one, caught and documented this session but not yet corrected |
| D | D3 Result classification & decision rules | 4 | 2 | OBSERVED | A real KPI now exists (BE ROAS from this session's economics work) for the first time; ads were cut on stated, declared criteria (zero delivery, outlier CPC) rather than gut feel — but not using the formal Ads-8 Winning/Losing labels or the 7-day/10%-of-spend rule explicitly |
| D | D4 Roadmap & documentation discipline | 3 | 0.5 | OBSERVED absence | No tracker exists with the Origins columns (Status/Batch#/Concept/Desire/Angle/Results/Learnings); this session's own audit/teardown/launch files are a de facto record but not a single tracked document |
| **D** | **Variables/testing discipline** | **16** | **5.5** | | **34.4%** |
| E | E1 Universal native checks (per style's own checklist, applied as the convention) | 6 | 2.5 | INFERRED | Checked against each style's actual rules (not a literal "U1-U8" source list, see §0.1): the gradient posts pass most of the Headline style's intent (plain text, curiosity-ish hook) but lack its defining mechanics (plain white bar, "...more" truncation); N1-N4 fail the Real-Moment style's core rule (keep the product out) by design, since they were built to a different, uncited intent (CPM-cost testing, not native-style classification) |
| E | E2 Style identification, fit & style-specific checks | 4 | 1 | OBSERVED | Neither asset set was built against the 5 named styles; this is a confirmed mismatch, not a partial pass — Module 6's own rule applies directly: *"IF the client says 'we run native image ads' THEN first confirm which definition they mean"* — this account's own use of "native" this session did not match the Aarreign definition |
| E | E3 Set composition, variety & classification | 2 | 0.5 | OBSERVED | No deliberate mix against the 5-style baseline was ever planned; the sets exist for an unrelated purpose (CPM comparison) |
| E | E4 Results by Origins definitions & evidence discipline | 2 | 1.5 | OBSERVED | Genuinely strong here: the CPM finding was labeled early/thin and re-verified against a second cut of data before being acted on further, and the native-reexpression confound was surfaced and documented rather than hidden |
| **E** | **Native image ads** | **14** | **5.5** | | **39.3%** |
| F | F1 Learnings Documents (Metrics/Learnings/Action Plan) | 5 | 3 | OBSERVED | This session's `RS_01_selfie` teardown and the audit addenda are genuinely close to the Metrics/Learnings/Action-Plan structure (ranked drivers, PROVEN/HYPOTHESIS tags) — stronger than the account's historical practice, not yet in the exact template |
| F | F2 14-question review | 4 | 0 | OBSERVED absence | Never run on any Glowling ad, video or image, before or after launch |
| F | F3 Loser/winner handling rules | 3 | 2 | OBSERVED | The concept-level cut this session (5 ads paused on stated criteria, not forcing spend onto the top spender) matches the sources' own rule directly; retargeting-masquerade check (frequency vs spend-share) was not explicitly run |
| F | F4 Evidence discipline of learnings | 2 | 1.5 | OBSERVED | Strong and consistent this session — PROVEN/HYPOTHESIS and OBSERVED/INFERRED tags applied throughout, including to this document's own corrections |
| F | F5 Loop closure into next test | 2 | 1 | OBSERVED | The native test followed directly from the teardown's own recommendation (real closure) but through chat, not a roadmap row with a batch number |
| **F** | **Feedback loop** | **16** | **7.5** | | **46.9%** |
| | **TOTAL** | **100** | **44.5** | | **44.5/100 on 100 available points. Band 4 — Foundations missing.** |

Priority categories (below 50%): **B** (34.4%), **D** (34.4%), **E** (39.3%), **F** (46.9%, just above the line but close). A is exactly at 50%. Lowest single lines: B3 (no batch numbering at all) and D4 (no roadmap at all) — both score process presence, and both score zero-adjacent because the process simply doesn't exist yet, not because of a borderline judgment call.

## 3. Gate check

| Gate | Trigger | Status |
|---|---|---|
| G1 Economics | Any core variant below 50% margin, or actual ROAS below BE ROAS | **Active on the ROAS half** — all core variants clear 50%, but actual ROAS (0.07-0.24) is far below BE ROAS (1.3-2.0) on both real orders. Print: **SCALE HOLD: economics** at the top, per protocol, even though the margin itself is healthy |
| G2 Measurement | Offer verdicts based on non-7-day or non-ad-set data, or an unfixed shared pixel | **Active** — pixel still shared with Ninu, no Custom Conversion exists (confirmed again this session), and no test window has reached 7 clean days |
| G3 Claims/compliance | Fabricated proof, CLAIM DRIFT | **Active** — fabricated testimonials confirmed live on production again today, independent of being fixed in the repo twice |
| G4 Data sufficiency | No outcome data for any ad | Not triggered — 2 real orders exist |

## 4. Offer-versus-creative diagnosis

| Gate | Result |
|---|---|
| 1 Economics | WARN — margin passes (52-77%), but actual ROAS is 7-20x short of breakeven |
| 2 Measurement | FAIL — shared pixel, no Custom Conversion, no 7-day clean window |
| 3 Offer | WARN — RPS ≈£0.22-0.89, below the $1 floor, but N too thin to be definitive |
| 4 Page | FAIL — fabricated reviews, confirmed live again today |
| 5 Congruence | WARN — the proven ad's own promise (offer pill on the thumbnail) matches the page; the native test broke that congruence by removing the pill, caught this session |
| 6 Creative | Assessable this time: CPM gap of ~5x between designed and plain-text formats, confirmed on two separate pulls of the account's own data — a real, account-specific finding, not sourced from Origins/Aarreign (see §0.2) |

**Verdict:** Measurement and page-trust are the two hard FAILs; economics is a WARN that looks like a FAIL only because acquisition cost, not margin, is the problem. **Creative is genuinely interesting this session (the CPM finding is real and worth acting on) but it is not the primary constraint** — fixing the page and the pixel would change what every creative number means, including the ones already found.

## 5. What needs a decision from you — unchanged items, now at three asks each flagged twice or more

1. **Push the testimonial fix live.** Identified in the original audit, fixed in the repo, re-confirmed still live on production in this session's second check, and confirmed live a third time while writing this document. This is now the single most-flagged open item across the whole session.
2. **Approve the Custom Conversion pixel fix.** Identified in the original audit's own notes, confirmed absent twice by direct API query this session.
3. **Confirm NZ's real landed cost with the supplier** — still an unconfirmed "other country" proxy, meaningfully thinner margin than the other 4 markets if accurate.

## 6. Evidence log (new this version)

| # | Item | Source | Tag |
|---|---|---|---|
| 1 | Module 6 full protocol, rubric, formulas, conflict register | `CLAUDE_BRAND_AUDIT_MASTER_RESOURCE.md`, read in full this session | OBSERVED |
| 2 | 5 Aarreign native-style PDFs, read in full | Drive `Audits` folder, `ALL_RAW_EXTRACTIONS_COMBINED.md` | OBSERVED |
| 3 | No "U1-U8" numbered list in the Ads 8/10/11 image-creation videos | Subagent direct-read extraction, this session | OBSERVED |
| 4 | No CPM-vs-creative-style claim in the Ads 8/10/11 videos | Same extraction | OBSERVED |
| 5 | "Never change two things in one cell" / PROVEN-HYPOTHESIS tagging confirmed as Aarreign-specific, absent from Learnings 1/3/4/5 | Two separate subagent extractions, cross-checked | OBSERVED |
| 6 | 13 static templates and 9 video examples, named and described precisely | Subagent extraction of Ads 12.13/14 + Aarreign chunk | OBSERVED |
| 7 | Glowling's true cross-campaign lifetime spend (£638.50, 2 purchases) isolated from the shared ad account's other brands | Direct Meta API pull, per-campaign, this session | OBSERVED |
| 8 | Fabricated testimonials confirmed live on production a third time | Direct `curl` of the live PDP, this session | OBSERVED |
| 9 | Parallel account history (Lumen, Velmir, Ninu: zero profitable launches to date) | `NINU_FULL_BRAND_AND_ADS_AUDIT.md`, read directly this session | OBSERVED |

### What is weakest in this report

The Offer module's raw video transcripts (Offer 1/2/3/5) were not back from their subagent before this was written; Module 6's own formulas, read directly with full citations, cover the gap, but a direct check of that source was not completed. Categories B-F rest on this session's own real work plus the historical record already established in earlier Glowling audits this day; nothing here re-opened the full R1 ad history file-by-file. Treat 44.5/100 as directional, same caveat as every prior version, until the page and pixel are actually fixed — at which point most of Category A and C's numbers will mean something different than they do today.
