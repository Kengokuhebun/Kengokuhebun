# Ads Launcher (v1)

A personal tool to bulk-launch Meta ads. You upload creatives, set campaign settings once, turn all Advantage+ enhancements off with one switch, and publish everything to your ad account in one go.

**Everything is created paused.** Nothing spends money until you switch it on in Ads Manager.

## What v1 does

| Feature | Status |
|---|---|
| Connect a Meta ad account with a System User token | Done |
| Choose an ad account, Page, Instagram account, pixel | Done |
| Drag-and-drop bulk upload (.mp4, .mov, .jpg, .png), with aspect ratio detection (1:1, 4:5, 9:16) | Done |
| Preview grid: rename, include or exclude, per-ad copy overrides, filter by ratio | Done |
| Campaign settings: new or existing campaign, objective, ABO or CBO, daily or lifetime budget, start and end | Done |
| Audience: countries, ages, gender, custom audiences (include or exclude), Advantage+ or manual placements | Done |
| Optimisation: conversions (pixel and event), landing page views, link clicks, reach, impressions | Done |
| **Disable all Advantage+ enhancements** (see below) | Done |
| Ad set structure: 1 ad set per creative, all in 1, or groups of N | Done |
| Dynamic naming, e.g. `{date} - {audience} - {creative}` (also `[Date]` style) | Done |
| Review screen showing every campaign, ad set and ad name before launch | Done |
| Dry run: walks the full launch and shows every API call, sends nothing to Meta | Done |
| Live progress while launching; one failure does not stop the rest | Done |
| Launch history with Meta IDs and Ads Manager links | Done |
| Presets for settings you reuse | Done |
| Optional password protection (`APP_PASSWORD`) | Done |
| Optional Supabase Storage and history table (for hosting online) | Done |
| Login with Facebook, AI campaign builder, placement-asset pairing (one ad with 1:1 + 9:16), multiple text variations | v2 |

## Install on Linux as a desktop app

```bash
sudo apt install -y git curl
git clone -b claude/ads-launcher-v1 https://github.com/Kengokuhebun/Kengokuhebun.git ~/ninu
bash ~/ninu/ads-launcher/scripts/install-linux.sh
```

The installer sets up Node.js 22 for your user if needed, builds the app, asks for your Meta token once (saved in `.env.local`, readable only by you), and adds an **Ads Launcher** icon to your app menu and desktop. Clicking it starts the app in the background on http://localhost:3737 (this computer only) and opens your browser.

Terminal commands: `~/.local/bin/ads-launcher` (open), `ads-launcher stop`, `ads-launcher update` (pull and rebuild), `ads-launcher log`.

## Run it on your computer

You need Node.js 20 or newer.

```bash
cd ads-launcher
npm install
cp .env.example .env.local   # then paste your Meta token into .env.local
npm run dev
```

Open http://localhost:3000. The **Setup** page checks your token and shows the steps to get one.

Without Supabase keys, creatives are stored in `ads-launcher/.data/uploads` and launch history in `.data/history.json`. Both are ignored by git.

### Getting the Meta token (one time)

Short version (the Setup page has the full steps):

1. developers.facebook.com: create a **Business** app, add **Marketing API**, add a privacy policy URL, switch the app to **Live**. Meta rejects ad creatives made by an app in development mode.
2. business.facebook.com/settings, then Users, then System users: add an **Admin** system user. Assign it your ad account, Page and pixel with full control, and add the app.
3. Generate a token for that system user with expiry **Never** and these permissions: `ads_management`, `ads_read`, `business_management`, `pages_show_list`, `pages_read_engagement`, `pages_manage_ads`.
4. Paste it into `.env.local` as `META_ACCESS_TOKEN=...` and restart.

The token stays on the server. It is never sent to the browser, logged, or saved in history.

## How "Disable all Advantage+ enhancements" works

When the switch is on (it is on by default):

