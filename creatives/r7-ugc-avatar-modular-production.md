# R7 — Modular UGC avatar production: 3 hooks, 1 shared body, ~30s

Builds on `ads/kitsch-ugc-teardown-and-reproduction.md` (structure/pacing reference) and
`creatives/r6-ugc-avatar-validation-script.md` (avatar persona, originally single-hook).
This version is production-structured for your actual ask: generate the body once, generate
3 hook variants separately, stitch each hook onto the same shared body footage. That gives you
3 finished videos from 4 total generation passes (1 body + 3 hooks), and it's a clean
single-variable test — identical footage after the cut, only the hook differs.

**No Google Flow connector available in this session** (checked — only Google Drive is
connected here), so I can't generate inside it directly. Workflow stays: I give you the
scripts and first/last-frame prompts below, you run them in Flow, send me the output and I'll
check it against the script before you cut anything together — same loop as the Grok test.

**On the 30s target:** trimmed the shared body hard to get there. Kitsch's own video got to
40s by dropping price/CTA/guarantee entirely — I'm not recommending that here (changes two
variables at once: format AND removing a FIXED beat you've never tested dropping). Instead the
offer is compressed to a 3-second tag at the end rather than removed. Total lands around
30-33s depending on delivery pace, hook included.

**On exact clip-length limits:** I don't know Google Flow's per-generation cap for your account,
so segments below are split by content/beat, not forced into assumed second-counts. If your tool
caps shorter than a given segment, split it further at a natural sentence break and use the same
first-frame/last-frame continuity principle (section 4) to keep the join clean.

---

## 1. Avatar persona (lock this across every segment and every hook variant)

Same identity used in `r6-ugc-avatar-validation-script.md` — don't introduce a different look
per hook, or you've changed two variables at once.

- Early-to-mid 30s, postpartum mom aesthetic, soft warm skin tone, minimal/no makeup, slightly
  tired but not styled
- Dark-to-medium brown hair, worn down, slightly undone
- Oversized soft grey or oatmeal sweater/robe — Ninu's own established wardrobe register, not
  Kitsch's fitted tank top. Keep what's already consistent across R4/R5/R6 rather than copying
  the competitor's incidental wardrobe choice.
- Ordinary bedroom, natural window light, lived-in not styled — same environment register as
  every native creative in this account
- Handheld selfie framing, front-camera distortion, slight natural handheld movement — matches
  the authenticity read from the Kitsch teardown

**Persona reference frame (generate once, use as the visual anchor for every other prompt below):**

```
A photorealistic, high-detail portrait of a woman in her early-to-mid 30s, postpartum mom
aesthetic, soft warm skin tone, slightly tired but makeup-free, dark-to-medium brown hair worn
down and slightly undone, wearing an oversized soft grey or oatmeal sweater or robe. Seated on
the edge of a bed, natural window light from one side, ordinary bedroom background, lived-in
not styled. Handheld selfie framing, front-camera perspective, slight natural distortion.
Natural, unposed expression, not smiling for the camera. This frame locks her exact appearance,
skin tone, and hair for every other shot in this sequence — do not redesign her between clips.

Aspect ratio: 9:16 vertical, 1080x1920.
```

---

## 2. Three hook variants (swappable, each generated separately, same avatar)

**Hook 1 — Control.** The only hook with actual purchases behind it (3 converting
executions), though it's also your least efficient hook historically (CAC £88.62, 2-6x worse
CPM/CPC than challengers). Baseline worth carrying into this format.

> "I actually do my scalp oil every night now. That wasn't true six months ago."

Delivery: straight to camera, conversational, a small wry half-smile on "that wasn't true six
months ago." No prop yet. ~4-5 seconds.

**Hook 2 — Social-Compare.** Confirmed (via screenshot) the actual content of HookD from your
live hook test — cheapest CPM, most volume of any challenger, never got a fair shot at its own
conversion before that test ended. Good candidate to see if format changes its luck.

> "Every mom in my postpartum group did her nightly oil for six months straight. I made it eleven nights."

Delivery: straight to camera, self-deprecating, small eye-roll or shrug on "eleven nights." No
prop. ~5-6 seconds.

**Hook 3 — New, borrowed device.** Not previously tested. Adapts the Kitsch teardown's
cost-complaint + simultaneous-demo device (section 4 of that doc) into your own angle — still a
habit/mess complaint, no hair-outcome claim.

