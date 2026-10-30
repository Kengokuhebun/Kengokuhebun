# R9b: 3D cartoon ad, sung slowly: scene-by-scene breakdown

Built from the Ad C long form (`ninu-r1-long-form.md`), the winning story, sung as a slow lullaby over a
3D cartoon animation. Every lyric line is verbatim from Ad C except numbers, which are spelled out so the
singer pronounces them (marked with "sung as").

I can only see the Ad Maker input screen, not what it does after you press Start, so where I mention
how the tool behaves I say "if". Everything else is tool-independent.

## 0. Ad Maker settings (from your screenshot)

| Field | Set it to | Why |
|---|---|---|
| **Brand** | **Not RYZE Superfoods.** Create "Ninu": cream #F5EFE6, espresso #241812, gold #C79A5A, wordmark "N I N U" | RYZE is another company's brand and is the default. Pressing Start as is would use its identity. |
| **Product** | Add product: the dispenser. Upload your white-background master image (and the kit flat-lay if it takes more than one). Name "Ninu Scalp Oil Dispenser" | So the tool draws your real product, not a generic bottle. |
| **Style** | 3D cartoon (already set) | Matches this plan. |
| **Model** | Seedance 2.5 (already set) | Keep as is. |
| **Ratio / quality** | 9:16, 720p for the test | Re-export higher only for a winner. |
| **Song** | Attach the sung track (section 3) | The song is the timeline. Generate it first if the tool doesn't write sung audio itself. |
| **Choose when to check** | If it offers a review before generating video, take it | Cheapest place to catch a wrong brand, product or script. |

## 1. Runtime math (read before you paste anything)

Slow singing runs about 1.75 words per second plus a breath between phrases. That sets the length:

| Cut | Scenes | Words | Runtime |
|---|---|---|---|
| **Core (recommended)** | 1, 2, 5, 7, 8, 9, 11, 12 | 107 | about 1:10 |
| **Full** | all 12 | 166 | about 1:48 |
| Whole long form | n/a | 410 | about 4 minutes, not viable |

The core cut keeps the hook, the Sunday loop, the discovery, the mechanism, the "oh", the close line and the
offer. The four add-back scenes (3, 4, 6, 10) are the lead, the wet hands, the chore line and the week-one
proof. Each is self-contained, so you can add any of them back.

## 2. Paste blocks for the "Paste the script" box

**Core cut (about 1:10):**

```
Scene 1
I actually do my scalp oil every night now.

Scene 2
That wasn't true six months ago.

Scene 5
I'd tell myself I'd start over Sunday.
I never started over Sunday.

Scene 7
Then I found a dispenser with hollow silicone tips.

Scene 8
You press the tips against the scalp,
and the oil releases right there,
directly on the skin.

Scene 9
The first night I used it I thought: oh.
This is what it's supposed to feel like.

Scene 11
The habit was always there.
The routine just needed to be easier than the reason to quit.

Scene 12
The Nee-noo Kit is forty-nine ninety-nine,
with free U.S. shipping and a thirty-day money-back guarantee.
Make tonight the easy one.
```

**Full cut (about 1:48):** the same, with these inserted in order:

```
Scene 3 (after Scene 2)
I had the castor oil. I had the rosemary.
I just couldn't make myself do it consistently.

Scene 4 (after Scene 3)
I'd get into bed with wet hands and just not do it.

Scene 6 (after Scene 5)
A chore at ten p.m. after a full day with a baby
is a chore that gets skipped.

Scene 10 (after Scene 9)
By the end of the first week I hadn't skipped a night.
```

If the tool ignores scene labels, delete the "Scene N" lines and keep the blank lines between blocks.
"Nee-noo" is my guess at how you say the brand. Change the spelling to match your pronunciation, and check
it in the generated song, because Kling already mispronounced it once.

## 3. The song (generate this first)

**Style prompt:**

