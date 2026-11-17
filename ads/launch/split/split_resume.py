#!/usr/bin/env python3
"""Resume the split after a rate limit: verify new ad sets, then switch over. Never deletes."""
import urllib.request, urllib.parse, urllib.error, json, sys, time

API='https://graph.facebook.com/v22.0'
CAMP='120252641461330104'
OLD='120252662597440104'
P='120252679147450104'
G='120252679147800104'
LOG='/home/user/Kengokuhebun/ads/launch/launch-log.json'

def call(method, path, data=None, patient=False):
    waits = 14 if patient else 3
    for t in range(waits):
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
                print(f'   still rate limited ({time.strftime("%H:%M:%S")}), waiting 120s', flush=True); time.sleep(120); continue
            print(f'ERROR {method} {path}: {body[:300]}', file=sys.stderr); raise SystemExit(1)
    print('gave up waiting for the rate limit to lift - nothing changed on the old ad set', file=sys.stderr); raise SystemExit(3)

print('verify (patient mode)...', flush=True)
vp=call('GET', f'{P}/ads', {'fields':'id,name','limit':50}, patient=True)['data']
time.sleep(5)
vg=call('GET', f'{G}/ads', {'fields':'id,name','limit':50}, patient=True)['data']
print(f'parents ad set holds {len(vp)}/20 ads, gift ad set holds {len(vg)}/5 ads', flush=True)
if len(vp)!=20 or len(vg)!=5:
    print('VERIFY FAILED - old ad set untouched and still delivering; new ad sets stay PAUSED'); sys.exit(2)

log=json.load(open(LOG))
by_name={a['name']:a for a in log['ads']}
new=[]
for which, rows in (('P',vp),('G',vg)):
    for r in rows:
        base=by_name.get(r['name'][:-3]) if r['name'].endswith('_v2') else None
        if not base: print('unmatched ad', r['name']); sys.exit(2)
        new.append({**base,'old_ad_id':base['id'],'id':r['id'],'name':r['name'],'adset':which})

print('switching over: activate new ad sets, then PAUSE (not delete) the old one', flush=True)
call('POST', P, {'status':'ACTIVE'}); time.sleep(4)
call('POST', G, {'status':'ACTIVE'}); time.sleep(4)
call('POST', OLD, {'status':'PAUSED'})

log['adsets']={'P_Parents_28-44':{'id':P,'status':'ACTIVE','age_min':28,'age_max':44,'daily_min_spend_gbp':45,'n_ads':20},
               'G_GiftBuyers_45-65+':{'id':G,'status':'ACTIVE','age_min':45,'age_max':65,'n_ads':5},
               'OLD_All_28-65_Broad':{'id':OLD,'status':'PAUSED','note':'paused, not deleted; 25 original ads inside'}}
log['ads']=new
log['split_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
json.dump(log, open(LOG,'w'), indent=2)

time.sleep(10)
print('readback:')
for label,i in (('parents',P),('gift',G),('old',OLD)):
    r=call('GET', i, {'fields':'name,status,effective_status,daily_min_spend_target'}, patient=True)
    print(f"  {label:8} {r['name']}: {r['status']}/{r['effective_status']} min_spend={r.get('daily_min_spend_target')}")
print('  campaign', call('GET', CAMP, {'fields':'status,effective_status,daily_budget'}, patient=True))
print('DONE', flush=True)