> "I don't even want to think about how much I've spent on scalp oil that just sat there doing nothing."

Delivery: holds up a plain oil dropper bottle while speaking, mirrors Kitsch's "show the failed
tool while complaining about it" choreography. ~5-6 seconds.

---

## 3. Shared body (generate once, reuse under all three hooks)

### Body-A — Lead + Failed Solutions (condensed)

> "I had the castor oil, I had the rosemary, I believed in the whole routine, I just couldn't keep it up. It'd end up on my hands, down my neck, soaked into a towel — easier to just skip it."

Delivery: dropper bottle near hairline/neck, a visible drip, slightly resigned expression.
~9-10 seconds at natural pace.

### Body-B — Discovery + Mechanism demo

> "Then I found this. Hollow tips, right onto your scalp, and the oil goes straight there — not on your hands."

Delivery: reveal the Ninu dispenser, part hair with one hand, press tips to scalp with the
other — same demo choreography as the Kitsch mechanism beat. ~7-8 seconds.

### Body-C — Close + Offer (compressed)

> "The habit was always there. The routine just needed to be easier than the reason to quit. Ninu Kit — forty-nine ninety-nine, thirty-day guarantee."

Delivery: back to straight-to-camera for the close line (Rule of One, FIXED, unchanged), hold
the product once more for the offer tag. ~7-8 seconds.

**Total shared body: ~24-26 seconds. Plus a hook: ~30-32 seconds total.**

---

## 4. First-frame / last-frame prompts

For each segment, generate a first frame and a last frame, then let your video tool
interpolate the motion between them. Each prompt below assumes the persona reference frame
(section 1) as the visual anchor — attach it to every generation call the same way the
product-lock reference worked in `r5-yap-video-prompts.md`.

**Continuity note:** the three hooks don't need to land on an identical last-frame pose before
cutting to Body-A — a hard jump cut between hook and body is fine and matches the authentic,
slightly rough-edged read of real UGC (the Kitsch video itself isn't a single unbroken motion,
it has natural micro-discontinuities). Don't over-engineer a seamless blend here.

### Hook 1 — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. She is mid-sentence, looking directly at the camera in
selfie framing, mouth slightly open as if beginning to speak, neutral conversational
expression, hands not yet visible or resting low out of frame. Same bedroom setting, same
natural window light.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe. A small wry half-smile, head tilted slightly, as if
just finishing a rueful sentence. Hands still low/out of frame or resting naturally, not
holding anything.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### Hook 2 — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. Mid-sentence, selfie framing, direct to camera, neutral
start-of-sentence expression. Same bedroom setting, same light.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe. A small self-deprecating eye-roll or shrug, slight
smile, as if just admitted something a little embarrassing about herself.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### Hook 3 — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. Selfie framing, one hand beginning to raise a plain glass
dropper bottle of amber oil into frame, mouth open starting to speak, slightly exasperated
expression.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe. The dropper bottle now held up clearly in frame near
shoulder height, still visible to camera, resigned/unimpressed expression, as if presenting
proof of something that didn't work.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### Body-A — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. Selfie framing, holding a plain glass dropper bottle near
her hairline, mid-sentence, slightly frustrated expression. Same bedroom setting, same light.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe. The dropper bottle now lower, near her neck/shoulder,
a visible drip of amber oil caught on her neck or soaking into a visible towel edge at her
shoulder. Resigned expression, as if this is a familiar annoyance.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### Body-B — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. Selfie framing, now holding the real Ninu dispenser
(clear cylindrical chamber, cream dome cap, five hollow clear tips in a cluster, ml markings —
match the reference renders in `r5-yap-video-prompts.md` section 0.5 exactly, do not redesign
the product), just revealed into frame near chest height.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe, same exact dispenser (five tips, cream cap, clear
chamber — unchanged). One hand parting her hair at the part, the dispenser's tip cluster
pressed flat against her scalp, visible contact point, calm focused expression.

Aspect ratio: 9:16 vertical, 1080x1920.
```

### Body-C — first/last frame

**First frame:**
```
Using the exact woman shown in the attached persona reference image — same face, hair, skin
tone, wardrobe, do not redesign her. Back to straight-to-camera selfie framing, calm and
genuine expression, hands down or resting naturally, mid-sentence beginning the closing line.

Aspect ratio: 9:16 vertical, 1080x1920.
```

**Last frame:**
```
Same woman, same setting, same wardrobe. Holding the same exact Ninu dispenser up once more
near chest height, small genuine smile, as if wrapping up naturally — not a hard sales smile,
just a settled, satisfied expression.