```
Slow lullaby ballad, 60 BPM, 6/8 feel. One intimate female vocal, warm and slightly breathy, close-mic'd,
tired but tender in the verses, warmer and fuller in the chorus. Music box and felt piano, warm nylon guitar,
a soft string pad that only enters on the line "oh" and swells in the chorus. No drums, no percussion, no
electronic sounds, no autotune, no choir. Sparse arrangement with a lot of space between phrases. Clear
diction, English. Start singing within one second, no instrumental intro. Gentle resolved ending.
```

**Lyrics with structure tags** (core cut; add the add-back lines in the same positions as section 2):

```
[Verse 1]
I actually do my scalp oil every night now.
That wasn't true six months ago.
I'd tell myself I'd start over Sunday.
I never started over Sunday.

[Verse 2]
Then I found a dispenser with hollow silicone tips.
You press the tips against the scalp,
and the oil releases right there,
directly on the skin.

[Bridge]
The first night I used it I thought: oh.
This is what it's supposed to feel like.

[Chorus]
The habit was always there.
The routine just needed to be easier than the reason to quit.

[Outro, softly spoken-sung]
The Nee-noo Kit is forty-nine ninety-nine,
with free U.S. shipping and a thirty-day money-back guarantee.
Make tonight the easy one.
```

Notes:
- Listen for "Nee-noo", "forty-nine ninety-nine" and "thirty-day" before using the take.
- A sung price can sound clumsy. If it does, end the song on "Make tonight the easy one" and put the price and
  guarantee in the end card and the ad's primary text instead.
- Once you have a take, set each scene's length to its real phrase timestamps. The times below are estimates.

## 4. Style lock (paste the first block into every scene prompt)

**Style:**
```
3D cartoon, soft Pixar-style animation, rounded friendly shapes, tactile materials (linen, satin, glass),
shallow depth of field, gentle film-like lighting, vertical 9:16. No text, no letters, no logos, no subtitles,
no baby visible, no extra fingers, no duplicate characters.
```

**Character (Maya):** 32, soft wavy shoulder-length brown hair with a center part, round friendly face, large
expressive eyes, warm medium skin tone, same casting as the PDP slide 02 woman. **Costume follows story time:**
- **The past, through her first night (Scenes 2-10):** oatmeal cardigan. In the oily "before" scenes (2, 3, 4, 6)
  add a towel over her shoulders, slightly messy hair and dark under-eye shadows. From Scene 7 on the towel is gone.
- **The present (Scenes 1 and 11):** tan robe, caramel satin bonnet, neat hair, relaxed shoulders.

If the tool lets you attach a character image, make one sheet (front, three-quarter, profile, three expressions)
and attach it.

**World:**
- Bedroom: cream linen bed, nightstand with a small lamp, a white baby monitor with one LED, a digital clock, a
  window with night sky.
- Bathroom: a wooden shelf with a few plain bottles, a mirror, a paper wall calendar above the shelf.
- Palette: cream #F5EFE6, espresso #241812, gold #C79A5A.

**Two looks, the grade shift is the story:**
- **Before:** cool moonlit blue, 40% desaturated, lamp off or dim, soft shadows.
- **After:** warm amber lamp glow, fully saturated, soft golden bloom.

**Product (match your master image exactly):** a palm-sized cylinder with a cream dome cap, a clear reservoir of
golden oil with fine measurement marks, and a row of hollow translucent silicone tips at the base. Count the
tips on your master image and write that number into every product prompt (the hero image shows about five).
Video models drift small details, so keep product close-ups short and re-roll any clip where the tip count or
cap shape changes.

## 5. Scene-by-scene

Times are estimates (core cut first, full cut in brackets).

