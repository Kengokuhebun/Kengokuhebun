#!/usr/bin/env python3
"""Split into Parents (28-44, min spend) + Gift (45-65+) ad sets. Build and verify FIRST; switch over only if verified. Never deletes."""
import urllib.request, urllib.parse, urllib.error, json, sys, time

API='https://graph.facebook.com/v22.0'
ACCT='act_1598462168591762'
CAMP='120252641461330104'
OLD='120252662597440104'
PIXEL='1736160617626618'
LOG='/home/user/Kengokuhebun/ads/launch/launch-log.json'
MIN_PARENTS_PENCE=4500   # GBP 45/day guaranteed to the parent set

def call(method, path, data=None, tries=4):
    for t in range(tries):
        url=f'{API}/{path}'
        if method=='POST':
            req=urllib.request.Request(url, data=urllib.parse.urlencode(data or {}).encode(), headers={'Authorization':'Bearer x'}, method='POST')
        else:
            if data: url+='?'+urllib.parse.urlencode(data)
            req=urllib.request.Request(url, headers={'Authorization':'Bearer x'})
        try:
            return json.loads(urllib.request.urlopen(req, timeout=60).read())
        except urllib.error.HTTPError as e:
            body=e.read().decode()
            if '"code":17' in body or 'too many calls' in body.lower():
                print(f'   rate limited, waiting 75s (try {t+1}/{tries})', flush=True); time.sleep(75); continue
            print(f'ERROR {method} {path}: {body[:400]}', file=sys.stderr); raise SystemExit(1)
    print('gave up after rate limits', file=sys.stderr); raise SystemExit(1)

def adset(name, age_min, age_max, extra=None):
    targeting={'age_min':age_min,'age_max':age_max,
        'geo_locations':{'countries':['US','GB','CA','AU'],'location_types':['home','recent']},
        'targeting_automation':{'advantage_audience':0},
        'publisher_platforms':['facebook','instagram'],
        'facebook_positions':['feed','story','facebook_reels'],
        'instagram_positions':['stream','story','reels'],
        'device_platforms':['mobile','desktop']}
    d={'name':name,'campaign_id':CAMP,'status':'PAUSED','billing_event':'IMPRESSIONS','optimization_goal':'OFFSITE_CONVERSIONS',
       'promoted_object':json.dumps({'pixel_id':PIXEL,'custom_event_type':'PURCHASE'}),
       'attribution_spec':json.dumps([{'event_type':'CLICK_THROUGH','window_days':7},{'event_type':'VIEW_THROUGH','window_days':1}]),
       'targeting':json.dumps(targeting)}
    d.update(extra or {})
    return call('POST', f'{ACCT}/adsets', d)['id']

log=json.load(open(LOG))
src=[a for a in log['ads'] if a.get('creative_id')]
assert len(src)==25, len(src)

print('1) create ad sets (PAUSED)')
P=adset('Glowling_R1_BF26_P_Parents_28-44', 28, 44, {'daily_min_spend_target': str(MIN_PARENTS_PENCE)})
G=adset('Glowling_R1_BF26_G_GiftBuyers_45-65plus', 45, 65)
print('   parents', P, '| gift', G)

print('2) create 25 ads (fresh, from surviving creatives; ad sets still paused so nothing delivers yet)')
new=[]
for a in src:
    target = G if a['copy']=='C5' else P
    ad=call('POST', f'{ACCT}/ads', {'name':a['name']+'_v2','adset_id':target,'creative':json.dumps({'creative_id':a['creative_id']}),'status':'ACTIVE'})
    new.append({**a,'old_ad_id':a['id'],'id':ad['id'],'adset':'P' if target==P else 'G','name':a['name']+'_v2'})
    time.sleep(0.5)
print(f'   created {len(new)}')

print('3) VERIFY before touching the old ad set')
time.sleep(20)
vp=call('GET', f'{P}/ads', {'fields':'id','limit':50})['data']
vg=call('GET', f'{G}/ads', {'fields':'id','limit':50})['data']
print(f'   parents ad set holds {len(vp)}/20 ads, gift ad set holds {len(vg)}/5 ads')
if len(vp)!=20 or len(vg)!=5:
    print('VERIFY FAILED - old ad set left untouched and still delivering. New ad sets stay PAUSED.'); sys.exit(2)

print('4) switch over: activate new ad sets, then PAUSE (not delete) the old one')
call('POST', P, {'status':'ACTIVE'}); time.sleep(3)
call('POST', G, {'status':'ACTIVE'}); time.sleep(3)
call('POST', OLD, {'status':'PAUSED'})

log['adsets']={'P_Parents_28-44':{'id':P,'status':'ACTIVE','age_min':28,'age_max':44,'daily_min_spend_gbp':MIN_PARENTS_PENCE/100,'n_ads':20},
               'G_GiftBuyers_45-65+':{'id':G,'status':'ACTIVE','age_min':45,'age_max':65,'n_ads':5},
               'OLD_All_28-65_Broad':{'id':OLD,'status':'PAUSED','note':'paused, not deleted; 25 original ads inside'}}
log['ads']=new
log['split_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
json.dump(log, open(LOG,'w'), indent=2)

print('5) readback')
time.sleep(15)
for label,i in (('parents',P),('gift',G),('old',OLD)):
    r=call('GET', i, {'fields':'name,status,effective_status,daily_min_spend_target'})
    print(f"   {label:8} {r['name']}: {r['status']}/{r['effective_status']} min_spend={r.get('daily_min_spend_target')}")
c=call('GET', CAMP, {'fields':'status,effective_status,daily_budget'})
print('   campaign', c)
print('DONE')