Aspect ratio: 9:16 vertical, 1080x1920.
```

---

## 5. Assembly

Three finished videos, each = one Hook clip + Body-A + Body-B + Body-C, same footage for the
body across all three:

- **Video 1:** Hook 1 (Control) → Body-A → Body-B → Body-C
- **Video 2:** Hook 2 (Social-Compare) → Body-A → Body-B → Body-C
- **Video 3:** Hook 3 (New, cost-complaint) → Body-A → Body-B → Body-C

Hard cuts between every segment — don't force a seamless blend, jump cuts read as authentic
here, same as the native read established across every creative in this account.

---

## 6a. Voice characteristics (locked, from user's audio sample 2026-10-26)

Measured directly from the user-generated ElevenLabs reference sample
(`voice_sample.mp3`, 18.9s, "I actually do my scalp oil every night now...").
These numbers are the voice spec; use them verbatim in every Kling prompt from here on
so the generated throwaway audio approximates the real reference, and the mouth
motion feels natural at the real pace.

- **Gender/age register:** adult female, early-to-mid 30s, American English (General American)
- **Median pitch (f0):** 197 Hz (middle of the natural adult female range)
- **Pitch range (10th-90th percentile):** 72-245 Hz — wide bottom end indicates
  intermittent vocal fry on phrase endings, characteristic of millennial-register
  conversational American English
- **Pacing:** ~184 words per minute — natural brisk-but-not-rushed conversation,
  not read-aloud slow, not performative
- **Dynamic range:** moderate (RMS std/mean 0.70) — expressive but not theatrical,
  not monotone, no stage projection
- **Phrase pauses:** natural, 400-600ms between sentences, no long dramatic beats
- **Register:** warm, slightly tired/resigned on reflection beats, dry-sincere on the
  Rule of One close line, zero announcer energy

**Compact voice description for Kling prompts (paste into every generation):**

> She speaks in an adult female American English voice, early-to-mid 30s, warm and
> slightly tired, natural brisk conversational pace around 180 words per minute, mid-pitched
> around 200 Hz with slight vocal fry on phrase endings, moderately expressive but not
> performative, no announcer energy.

**Important caveat — what this actually does:** Kling 4.0 keyframe-to-video has no audio
input field (confirmed from the API schema, section 7 above). The voice description in the
video-generation prompt mainly shapes Kling's own auto-generated throwaway audio, which still
gets muted and replaced with the user's real ElevenLabs VO (section 6 below). It can
subtly influence mouth motion naturalness/timing but does not produce lip-sync to the
ElevenLabs voice. The final deliverable's actual spoken audio always comes from the
separately-generated ElevenLabs track, not from Kling.

---

## 6. Voice/audio script (for a separate audio generator, not Kling's default voice)

Six clips, matching the six video segments exactly — same wording as sections 2 and 3, no
drift. Generate each as its own audio file, labeled to match, so pairing with the video
segments is unambiguous: `hook1.mp3`, `hook2.mp3`, `hook3.mp3`, `bodyA.mp3`, `bodyB.mp3`,
`bodyC.mp3`.

**Voice brief (for picking/describing the voice in your generator):** woman, early-to-mid 30s,
warm and natural, slightly tired register — not a polished announcer read, not an ASMR
whisper. Neutral American accent (or whatever matches your target audience), conversational
pace, talking to a phone propped up or held at arm's length, not performing for a microphone.
Small natural pauses at commas, not metronomic. If your tool supports an emotional/style
descriptor, something like "casual, slightly dry, a little wry" fits the delivery notes below
better than "upbeat" or "enthusiastic."

**Hook 1 — Control (~4-5s spoken)**
> "I actually do my scalp oil every night now. That wasn't true six months ago."

Delivery: conversational, small wry half-smile landing on "that wasn't true six months ago."

**Hook 2 — Social-Compare (~5-6s spoken)**
> "Every mom in my postpartum group did her nightly oil for six months straight. I made it eleven nights."

Delivery: self-deprecating, a small laugh or sigh right before "eleven nights," not a
triumphant delivery — she's a little embarrassed.

**Hook 3 — New, cost-complaint (~5-6s spoken)**
> "I don't even want to think about how much I've spent on scalp oil that just sat there doing nothing."

Delivery: mildly exasperated, deadpan rather than dramatic.

**Body-A — Lead + Failed Solutions (~9-10s spoken)**
> "I had the castor oil, I had the rosemary, I believed in the whole routine, I just couldn't keep it up. It'd end up on my hands, down my neck, soaked into a towel — easier to just skip it."

Delivery: resigned, a little tired, the list of oils said quickly/flatly like reciting
something familiar, slowing down on "easier to just skip it."

**Body-B — Discovery + Mechanism (~7-8s spoken)**
> "Then I found this. Hollow tips, right onto your scalp, and the oil goes straight there — not on your hands."

Delivery: a genuine shift in energy here, mild relief/satisfaction, slightly slower and more
deliberate than Body-A.

**Body-C — Close + Offer (~7-8s spoken)**
> "The habit was always there. The routine just needed to be easier than the reason to quit. Ninu Kit — forty-nine ninety-nine, thirty-day guarantee."

Delivery: the first sentence (Rule of One) said plainly and sincerely, almost like a thought
rather than a tagline. The offer tag at the end picks up pace slightly — quick, matter-of-fact,
not a hard sell.

**On timing:** these are natural-pace estimates, not hard targets. Once you have the audio
back, check each clip's actual length against its paired video segment's generated duration —
small mismatches (a second or two) are normal and fixable by slightly trimming silence at the
start/end; a large mismatch means the video generation's duration should be adjusted to match
before pairing them.

---

## 7. kie.ai / Kling 4.0 keyframe-to-video — confirmed API shape

Confirmed directly from the kie.ai Playground UI (2026-10-26), correcting an earlier
assumption:

- `first_frame_url` and `last_frame_url` are **separate, single-image fields** —
  `keyframe_urls` is only for up to 8 *additional middle* frames beyond the first/last pair.
  We don't need `keyframe_urls` at all for simple first+last interpolation.
- `prompt` (required, up to 8000 chars) expects a **detailed, timestamped shot description**
  referencing `@first_frame` and `@last_frame` directly in the prose (e.g. "0-3s, PICKUP:
  Begin exactly on @first_frame..."), not a short one-line description.
- `duration`: numeric seconds, 3-30 range.
- `resolution`: `720P` or `1080P` — using 720P per the cost-efficiency reasoning above.
- `aspect_ratio`: defaults to `Auto` — should infer 9:16 correctly from our source images,
  which are already generated at 1080x1920.
- No audio input field exists anywhere in the schema. **This means Kling generates its own
  mouth movement/talking motion with no way to lip-sync to a separately-produced custom
  voiceover.** Swapping in your own VO (section 6) will not be word-perfect synced to the
  generated mouth movement. Worth treating the Hook 1 + Body A sample specifically as a check
  on how noticeable that mismatch is before committing further spend to this format — a raw
  handheld-selfie read tolerates looseness better than a polished talking-head shot would, but
  it's a real limitation, not a solved one.
- Error handling: kie.ai returns errors as **HTTP 200 with an error `code` in the body**, not
  a 4xx status — check `code`, not just the HTTP status.
- Status polling: `GET /api/v1/jobs/recordInfo?taskId=...`.
- Generated media is deleted after 14 days — download and archive results promptly (into the
  Ninu UGC resources Drive folder).

### Hook 1 — Control — video generation prompt

`duration: 5`, `resolution: 720P`, `aspect_ratio: Auto`

**Attach:** `hook1-first-frame.png` as `first_frame_url`, `hook1-last-frame.png` as `last_frame_url`

> 0-5s, HOOK CONTROL: Begin exactly on @first_frame — adult woman in selfie framing, early-to-mid
> 30s, postpartum mom aesthetic, soft warm skin tone, slightly tired makeup-free face, wearing an
> oversized soft grey oatmeal sweater, dark-to-medium brown hair worn loose. Ordinary bedroom
> background, natural window light. Handheld selfie framing with slight natural camera sway.
>
> She speaks the following line to camera in a natural, slightly dry, conversational register —
> adult female American English (General American accent), early-to-mid 30s voice, warm but
> slightly tired, natural brisk conversational pace around 180 words per minute, mid-pitched
> around 200 Hz with slight vocal fry on phrase endings, moderately expressive but not
> performative, no announcer energy. Mouth movement must shape the English words naturally —
> English visemes only, do not speak Chinese or any other language.
>
> Spoken line (verbatim, English): "I actually do my scalp oil every night now. That wasn't
> true six months ago."
>
> Delivery direction: conversational, with a small wry half-smile landing on "that wasn't true
> six months ago." Short natural pause between the two sentences. Hands stay low or out of frame
> throughout. Transition smoothly by the end into @last_frame — the small wry half-smile, head
> tilted slightly, as if just finishing a rueful sentence.
>
> Same woman, same wardrobe, same bedroom setting throughout — no identity drift, no change in
> appearance or background.

### Hook 2 — Social-Compare — video generation prompt

`duration: 5`, `resolution: 720P`, `aspect_ratio: Auto`

**Attach:** `hook2-first-frame.png` as `first_frame_url`, `hook2-last-frame.png` as `last_frame_url`

> 0-5s, HOOK SOCIAL-COMPARE: Begin exactly on @first_frame — adult woman in selfie framing,
> early-to-mid 30s, postpartum mom aesthetic, soft warm skin tone, slightly tired makeup-free
> face, wearing an oversized soft grey oatmeal sweater, dark-to-medium brown hair worn loose.
> Ordinary bedroom background, natural window light. Handheld selfie framing with slight natural
> camera sway.
>
> She speaks the following line to camera in a natural, self-deprecating, conversational
> register — adult female American English (General American accent), early-to-mid 30s voice,
> warm but slightly tired, natural brisk conversational pace around 180 words per minute,
> mid-pitched around 200 Hz with slight vocal fry on phrase endings, moderately expressive but
> not performative, no announcer energy. Mouth movement must shape the English words naturally —
> English visemes only, do not speak Chinese or any other language.
>
> Spoken line (verbatim, English): "Every mom in my postpartum group did her nightly oil for six
> months straight. I made it eleven nights."
>
> Delivery direction: self-deprecating, a small laugh or sigh landing right before "eleven
> nights" — she's a little embarrassed, not triumphant. Small natural pause between the two
> sentences. Hands stay low or out of frame throughout. Transition smoothly by the end into
> @last_frame — the small self-deprecating eye-roll or shrug with slight smile, as if just
> admitted something a little embarrassing about herself.
>
> Same woman, same wardrobe, same bedroom setting throughout — no identity drift.

### Hook 3 — Cost-Complaint — video generation prompt

`duration: 5`, `resolution: 720P`, `aspect_ratio: Auto`

**Attach:** `hook3-first-frame.png` as `first_frame_url`, `hook3-last-frame.png` as `last_frame_url`

> 0-5s, HOOK COST-COMPLAINT: Begin exactly on @first_frame — adult woman in selfie framing,
> early-to-mid 30s, postpartum mom aesthetic, soft warm skin tone, slightly tired makeup-free
> face, wearing an oversized soft grey oatmeal sweater, dark-to-medium brown hair worn loose.
> Ordinary bedroom background, natural window light. Handheld selfie framing with slight
> natural camera sway. She is holding a plain glass dropper bottle of amber oil in one hand,
> raised into frame at shoulder height.
>
> She speaks the following line to camera in a mildly exasperated, deadpan conversational
> register — adult female American English (General American accent), early-to-mid 30s voice,
> warm but slightly tired, natural brisk conversational pace around 180 words per minute,
> mid-pitched around 200 Hz with slight vocal fry on phrase endings, moderately expressive but
> not performative, no announcer energy. Mouth movement must shape the English words naturally —
> English visemes only, do not speak Chinese or any other language.
>
> Spoken line (verbatim, English): "I don't even want to think about how much I've spent on
> scalp oil that just sat there doing nothing."
>
> Delivery direction: mildly exasperated and deadpan, not dramatic. The dropper bottle is a
> visible proof-prop — she presents it near her face while speaking. Small natural emphasis on
> "just sat there doing nothing" with a slight resigned shrug. Transition smoothly by the end
> into @last_frame — the dropper bottle held up clearly in frame near shoulder height, still
> visible to camera, resigned/unimpressed expression as if presenting proof of something that
> didn't work.
>
> Same woman, same wardrobe, same bedroom setting throughout — no identity drift.

### Body A — video generation prompt

`duration: 10`, `resolution: 720P`, `aspect_ratio: Auto`

> 0-10s, FAILED SOLUTIONS: Begin exactly on @first_frame — woman in selfie framing, holding a
> plain glass dropper bottle near her hairline, mid-sentence, slightly frustrated expression,
> mouth moving naturally as if speaking casually **in English (American English)**. Handheld
> camera, slight natural sway. Over the course of the clip she slowly lowers the dropper bottle
> from her hairline down toward her neck and shoulder, continuous natural hand motion,
> expression gradually shifting toward mild resignation. Transition smoothly by the end into
> @last_frame — the dropper bottle now lower near her neck/shoulder, a visible drip of amber
> oil on her neck or soaking into a towel edge at her shoulder, resigned expression. Same
> woman, same wardrobe, same bedroom setting throughout — no identity drift.

Body B and Body C will follow the same enhanced format (visual direction + spoken line +
voice spec + delivery) once the hook round is done, so the full script from section 6 ends up
baked into every clip's prompt rather than left on the side.

### Sample round result (2026-10-26): Hook 1 + Body A — both succeeded on the 2nd attempt

**Real issue hit and fixed:** the images as pasted into chat come through as `.webp`. Kling
4.0 keyframe-to-video rejects this outright: `"Unsupported file format. Images must be JPG or
PNG."` — both first-attempt jobs failed cleanly at `creditsConsumed: 0.0`, no money lost, but
this needs fixing before every future round, not just worked around once: **convert every
image to PNG or JPG before uploading**, regardless of source format.