### Scene 1 · Hook, the "now" · 0:00-0:06 · core
- **Lyric:** "I actually do my scalp oil every night now."
- **Beat:** quiet pride. The viewer should instantly read "this woman has her routine".
- **Set and light:** bedroom, warm amber lamp, cream linen, the clock reading 10:00 PM, baby monitor LED steady green. After look.
- **Maya:** cross-legged on the bed in the tan robe and caramel bonnet, shoulders low, soft closed-mouth smile, the dispenser resting upright on her knee.
- **Action:** 0-2s she looks down at the dispenser fondly; 2-4s she looks up to camera; 4-6s a slow exhale and a tiny nod, as if confirming it is true.
- **Camera:** medium close-up, eye level, locked off with a 3% slow push-in. Lamp bokeh in the background.
- **Animation notes:** slight breathing in the shoulders, a soft sway of the bonnet fabric, the dispenser catches a small gold highlight.
- **Audio:** the first note lands at about 0:00.4. Music box and soft piano only, voice warm and close.
- **Caption:** the lyric, word by word from frame 1 (most people watch muted).
- **Cut out:** hard cut on the last held note.
- **Seedance prompt:** `[Style] A calm 3D cartoon woman, brown wavy hair, caramel satin bonnet, tan robe, sits cross-legged on a cream linen bed at night holding a small cream-capped oil dispenser on her knee, warm amber lamp glow, she glances down at it, looks up to camera and gives a small satisfied nod, medium close-up, locked camera with a very slow push-in, shallow depth of field, cozy and proud mood.`
- **Watch for:** dispenser shape drifting, fingers merging with the product, the bonnet melting into her hair.

### Scene 2 · Hook, "six months ago" · 0:06-0:11 · core
- **Lyric:** "That wasn't true six months ago."
- **Beat:** the same woman, the same framing, drained. The contrast is the hook.
- **Set and light:** same room and same camera position, now cool moonlit blue, lamp off, 40% desaturated. Bed rumpled, an uncapped dropper bottle on the nightstand, the monitor LED amber, the clock showing 11:42 PM.
- **Maya:** same pose, but messy hair, oatmeal cardigan, a towel over her shoulders, no bonnet, dark under-eye shadows, glossy oily fingertips.
- **Action:** slow heavy blink; her gaze drifts down to her hands; she stares at her wet fingers without moving.
- **Camera:** identical framing to Scene 1 so the cut reads as a match cut; 3% push-in.
- **Animation notes:** very little motion; only breathing and one blink. Stillness sells exhaustion.
- **Audio:** same voice, quieter and lower. The music drops to single piano notes and a faint reverb tail.
- **Caption:** the lyric.
- **Cut out:** hard cut on the downbeat of the next phrase.
- **Seedance prompt:** `[Style] The same 3D cartoon woman, now exhausted, messy brown hair, oatmeal cardigan, a towel over her shoulders, sits in the same pose on a rumpled bed at night, cool blue moonlight, lamp off, an open dropper bottle on the nightstand, she slowly blinks and looks down at her glossy oily fingers, medium close-up, locked camera with a slight push-in, desaturated, heavy and tired mood.`
- **Watch for:** the character looking like a different person. Re-roll until the face matches Scene 1.

### Scene 3 · The lead · full cut only [0:11-0:22]
- **Lyric:** "I had the castor oil. I had the rosemary. I just couldn't make myself do it consistently."
- **Beat:** she had everything and good intentions. This is the avatar's awareness.
- **Set and light:** the bathroom, cool blue, a wooden shelf. Front row: a dark amber bottle with a plain cream label and a green glass bottle with a rosemary sprig tied to its neck (no readable words).
- **Maya:** oatmeal cardigan, towel on shoulders.
- **Action:** 0-4s the camera slides along the shelf and a soft warm highlight touches each bottle as it is named; 4-8s Maya stands at the sink and reaches for the amber bottle; 8-11s her hand hovers over it, hesitates, and slowly lowers.
- **Camera:** lateral slide along the shelf, then a medium shot of Maya at the sink with a reflection in the mirror.
- **Animation notes:** liquid sways in the bottles, the rosemary sprig has a small secondary swing.
- **Audio:** the voice stays low and weary. A single sustained note on "consistently".
- **Caption:** the lyric.
- **Seedance prompt:** `[Style] A wooden bathroom shelf in cool blue light, a dark amber glass bottle and a green glass bottle with a rosemary sprig, the camera slides slowly along the shelf, then a tired 3D cartoon woman in an oatmeal cardigan reaches toward the amber bottle, hesitates and lowers her hand, soft desaturated look, medium shot.`
- **Watch for:** invented label text. Add "blank labels" if words appear.

