#!/usr/bin/env python3
"""Resume: build 25 creatives+ads (ALL → PDP) and activate campaign + both ad sets."""
import urllib.request, urllib.parse, urllib.error, json, time, sys

API='https://graph.facebook.com/v22.0'
ACCT='act_1598462168591762'
PAGE='1508787922308138'
PDP='https://x5a9bu-97.myshopify.com/products/glowling-led-drawing-board'
UTM='utm_source=facebook&utm_medium=paid&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{placement}}'

log=json.load(open('/home/user/Kengokuhebun/ads/launch/launch-log.json'))
copies=json.load(open('/home/user/Kengokuhebun/ads/launch/copies.json'))
CAMP=log['campaign']['id']
AS_A=log['adsets']['A_Parents_28-44']['id']
AS_B=log['adsets']['B_GiftBuyers_45-65+']['id']
HASH=log['image_hashes']

STATIC_SLUGS={'S1':'ledger','S2':'714am','S3':'standup','S4':'moon','S5':'boxingday'}
COPY_SLUGS={'C1':'dinner','C2':'shower','C3':'wfh','C4':'bedtime','C5':'gift'}

DOF=('adapt_to_placement','add_text_overlay','creative_stickers','description_automation',
    'enhance_cta','image_animation','image_background_gen','image_brightness_and_contrast',
    'image_templates','image_text_translation','image_touchups','image_uncrop','inline_comment',
    'media_type_automation','pac_relaxation','product_extensions','reveal_details_over_time',
    'text_optimizations','text_translation','translate_voiceover','video_auto_crop',
    'video_filtering','video_uncrop')

def api(method, path, data=None):
    url=f'{API}/{path}'
    if method=='POST':
        req=urllib.request.Request(url, data=urllib.parse.urlencode(data or {}).encode(),
            headers={'Authorization':'Bearer x'}, method='POST')
    else:
        if data: url+='?'+urllib.parse.urlencode(data)
        req=urllib.request.Request(url, headers={'Authorization':'Bearer x'})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        print(f'ERROR {method} {path}:\n{e.read().decode()[:600]}', file=sys.stderr); raise

log.setdefault('creatives',[]); log.setdefault('ads',[])
dof_spec={'creative_features_spec':{f:{'enroll_status':'OPT_OUT'} for f in DOF}}

pairs=[(c,s) for c in ('C1','C2','C3','C4') for s in ('S1','S2','S3','S4','S5')] + [('C5',s) for s in ('S1','S2','S3','S4','S5')]
print(f'Creating {len(pairs)} creatives+ads, all → PDP, status ACTIVE')

for copy, static in pairs:
    cd=copies[copy]
    slug=f'{copy}-{static}-{COPY_SLUGS[copy]}-{STATIC_SLUGS[static]}'
    ad_name=f'Glowling_R1_BF26_{slug}'
    adset_id = AS_B if copy=='C5' else AS_A
    story={'page_id':PAGE,'link_data':{
        'image_hash':HASH[f'{static}_{STATIC_SLUGS[static]}'],
        'link':PDP,
        'message':cd['primary_text'],
        'name':cd['headline'],
        'description':cd['description'],
        'call_to_action':{'type':'SHOP_NOW','value':{'link':PDP}},
    }}
    cr=api('POST', f'{ACCT}/adcreatives', {
        'name':f'cr_{slug}',
        'object_story_spec':json.dumps(story),
        'degrees_of_freedom_spec':json.dumps(dof_spec),
        'contextual_multi_ads':json.dumps({'enroll_status':'OPT_OUT'}),
        'url_tags':UTM,
    })
    log['creatives'].append({'copy':copy,'static':static,'id':cr['id']})
    ad=api('POST', f'{ACCT}/ads', {
        'name':ad_name,
        'adset_id':adset_id,
        'creative':json.dumps({'creative_id':cr['id']}),
        'status':'ACTIVE',
    })
    log['ads'].append({'name':ad_name,'copy':copy,'static':static,'adset':adset_id,'id':ad['id'],'creative_id':cr['id']})
    print(f'  {slug:34} creative={cr["id"]:20} ad={ad["id"]}')

print('\n→ activating ad set A')
api('POST', AS_A, {'status':'ACTIVE'})
log['adsets']['A_Parents_28-44']['status']='ACTIVE'
print('→ activating ad set B')
api('POST', AS_B, {'status':'ACTIVE'})
log['adsets']['B_GiftBuyers_45-65+']['status']='ACTIVE'
print('→ activating campaign')
api('POST', CAMP, {'status':'ACTIVE'})
log['campaign']['status']='ACTIVE'

# READBACK
print('\n=== READBACK ===')
camp=api('GET', CAMP, {'fields':'name,status,effective_status,daily_budget,bid_strategy'})
print(f'Campaign {camp["name"]}: status={camp["status"]} effective={camp["effective_status"]} budget £{int(camp["daily_budget"])/100:.0f}/day {camp["bid_strategy"]}')
for k,ai in (('A',AS_A),('B',AS_B)):
    a=api('GET', ai, {'fields':'name,status,effective_status'})
    n_ads=sum(1 for x in log['ads'] if x['adset']==ai)
    print(f'Ad set {k} {a["name"]}: status={a["status"]} effective={a["effective_status"]} ads={n_ads}')

# status spread across all 25 ads
ids=','.join(a['id'] for a in log['ads'])
s=api('GET', '', {'ids':ids,'fields':'name,status,effective_status'})
from collections import Counter
eff=Counter(v['effective_status'] for v in s.values())
print(f'\n25 ads effective_status: {dict(eff)}')

open('/home/user/Kengokuhebun/ads/launch/launch-log.json','w').write(json.dumps(log,indent=2))
print('Log updated.')