**Image hosting:** kie.ai needs a real public URL for `first_frame_url`/`last_frame_url` — the
Artifact asset store and a Drive share link both turned out to require auth a third-party
server can't provide. The working path is kie.ai's own upload endpoint:
`POST https://kieai.redpandaai.co/api/file-base64-upload` with
`{"base64Data": "data:image/png;base64,<...>", "uploadPath": "...", "fileName": "..."}` →
returns `data.downloadUrl`, confirmed publicly fetchable. (Note the host —
`kieai.redpandaai.co`, not `api.kie.ai`; the latter 404s for uploads, the jobs API stays on
`api.kie.ai`.)

**Image-to-prompt mapping was not upload order.** The 5 pasted images had to be matched to
their intended role by content (expression, prop position), not by the sequence they arrived
in — confirmed by checking which frame matched each prompt's described expression/prop state
before spending anything. Worth double-checking this every round, not assuming a fixed order.

**Results:**

| Segment | Duration | Credits | Cost | State |
|---|---|---|---|---|
| Hook 1 | 5s | 142.5 | $0.71 | success |
| Body A | 10s | 285 | $1.43 | success |

**QA (frame-sampled, not just trusted on "success"):** both clips land cleanly on their
intended last frame — Hook 1 ends on the wry half-smile, Body A ends with the dropper lowered
and oil visibly dripping onto the towel. Consistent identity and wardrobe throughout, no
visible warping or product/prop distortion, natural handheld camera motion.