### Scene 4 · The wet hands · full cut only [0:22-0:30]
- **Lyric:** "I'd get into bed with wet hands and just not do it."
- **Beat:** the nightly surrender.
- **Set and light:** bedroom, cool blue, the monitor on the nightstand.
- **Maya:** oatmeal cardigan, towel on shoulders, glossy oily hands held away from the sheets.
- **Action:** 0-3s she sits on the bed edge, hands held out in front of her, looks at the clean pillow; 3-5s she wipes her hands on the towel on her shoulders; 5-8s she lies down on her side facing away. The monitor's LED blinks three times.
- **Camera:** medium shot, slow push toward the hands, then a short pan to the monitor on the last beat.
- **Animation notes:** oil sheen on the fingers, the towel wrinkles, the three monitor blips are the only bright thing in the frame.
- **Audio:** three soft monitor blips between phrases (carries "baby up three times" without a lyric).
- **Caption:** the lyric.
- **Seedance prompt:** `[Style] A tired 3D cartoon woman in an oatmeal cardigan with a towel on her shoulders sits on a bed edge holding glossy oily hands away from clean sheets, wipes them on the towel, then lies down on her side facing away, a baby monitor on the nightstand blinks three times, cool blue night light, medium shot with a slow push-in.`
- **Watch for:** hands. Keep the action to one slow gesture; re-roll on extra fingers.

### Scene 5 · The Sunday loop · 0:11-0:19 · core [0:30-0:38]
- **Lyric:** "I'd tell myself I'd start over Sunday. I never started over Sunday."
- **Beat:** the callback. Say it once, then let it land in silence.
- **Set and light:** one frame with the paper wall calendar on top and the bathroom shelf below it. Cool blue. An amber bottle sits at the front of the shelf.
- **Maya:** not on screen (her absence is the point).
- **Action:** 0-2s a gold marker draws a circle around "SUN" on this week; 2-3s the page flips to the next week and the bottle slides backward on the shelf; 3-5s "SUN" is circled again, no tick, the bottle slides back again; 5-8s the third week flips and "SUN" is bare, the bottle now hidden behind other products. A 0.8s pause with no vocal after the last word.
- **Camera:** locked-off, then a slow rack focus from the calendar down to the shelf.
- **Animation notes:** the circle draws on with a hand-drawn wobble; each bottle slide has a small stop-motion feel.
- **Audio:** the page-flips are soft sound effects on the beat. Let the final "Sunday" ring, then silence for a beat before the next scene.
- **Caption:** the lyric. Highlight "Sunday" in gold both times.
- **Seedance prompt:** `[Style] A paper wall calendar above a wooden bathroom shelf in cool blue light, a gold marker draws a circle around the Sunday square, the page flips to the next week while a small amber bottle slides backward on the shelf, a circle is drawn again with no tick, the page flips once more and the bottle is now hidden behind other bottles, static frame with a slow rack focus from calendar to shelf. No readable text on bottles.`
- **Watch for:** calendar text turning to gibberish. Ask for "blank grid with a single circled column" if it does. Overlay "SUN" in the edit if needed.

