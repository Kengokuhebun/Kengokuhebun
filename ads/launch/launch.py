#!/usr/bin/env python3
"""Glowling R1 Black Friday CBO launch: campaign + 2 ad sets + 25 ads, all PAUSED."""
import urllib.request, urllib.parse, urllib.error, json, os, sys, time, mimetypes

API = 'https://graph.facebook.com/v22.0'
ACCT = 'act_1598462168591762'
PAGE = '1508787922308138'        # Amanda Miller
PIXEL = '1736160617626618'        # shared pixel (flagged)
PDP   = 'https://x5a9bu-97.myshopify.com/products/glowling-led-drawing-board'
LIST  = 'https://x5a9bu-97.myshopify.com/pages/glowling-7-reasons'
DAILY_BUDGET_PENCE = 8000         # £80/day CBO
UTM = 'utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{placement}}'

IMGDIR = '/tmp/claude-0/-home-user-Kengokuhebun/8aadc6e6-93f1-5925-a984-2582c804173b/scratchpad/staticimgs'
STATICS = {
    'S1': ('ledger',     f'{IMGDIR}/Product_contents_flat_lay_arrang__2d201ecf.jpg'),
    'S2': ('714am',      f'{IMGDIR}/Boy_drawing_on_glowing_board_161c9065.jpg'),
    'S3': ('standup',    f'{IMGDIR}/Child_drawing_at_kitchen_bench_1c1377cb.jpg'),
    'S4': ('moon',       f'{IMGDIR}/Create_product_collage_layout_46c12074.jpg'),
    'S5': ('boxingday',  f'{IMGDIR}/Promotional_graphic_for_drawing___9b5a4179.jpg'),
}
COPY_LP = {'C1': LIST, 'C2': PDP, 'C3': PDP, 'C4': PDP, 'C5': LIST}
COPY_SLUG = {'C1': 'dinner', 'C2': 'shower', 'C3': 'wfh', 'C4': 'bedtime', 'C5': 'gift'}

copies = json.load(open('/home/user/Kengokuhebun/ads/launch/copies.json'))

# All Advantage+ creative features to opt out of
DOF_FEATURES = ('adapt_to_placement','add_text_overlay','creative_stickers','description_automation',
    'enhance_cta','image_animation','image_background_gen','image_brightness_and_contrast',
    'image_templates','image_text_translation','image_touchups','image_uncrop','inline_comment',
    'media_type_automation','pac_relaxation','product_extensions','reveal_details_over_time',
    'text_optimizations','text_translation','translate_voiceover','video_auto_crop',
    'video_filtering','video_uncrop')
def dof():
    return {'creative_features_spec': {f: {'enroll_status': 'OPT_OUT'} for f in DOF_FEATURES}}

def api(method, path, data=None, multipart=None):
    url = f'{API}/{path}'
    if multipart:
        boundary = '----form' + str(int(time.time()*1000))
        body = []
        for k, v in (data or {}).items():
            body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
        fname, fpath = multipart
        ctype = mimetypes.guess_type(fname)[0] or 'application/octet-stream'
        body.append(f'--{boundary}\r\nContent-Disposition: form-data; name="filename"; filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'.encode())
        body.append(open(fpath, 'rb').read())
        body.append(f'\r\n--{boundary}--\r\n'.encode())
        payload = b''.join(body)
        headers = {'Authorization': 'Bearer x', 'Content-Type': f'multipart/form-data; boundary={boundary}'}
        req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
    elif method == 'POST':
        payload = urllib.parse.urlencode(data or {}).encode()
        req = urllib.request.Request(url, data=payload, headers={'Authorization': 'Bearer x'}, method='POST')
    else:
        if data:
            url += '?' + urllib.parse.urlencode(data)
        req = urllib.request.Request(url, headers={'Authorization': 'Bearer x'})
    try:
        r = urllib.request.urlopen(req, timeout=60).read()
        return json.loads(r)
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f'ERROR {method} {path}:\n{err[:1000]}', file=sys.stderr)
        raise SystemExit(1)

log = {'campaign': None, 'adsets': {}, 'image_hashes': {}, 'creatives': [], 'ads': []}

# 1. CAMPAIGN
print('→ creating campaign')
camp = api('POST', f'{ACCT}/campaigns', {
    'name': 'Glowling_R1_BF26_CBO',
    'objective': 'OUTCOME_SALES',
    'status': 'PAUSED',
    'special_ad_categories': json.dumps([]),
    'buying_type': 'AUCTION',
    'daily_budget': DAILY_BUDGET_PENCE,
    'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
})
log['campaign'] = camp
CAMP_ID = camp['id']
print(f'  campaign_id={CAMP_ID}')