**Confirmed limitation:** both clips came back with their own AAC audio track — Kling
generates native audio/dialogue even with no audio input supplied. This needs to be muted
before the custom VO (section 6) goes on; there's no lip-sync between the two.

**Delivery:** sent directly to the user as files rather than pushed into Drive — the available
Drive upload tool only accepts inline base64 content as a tool parameter with no file-path
option, which isn't practical for multi-MB video. Clips need to be manually dragged into the
Ninu UGC resources Drive folder.

**Second bug found and fixed on this round: wrong spoken language.** Neither prompt specified
a language for the "speaking naturally" instruction, and Kling (a Kuaishou/Chinese model)
defaulted to Mandarin for its native generated audio. This isn't just a muted-track cosmetic
issue — the mouth shapes/visemes the video generates are shaped by whatever language it thinks
is being spoken, so Mandarin-shaped mouth movement would mismatch an English VO worse than
English-shaped movement would. **Fix: every prompt must explicitly state "speaking casually in
English (American English)"** — now added to both prompts above. Verified the fix actually
worked by running the regenerated audio through Whisper's language detector (both now read
`en`), not just trusting the clip looked right. Both segments regenerated: same cost again
($0.71 + $1.43 = $2.14), same quality/identity/landing-frame accuracy as the first pass.
**Apply this language lock to the Hook 2/3 and Body B/C prompts before generating them —
don't repeat this on the next 4 segments.**

## 8. Test setup

Single-variable test (hook only, per the Master Doc's Variation Winners rule) — launch all
three as separate ads in one new ad set, small test budget, same checkpoint structure as
everything else in this account: £10.77 (0 link clicks) / £21.54 (0 ATC) / £32.31 (0 IC) /
£53.85 (0 purchases, hard stop), per ad. Keep this test budget separate from the £85 proven
pool and the HookD retest.