### Scene 6 · The chore · full cut only [0:38-0:49]
- **Lyric:** "A chore at ten p.m. after a full day with a baby is a chore that gets skipped." (printed as "10pm")
- **Beat:** the old method, the mess, the dread.
- **Set and light:** bathroom counter, cool blue, a digital clock reading 10:04 PM.
- **Maya:** oatmeal cardigan, towel over her shoulders, shoulders slumped.
- **Action:** 0-4s macro: oil droplets fall from a dropper onto her hair, run down the strands and down her neck into the towel; 4-8s she sets the dropper down and rests her forehead on her hand; 8-11s the clock turns from 10:04 to 10:05 as she stares at it.
- **Camera:** macro on the droplets, then a pull-back to a medium close-up of her tired face.
- **Animation notes:** viscous slow oil, a visible streak on her neck, the towel darkening.
- **Audio:** the lowest, quietest line of the song. A slow clock tick under the voice.
- **Caption:** the lyric, with "10pm" printed as numerals.
- **Seedance prompt:** `[Style] Close-up of golden oil dripping from a glass dropper onto brown hair and running down a neck into a towel, then pull back to a tired 3D cartoon woman who sets the dropper down and rests her forehead on her hand, a digital clock showing 10:04 PM beside her, cool blue light, slow and heavy mood.`
- **Watch for:** the dropper looking like your product. It must look like a plain glass dropper, never like the Ninu dispenser.

### Scene 7 · The discovery · 0:19-0:25 · core [0:49-0:55]
- **Lyric:** "Then I found a dispenser with hollow silicone tips."
- **Beat:** hope. The grade begins to warm.
- **Set and light:** bedroom, the lamp clicks on and the blue starts to turn amber.
- **Maya:** still in the oatmeal cardigan, the towel now off her shoulders, a tiny spark of curiosity.
- **Action:** 0-2s a plain cream box sits on the bed and she lifts the lid; 2-4s she lifts out the dispenser and the tips catch the light; 4-6s macro on the hollow translucent tips with a soft gold glint.
- **Camera:** medium shot, then a push-in to a macro of the tips.
- **Animation notes:** the lid lifts with a satin ease; a small warm glow builds around the tips.
- **Audio:** the music box enters brighter, one added high note on "tips".
- **Caption:** the lyric. No text on the box (the model will garble it).
- **Cut out:** hard cut.
- **Seedance prompt:** `[Style] A 3D cartoon woman on a cream bed opens a plain cream box and lifts out a small oil dispenser with a cream dome cap, a clear reservoir of golden oil and a row of hollow translucent silicone tips at the base, a warm lamp turns on and the room shifts from cool blue to amber, push-in to a macro of the tips catching the light. Match the attached product image exactly.`
- **Watch for:** the product. Check the tip count and cap against the master before you accept the clip.

### Scene 8 · The mechanism · 0:25-0:36 · core [0:55-1:06]
- **Lyric:** "You press the tips against the scalp, and the oil releases right there, directly on the skin."
- **Beat:** the belief shift. This is the proof scene.
- **Set and light:** warm amber bedroom, plus a stylized cutaway.
- **Maya:** oatmeal cardigan (this is her first use, so no bonnet yet), no towel, hair neat.
- **Action (three cuts):** (a) 0-3s she parts her hair down the center with her free hand; (b) 3-8s stylized 3D cross-section: soft cylindrical hair strands, a clean part line, the dispenser's tips lower between the strands and touch the skin, a golden droplet releases and spreads across the skin with a soft glow; (c) 8-11s back to live, she presses the dispenser along the part with one hand, and her shoulders and the sheets stay clean and dry.
- **Camera:** medium, then a side-on macro for the cutaway, then medium.
- **Animation notes:** the oil is slow and honey-like; the glow on the skin is the focal point.
- **Audio:** a gentle swell on "right there", a soft "click" sound when the tips meet the scalp.
- **Caption:** the lyric. Add a small gold tag "hollow silicone tips" in the edit.
- **Seedance prompts:** generate (b) separately so it can't be muddled with live action.
  - (a)+(c): `[Style] A 3D cartoon woman in an oatmeal cardigan parts her brown hair down the center, then presses a small cream-capped oil dispenser along the part with one hand, warm amber lamp light, no oil on her shoulders or sheets, medium shot, calm and satisfied mood.`
  - (b): `[Style] Stylized 3D cross-section of a scalp: soft cylindrical hair strands, a clean center part, a cream-capped dispenser lowers so its hollow translucent silicone tips pass between the strands and touch the skin, a golden droplet releases and spreads across the skin with a soft glow, side-on macro, warm lighting, no text.`