- **Every creative** is sent with `degrees_of_freedom_spec.creative_features_spec`, and each of these 23 enhancements is set to `OPT_OUT`: `adapt_to_placement`, `add_text_overlay`, `creative_stickers`, `description_automation`, `enhance_cta`, `image_animation`, `image_background_gen`, `image_brightness_and_contrast`, `image_templates`, `image_text_translation`, `image_touchups`, `image_uncrop`, `inline_comment`, `media_type_automation`, `pac_relaxation`, `product_extensions`, `reveal_details_over_time`, `text_optimizations`, `text_translation`, `translate_voiceover`, `video_auto_crop`, `video_filtering`, `video_uncrop`. Each one is set separately because Meta deprecated the old single `standard_enhancements` switch in API v22.0.
- **Multi-advertiser ads** are opted out (`contextual_multi_ads`).
- **Advantage+ audience** is off on every ad set (`targeting_automation.advantage_audience = 0`), so your age, gender and country settings are hard limits, not suggestions.
- **No text variations**: each ad gets exactly one primary text, headline and description. There is no `asset_feed_spec`, so Meta has no extra text to rotate, and no music is added because no audio is sent.

**Making sure they stay off:**

1. After creating each ad, the tool reads the creative back from Meta. If any enhancement shows `OPT_IN`, you get a warning naming it, on screen and in History.
2. It also reads back the first ad set to confirm Advantage+ audience is off.
3. If a future API version stops accepting one of the setting names, Meta returns an error naming it. The tool drops only that setting, retries, and tells you which one was dropped. If Meta rejects the settings without naming one, the ad is **not** created, so nothing goes live with enhancements on by accident.

Two separate controls are not covered by the switch, and you choose them yourself: **placements** (Advantage+ or Manual) and **campaign budget** (CBO is Meta's "Advantage campaign budget"). The launch panel warns you when either is still on.

The list of enhancements comes from Meta's Advantage+ creative documentation, read on 2026-11-06. Meta changes these often, which is why the tool reads each ad back instead of trusting the request.

## Naming tokens

`{date}` `{campaign}` `{objective}` `{audience}` `{country}` `{adset}` `{creative}` `{ratio}` `{type}` `{n}`. `[Date]` style works too. Unknown tokens are left as typed so a typo is visible in the Review section.

`{creative}` is the creative's name in the grid (the file name without its extension, editable).

## URL parameters

The default is
`utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_term={{adset.name}}&utm_content={{ad.id}}`.
Meta fills the `{{...}}` values. With `utm_content={{ad.id}}`, Shopify orders can be matched to the exact ad.

## Hosting online (optional)

1. Create a Supabase project. In the SQL editor, run `supabase/schema.sql`. This creates a private `creatives` bucket and a `launches` table.
2. Set these on your host, for example in Vercel's Environment Variables: `META_ACCESS_TOKEN`, `META_APP_SECRET`, `APP_PASSWORD`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.
3. Deploy. Uploads go straight from the browser to Supabase, so file size is not limited by the host. Videos are handed to Meta as a short-lived signed URL.

Always set `APP_PASSWORD` when it is online, because anyone with the URL could otherwise launch ads on your account.

A launch with many videos can take several minutes while Meta processes them. On Vercel the launch route asks for up to 800 seconds, which needs a plan that allows it. Running locally has no limit.

## Developer notes

```bash
npm test            # unit tests: plan builder, Advantage+ payloads, executor, Graph client
npm run typecheck
npm run lint
npm run mock:meta   # fake Meta API on :4010 for testing without a real account
npm run dev:mock    # app pointed at the fake API (token "test-token")
```

The mock can simulate Meta rejecting a setting (`MOCK_REJECT_KEY=video_filtering`) and an enhancement coming back on (`MOCK_FLIP=1`).

Code map:

| Path | What |
|---|---|
| `src/lib/launch/schema.ts` | Launch settings and creative types (zod) |
| `src/lib/launch/plan.ts` | Turns settings into exact Meta payloads; validation |
| `src/lib/launch/advantage.ts` | Advantage+ opt-out list, rejected-key handling, read-back check |
| `src/lib/launch/executor.ts` | Runs the plan against the API, streams progress |
| `src/lib/meta/graph.ts` | Graph API client: retries, error messages, appsecret_proof |
| `src/lib/server/*` | Env, storage (local or Supabase), history |
| `src/app/api/*` | Routes: config, Meta account data, media, launch (streaming), history |
| `src/components/*` | UI |

Things v1 has **not** been tested against: a real Meta ad account. Every path was tested against the mock API and unit tests, which follow Meta's documented request shapes. Do the first real launch with one or two creatives, check them in Ads Manager, then go bigger.
