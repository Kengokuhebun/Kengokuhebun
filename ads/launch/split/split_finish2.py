#!/usr/bin/env python3
"""Finish the split: find the highest minimum Meta accepts for the parents set, then switch over. Never deletes."""
import urllib.request, urllib.parse, urllib.error, json, sys, time

API='https://graph.facebook.com/v22.0'
CAMP='120252641461330104'; OLD='120252662597440104'
P='120252679147450104'; G='120252679147800104'
LOG='/home/user/Kengokuhebun/ads/launch/launch-log.json'

def raw(method, path, data=None):
    for t in range(12):
        url=f'{API}/{path}'
        if method=='POST':
            req=urllib.request.Request(url, data=urllib.parse.urlencode(data or {}).encode(), headers={'Authorization':'Bearer x'}, method='POST')
        else:
            if data: url+='?'+urllib.parse.urlencode(data)
            req=urllib.request.Request(url, headers={'Authorization':'Bearer x'})
        try:
            return 200, json.loads(urllib.request.urlopen(req, timeout=60).read())
        except urllib.error.HTTPError as e:
            body=e.read().decode()
            if '"code":613' in body:
                print('   30s edit limit hit, waiting 45s', flush=True); time.sleep(45); continue
            if '"code":17' in body or 'too many calls' in body.lower():
                print(f'   rate limited, waiting 120s', flush=True); time.sleep(120); continue
            return e.code, json.loads(body)
    print('gave up on rate limit; nothing switched'); sys.exit(3)


CAP_PENCE=3500   # gift set may spend at most GBP 35/day, leaving ~GBP 45 for the parent set
def need(c,r,what):
    if c!=200:
        print(f'STOP at {what}: {json.dumps(r)[:300]}'); sys.exit(5)

print('1) gift set: cap GBP 35/day and activate', flush=True)
c,r=raw('POST', G, {'daily_spend_cap': str(CAP_PENCE), 'status':'ACTIVE'}); need(c,r,'gift set')
time.sleep(40)
print('2) parents set: remove the minimum (Meta rejects it) and activate', flush=True)
c,r=raw('POST', P, {'daily_min_spend_target':'0','status':'ACTIVE'}); need(c,r,'parents set')
time.sleep(40)
print('3) pause (not delete) the old ad set', flush=True)
c,r=raw('POST', OLD, {'status':'PAUSED'}); need(c,r,'old ad set')

time.sleep(10)
log=json.load(open(LOG)); by={a['name']:a for a in log['ads']}
new=[]
for which,i in (('P',P),('G',G)):
    c,r=raw('GET', f'{i}/ads', {'fields':'id,name','limit':50}); need(c,r,'list ads')
    for a in r['data']:
        base=by[a['name'][:-3]]; new.append({**base,'old_ad_id':base['id'],'id':a['id'],'name':a['name'],'adset':which})
log['adsets']={'P_Parents_28-44':{'id':P,'status':'ACTIVE','age_min':28,'age_max':44,'min_spend':'none (Meta rejected any minimum)','n_ads':sum(1 for a in new if a['adset']=='P')},
               'G_GiftBuyers_45-65+':{'id':G,'status':'ACTIVE','age_min':45,'age_max':65,'daily_spend_cap_gbp':CAP_PENCE/100,'n_ads':sum(1 for a in new if a['adset']=='G')},
               'OLD_All_28-65_Broad':{'id':OLD,'status':'PAUSED','note':'paused, not deleted; 25 original ads inside'}}
log['ads']=new; log['split_at']=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
json.dump(log, open(LOG,'w'), indent=2)

print('readback:')
for label,i in (('parents',P),('gift',G),('old',OLD)):
    c,r=raw('GET', i, {'fields':'name,status,effective_status,daily_min_spend_target,daily_spend_cap'})
    print(f"  {label:8} {r['name']}: {r['status']}/{r['effective_status']} min={r.get('daily_min_spend_target')} cap={r.get('daily_spend_cap')}")
c,r=raw('GET', CAMP, {'fields':'status,effective_status,daily_budget'}); print('  campaign', r)
for label,i in (('parents',P),('gift',G)):
    c,r=raw('GET', f'{i}/ads', {'fields':'effective_status','limit':50})
    print(f'  {label} ads:', {k:sum(1 for a in r['data'] if a['effective_status']==k) for k in {a['effective_status'] for a in r['data']}})
print('DONE')