- **Watch for:** the cutaway turning anatomical or gory. Keep it soft, stylized and cartoonish.

### Scene 9 · The "oh" · 0:36-0:47 · core [1:06-1:17]
- **Lyric:** "The first night I used it I thought: oh. This is what it's supposed to feel like."
- **Beat:** relief. The emotional peak of the ad.
- **Set and light:** bedroom, starting cool and shifting fully to warm amber on the word "oh".
- **Maya:** oatmeal cardigan for the whole scene, no towel. Only the light changes, not the costume.
- **Action:** 0-4s she sits on the bed edge and presses the dispenser along her part, eyes closed; 4-6s on "oh" her shoulders drop and her eyes open with a small, genuine surprise; 6-11s a soft smile, she rests the dispenser in her lap and exhales.
- **Camera:** medium close-up, slow 5% push-in, shallow depth of field.
- **Animation notes:** the light change is the shot. Lamp bloom, warm rim light on her hair, the room's blue draining to amber.
- **Audio:** the string pad enters on "oh", the vocal holds the note slightly longer.
- **Caption:** the lyric, with "oh" large.
- **Seedance prompt:** `[Style] A 3D cartoon woman in an oatmeal cardigan sits on a bed edge pressing a small cream-capped dispenser along her hair part with her eyes closed, then her shoulders drop and she opens her eyes with gentle surprise and a soft smile, the room light shifts from cool blue to warm amber, medium close-up, slow push-in, shallow depth of field, tender and relieved mood.`
- **Watch for:** the expression. Aim for relief, not a big grin.

### Scene 10 · The week · full cut only [1:17-1:25]
- **Lyric:** "By the end of the first week I hadn't skipped a night."
- **Beat:** the payoff of the Sunday loop in Scene 5.
- **Set and light:** the same calendar-and-shelf frame as Scene 5, now warm amber.
- **Maya:** not on screen.
- **Action:** 0-6s seven soft gold ticks pop onto seven squares one by one, and with each tick the amber bottle slides a little forward on the shelf until it is at the front; 6-8s the earlier circled Sundays are gone.
- **Camera:** locked-off, identical framing to Scene 5 so the viewer feels the reversal.
- **Animation notes:** each tick has a tiny squash-and-stretch pop; the bottle slides forward with a reverse of Scene 5's easing.
- **Audio:** a soft "ting" per tick, the page flip sound reversed.
- **Caption:** the lyric.
- **Seedance prompt:** `[Style] The same paper wall calendar above a wooden shelf, now in warm amber light, seven small gold check marks pop onto seven squares one by one while an amber bottle slides forward to the front of the shelf, static frame, satisfying and bright.`
- **Watch for:** the tick count. If the model draws the wrong number, overlay ticks in the edit.