# 2. AD SETS
def make_adset(name, age_min, age_max):
    targeting = {
        'age_min': age_min, 'age_max': age_max,
        'geo_locations': {'countries': ['US','GB','CA','AU'], 'location_types': ['home','recent']},
        'targeting_automation': {'advantage_audience': 0},
        'publisher_platforms': ['facebook','instagram'],
        'facebook_positions': ['feed','story','facebook_reels'],
        'instagram_positions': ['stream','story','reels'],
        'device_platforms': ['mobile','desktop'],
    }
    promo = {'pixel_id': PIXEL, 'custom_event_type': 'PURCHASE'}
    attrib = [{'event_type': 'CLICK_THROUGH','window_days': 7},{'event_type': 'VIEW_THROUGH','window_days': 1}]
    r = api('POST', f'{ACCT}/adsets', {
        'name': name, 'campaign_id': CAMP_ID, 'status': 'PAUSED',
        'billing_event': 'IMPRESSIONS', 'optimization_goal': 'OFFSITE_CONVERSIONS',
        'promoted_object': json.dumps(promo),
        'attribution_spec': json.dumps(attrib),
        'targeting': json.dumps(targeting),
    })
    return r

print('→ creating ad set A (parents 28-44)')
adset_a = make_adset('Glowling_R1_BF26_A_Parents_28-44_BroadX4', 28, 44)
log['adsets']['A'] = adset_a
AS_A = adset_a['id']
print(f'  adset_a={AS_A}')

print('→ creating ad set B (grandparents 45-65+)')
adset_b = make_adset('Glowling_R1_BF26_B_GiftBuyers_45-65plus_BroadX4', 45, 65)
log['adsets']['B'] = adset_b
AS_B = adset_b['id']
print(f'  adset_b={AS_B}')

# 3. UPLOAD IMAGES
print('→ uploading 5 placeholder static images')
for s, (slug, path) in STATICS.items():
    fname = os.path.basename(path)
    r = api('POST', f'{ACCT}/adimages', {}, multipart=(fname, path))
    h = list(r['images'].values())[0]['hash']
    log['image_hashes'][s] = h
    print(f'  {s} {slug}: hash={h}')

# 4. CREATIVES + ADS (25 total: 20 in A, 5 in B)
def make_creative_and_ad(copy, static, adset_id):
    cdata = copies[copy]
    img_hash = log['image_hashes'][static]
    link = COPY_LP[copy]
    name_parts = f'{copy}-{static}-{COPY_SLUG[copy]}-{STATICS[static][0]}'
    ad_name = f'Glowling_R1_BF26_{name_parts}'
    story = {
        'page_id': PAGE,
        'link_data': {
            'image_hash': img_hash,
            'link': link,
            'message': cdata['primary_text'],
            'name': cdata['headline'],
            'description': cdata['description'],
            'call_to_action': {'type': 'SHOP_NOW', 'value': {'link': link}},
        },
    }
    creative = api('POST', f'{ACCT}/adcreatives', {
        'name': f'cr_{name_parts}',
        'object_story_spec': json.dumps(story),
        'degrees_of_freedom_spec': json.dumps(dof()),
        'contextual_multi_ads': json.dumps({'enroll_status': 'OPT_OUT'}),
        'url_tags': UTM,
    })
    log['creatives'].append({'copy': copy, 'static': static, 'id': creative['id']})
    ad = api('POST', f'{ACCT}/ads', {
        'name': ad_name,
        'adset_id': adset_id,
        'creative': json.dumps({'creative_id': creative['id']}),
        'status': 'PAUSED',
    })
    log['ads'].append({'name': ad_name, 'copy': copy, 'static': static, 'adset': adset_id, 'id': ad['id'], 'creative_id': creative['id']})
    return ad

# 20 parent-copy ads in A
print('→ creating 20 parent-copy ads in A')
for copy in ('C1','C2','C3','C4'):
    for static in ('S1','S2','S3','S4','S5'):
        ad = make_creative_and_ad(copy, static, AS_A)
        print(f'  {copy}-{static} → ad {ad["id"]}')

# 5 gift-copy ads in B
print('→ creating 5 gift-copy ads in B')
for static in ('S1','S2','S3','S4','S5'):
    ad = make_creative_and_ad('C5', static, AS_B)
    print(f'  C5-{static} → ad {ad["id"]}')

# 5. READ BACK
print('\n=== READBACK ===')
camp_rb = api('GET', CAMP_ID, {'fields':'name,objective,status,effective_status,daily_budget,bid_strategy,buying_type,special_ad_categories'})
print(f'Campaign: {camp_rb["name"]} · {camp_rb["objective"]} · budget £{int(camp_rb.get("daily_budget",0))/100:.2f}/day · {camp_rb["bid_strategy"]} · {camp_rb["effective_status"]}')
for k, as_id in (('A', AS_A), ('B', AS_B)):
    ad = api('GET', as_id, {'fields':'name,status,effective_status,targeting,promoted_object,optimization_goal,attribution_spec'})
    t = ad['targeting']
    print(f'Ad set {k}: {ad["name"]} · {ad["effective_status"]} · age {t["age_min"]}-{t["age_max"]} · countries {t["geo_locations"]["countries"]} · placements FB:{t.get("facebook_positions")} IG:{t.get("instagram_positions")} · opt {ad["optimization_goal"]} · pixel {ad["promoted_object"]["pixel_id"]}/{ad["promoted_object"]["custom_event_type"]}')
ads_count = len(log['ads'])
print(f'\nAds created: {ads_count} (20 in A + 5 in B), all PAUSED')

# 6. SAVE LAUNCH LOG
open('/home/user/Kengokuhebun/ads/launch/launch-log.json','w').write(json.dumps(log, indent=2))
print('\nLaunch log saved to ads/launch/launch-log.json')