### Scene 11 · The close (chorus) · 0:47-0:58 · core [1:25-1:36]
- **Lyric:** "The habit was always there. The routine just needed to be easier than the reason to quit."
- **Beat:** the big idea. This is the chorus, so it should feel like an exhale.
- **Set and light:** warm amber bedroom, wide shot of the nightstand: the dispenser standing upright beside the satin bonnet, the baby monitor LED steady green and quiet, the clock reading 10:00 PM.
- **Maya:** tan robe, bonnet. Her hand enters the frame and picks up the dispenser without her looking, as automatically as reaching for a toothbrush; the camera pulls back to show her already settled on the bed with a faint smile.
- **Action:** 0-4s still life of the nightstand; 4-8s her hand takes the dispenser; 8-11s pull back to the full room.
- **Camera:** locked-off wide, then a slow pull-back.
- **Animation notes:** dust motes in the lamp light, a very slight sway of the bonnet fabric.
- **Audio:** the warmest, fullest moment: strings pad, piano, voice at its most open.
- **Caption:** the lyric, line by line.
- **Seedance prompt:** `[Style] Wide shot of a nightstand in warm amber lamp light, a small cream-capped oil dispenser standing upright beside a folded caramel satin bonnet and a quiet baby monitor, a clock reading 10:00 PM, a woman's hand in a tan robe sleeve reaches in and picks up the dispenser without looking, camera slowly pulls back to reveal her relaxed on the bed with a faint smile, peaceful and resolved mood.`

### Scene 12 · Offer and CTA · 0:58-1:10 · core [1:36-1:48]
- **Lyric:** "The Nee-noo Kit is forty-nine ninety-nine, with free U.S. shipping and a thirty-day money-back guarantee. Make tonight the easy one."
- **Beat:** a calm, clear offer, then the last emotional line.
- **Set and light:** a clean cream background with a thin gold line, a soft warm light sweep.
- **Maya:** not on screen.
- **Action:** 0-5s three items float in and settle: the dispenser in the center, a 60ml amber oil bottle on the left, a folded caramel satin bonnet on the right; 5-9s a gentle light sweep across them; 9-12s the end card holds with the last line.
- **Camera:** slow push-in on the still life.
- **Animation notes:** objects land with a soft ease and a tiny bounce.
- **Audio:** the outro, quieter and more spoken-sung. A soft resolving chord on "easy one".
- **Caption and end card (add in the edit, not in the video model):** wordmark "N I N U", "The Ninu Kit · $49.99", "Free US shipping · 30-day money-back guarantee", "tryninu.store". **No** ebook, no bundle, no discount line.
- **Seedance prompt:** `[Style] On a clean cream background with a thin gold line, a small cream-capped oil dispenser, a 60ml amber glass oil bottle and a folded caramel satin bonnet float in and settle in a neat arrangement, a soft warm light sweeps across them, slow push-in, calm and premium. No text.`
- **Watch for:** any generated text on the bottle or background. Prices and logos always go in the edit.

## 6. Captions

Sung lyrics are hard to follow muted, so captions carry the first seconds. Burn them in from frame 1: bold white, dark outline, lower-middle of the frame (roughly 55-72% of the height, clear of Meta's top and bottom UI zones), two to four words highlighted at a time, "Sunday" and "oh" in gold.

## 7. Edit and QC checklist

- [ ] Hard cuts on phrase boundaries, no crossfades or wipes.
- [ ] Same face in every Maya scene (re-roll until it matches Scene 1).
- [ ] Dispenser matches the master image in every shot: cap, reservoir, tip count.
- [ ] No generated text anywhere. Price, logo and "SUN" are overlays.
- [ ] The song says "Nee-noo" (or your pronunciation), "forty-nine ninety-nine", "thirty-day".
- [ ] No baby on screen, no ebook, no Buy 2 Get 1 Free, no Black Friday.
- [ ] Export 9:16 at 720p for the test.

## 8. Ad setup

Primary text, headline and description: the original Ad C text, unchanged, so format is the variable. Same
checkpoints as `ninu-kill-criteria.md` section 3.

## 9. Gate before you spend

Orders have been zero since Oct 26 on about 450 non-junk sessions, and only 0-1 sessions a day reach checkout.
A live phone-size test with an Instagram user agent loads the PDP, adds to cart and reaches Shopify checkout,
so the button isn't mechanically broken, but iOS in-app browsing is untested. Watch real session recordings
(Microsoft Clarity) or have two people on iPhones buy through an ad link before you pay for video credits.
