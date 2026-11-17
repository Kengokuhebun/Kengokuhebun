#!/usr/bin/env python3
"""3h performance check for Glowling_R1_BF26_CBO."""
import urllib.request, urllib.parse, urllib.error, json, sys, time, os
from collections import Counter

API='https://graph.facebook.com/v22.0'
CAMP='120252641461330104'
AS='120252662597440104'
ACCT='act_1598462168591762'
PIXEL='1736160617626618'

def g(path, params=None):
    url=f'{API}/{path}'
    if params: url+='?'+urllib.parse.urlencode(params)
    try:
        return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'Authorization':'Bearer x'}), timeout=60).read())
    except urllib.error.HTTPError as e:
        print(f'ERR {path}: {e.read().decode()[:300]}', file=sys.stderr)
        return {'error': str(e)}

def parse_actions(actions):
    d={}
    for a in actions or []:
        d[a['action_type']]=float(a['value'])
    return {
        'lpv': d.get('landing_page_view', 0),
        'atc': d.get('add_to_cart', 0),
        'ic':  d.get('initiate_checkout', 0),
        'purchase': d.get('purchase', 0),
    }

def parse_values(action_values):
    for a in action_values or []:
        if a['action_type']=='purchase': return float(a['value'])
    return 0

FIELDS='spend,impressions,cpm,inline_link_clicks,cost_per_inline_link_click,actions,action_values,purchase_roas,reach,frequency'

# A) Campaign totals today + 24h
camp_today = g(f'{CAMP}/insights', {'date_preset':'today','fields':FIELDS})
camp_24h = g(f'{CAMP}/insights', {'date_preset':'last_3d','fields':FIELDS})

def summarize(data, label):
    rows = data.get('data', [])
    if not rows:
        return {'label': label, 'spend': 0, 'impressions': 0, 'empty': True}
    r = rows[0]
    acts = parse_actions(r.get('actions'))
    rev = parse_values(r.get('action_values'))
    spend = float(r.get('spend', 0))
    return {
        'label': label,
        'spend': spend, 'impressions': int(r.get('impressions', 0)),
        'cpm': float(r.get('cpm', 0)), 'clicks': int(r.get('inline_link_clicks', 0)),
        'cpc': float(r.get('cost_per_inline_link_click', 0)),
        'lpv': int(acts['lpv']), 'atc': int(acts['atc']), 'ic': int(acts['ic']),
        'purchase': int(acts['purchase']), 'revenue': rev,
        'cost_per_lpv': spend/acts['lpv'] if acts['lpv']>0 else None,
        'cost_per_atc': spend/acts['atc'] if acts['atc']>0 else None,
        'cost_per_purchase': spend/acts['purchase'] if acts['purchase']>0 else None,
        'roas': rev/spend if spend>0 else 0,
    }

C_today = summarize(camp_today, 'today')
C_24h = summarize(camp_24h, 'last_3d')

# B) Per-ad
ads = g(f'{CAMP}/insights', {
    'level':'ad','date_preset':'today',
    'fields':'ad_name,'+FIELDS,'limit':50
})
ad_rows = []
for r in ads.get('data', []):
    acts = parse_actions(r.get('actions'))
    spend = float(r.get('spend', 0))
    ad_rows.append({
        'name': r.get('ad_name','?'),
        'spend': spend, 'impressions': int(r.get('impressions',0)),
        'clicks': int(r.get('inline_link_clicks',0)),
        'cpc': float(r.get('cost_per_inline_link_click',0)),
        'lpv': int(acts['lpv']), 'atc': int(acts['atc']), 'ic': int(acts['ic']),
        'purchase': int(acts['purchase']),
        'cost_per_lpv': spend/acts['lpv'] if acts['lpv']>0 else None,
    })
ad_rows.sort(key=lambda x: (x['cost_per_lpv'] is None, x['cost_per_lpv'] or 999))

# C) Placement
plc = g(f'{CAMP}/insights', {
    'date_preset':'today','breakdowns':'publisher_platform,platform_position',
    'fields':'spend,impressions,inline_link_clicks,cost_per_inline_link_click,inline_link_click_ctr,actions','limit':50
})
plc_rows = []
for r in plc.get('data', []):
    acts = parse_actions(r.get('actions'))
    spend = float(r.get('spend',0))
    plc_rows.append({
        'platform': r.get('publisher_platform','?'),
        'position': r.get('platform_position','?'),
        'spend': spend,
        'cpc': float(r.get('cost_per_inline_link_click',0)),
        'atc': int(acts['atc']),
        'lpv': int(acts['lpv']),
    })

# D) Country
ctry = g(f'{CAMP}/insights', {
    'date_preset':'today','breakdowns':'country',
    'fields':'spend,impressions,inline_link_clicks,cost_per_inline_link_click,actions','limit':50
})
ctry_rows = []
for r in ctry.get('data', []):
    acts = parse_actions(r.get('actions'))
    spend = float(r.get('spend',0))
    ctry_rows.append({'c': r.get('country','?'), 'spend': spend, 'cpc': float(r.get('cost_per_inline_link_click',0)), 'lpv': int(acts['lpv']), 'atc': int(acts['atc']), 'purchase': int(acts['purchase'])})

# E) Age
age = g(f'{CAMP}/insights', {
    'date_preset':'today','breakdowns':'age',
    'fields':'spend,impressions,inline_link_clicks,cost_per_inline_link_click,actions','limit':50
})
age_rows = []
for r in age.get('data', []):
    acts = parse_actions(r.get('actions'))
    spend = float(r.get('spend',0))
    age_rows.append({'age': r.get('age','?'), 'spend': spend, 'cpc': float(r.get('cost_per_inline_link_click',0)), 'lpv': int(acts['lpv']), 'atc': int(acts['atc']), 'purchase': int(acts['purchase'])})

# Snapshot prior for delta
prior_path='/home/user/Kengokuhebun/ads/launch/perfcheck-latest.json'
prior = None
if os.path.exists(prior_path):
    try: prior = json.load(open(prior_path))
    except: pass

# Apply kill rules
flags = []
camp_cpl = C_today.get('cost_per_lpv')
# Rule 1
for a in ad_rows:
    if a['spend'] > 50 and a['cost_per_lpv'] and camp_cpl and a['cost_per_lpv'] > 2*camp_cpl and a['impressions'] > 1000:
        flags.append({'rule':1,'ad':a['name'],'reason':f"spend £{a['spend']:.2f}, cost/LPV £{a['cost_per_lpv']:.2f} vs campaign avg £{camp_cpl:.2f}, {a['impressions']} imp"})
# Rule 2
for a in ad_rows:
    if a['cpc']>0 and a['cpc'] < 0.30 and a['atc']==0 and a['impressions']>500:
        flags.append({'rule':2,'ad':a['name'],'reason':f"CPC £{a['cpc']:.2f}, 0 ATC, {a['impressions']} imp"})
# Rule 3 - placement
total_spend = C_today['spend']
for p in plc_rows:
    if total_spend>0 and (p['spend']/total_spend)>0.5 and p['cpc']>0 and p['cpc']<0.30 and p['atc']==0:
        flags.append({'rule':3,'placement':f"{p['platform']}/{p['position']}",'reason':f"{p['spend']/total_spend*100:.0f}% of spend, CPC £{p['cpc']:.2f}, 0 ATC"})
# Rule 4 - country
cpa = C_today.get('cost_per_purchase')
for c in ctry_rows:
    if c['spend']>80 and (c['purchase']==0 or (cpa and c['spend']/max(c['purchase'],1)>2*cpa)):
        flags.append({'rule':4,'country':c['c'],'reason':f"£{c['spend']:.2f} spent, {c['purchase']} purchases"})
# Rule 5 - age
age_cpas = [(a['age'], a['spend']/max(a['purchase'],0.001)) for a in age_rows if a['purchase']>0]
if len(age_cpas)>=2:
    best = min(x[1] for x in age_cpas)
    for a in age_rows:
        if a['spend']>40 and a['purchase']>0 and (a['spend']/a['purchase'])>1.5*best:
            flags.append({'rule':5,'age':a['age'],'reason':f"£{a['spend']:.2f}, CPA £{a['spend']/a['purchase']:.2f} vs best £{best:.2f}"})
# Rule 6 - deterioration
delta_note=''
if prior:
    prior_cpl = prior.get('campaign_today',{}).get('cost_per_lpv')
    if prior_cpl and camp_cpl and C_today['spend']>50:
        pct = (camp_cpl - prior_cpl)/prior_cpl*100
        delta_note = f"cost/LPV delta: £{prior_cpl:.2f} → £{camp_cpl:.2f} ({pct:+.0f}%)"
        if pct > 30:
            flags.append({'rule':6,'reason':f"cost/LPV up {pct:.0f}% vs last check"})

# Verdict
if C_today['spend'] < 5:
    verdict = 'Watch'
    verdict_reason = 'Very early, insufficient spend (<£5) to judge anything'
elif any(f['rule']==6 for f in flags):
    verdict = 'Needs intervention'
    verdict_reason = 'Deterioration flag triggered'
elif C_today['spend'] > 100 and C_today['purchase']==0 and C_today['atc']==0:
    verdict = 'Kill now'
    verdict_reason = f"£{C_today['spend']:.0f} spent, 0 ATC, 0 purchase"
elif flags:
    verdict = 'Watch'
    verdict_reason = f"{len(flags)} flags but spend too small for firm action"
else:
    verdict = 'Keep running'
    verdict_reason = 'No kill rules triggered'

ts_utc = time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())
ts_fn = time.strftime('%Y%m%d-%H%M', time.gmtime())

# Build report
def fmt_pct(v,t): return f"{v/t*100:.0f}%" if t>0 else '-'
def fmt(v): return f"£{v:.2f}" if v is not None else '—'

report = [f"# 3h check {ts_utc}", f"**Verdict: {verdict}** — {verdict_reason}", ""]
report.append("## Campaign (today / last 24h)")
report.append(f"| Window | Spend | Imp | CPM | CPC | LPV | ATC | IC | Purch | Revenue | ROAS |")
report.append(f"|---|---|---|---|---|---|---|---|---|---|---|")
for s in (C_today, C_24h):
    if s.get('empty'):
        report.append(f"| {s['label']} | £0 | 0 | — | — | 0 | 0 | 0 | 0 | £0 | 0 |")
    else:
        report.append(f"| {s['label']} | £{s['spend']:.2f} | {s['impressions']} | £{s['cpm']:.2f} | £{s['cpc']:.2f} | {s['lpv']} | {s['atc']} | {s['ic']} | {s['purchase']} | £{s['revenue']:.2f} | {s['roas']:.2f} |")
report.append("")
report.append("## Top 5 ads by cost/LPV")
report.append("| Ad | Spend | Imp | CPC | LPV | ATC | Cost/LPV |")
report.append("|---|---|---|---|---|---|---|")
for a in ad_rows[:5]:
    report.append(f"| {a['name']} | £{a['spend']:.2f} | {a['impressions']} | £{a['cpc']:.2f} | {a['lpv']} | {a['atc']} | {fmt(a['cost_per_lpv'])} |")
report.append("")
report.append("## Bottom 3 ads")
report.append("| Ad | Spend | Imp | CPC | LPV | ATC | Cost/LPV |")
report.append("|---|---|---|---|---|---|---|")
for a in [x for x in ad_rows if x['impressions']>0][-3:]:
    report.append(f"| {a['name']} | £{a['spend']:.2f} | {a['impressions']} | £{a['cpc']:.2f} | {a['lpv']} | {a['atc']} | {fmt(a['cost_per_lpv'])} |")
report.append("")
report.append("## Placement spread")
for p in sorted(plc_rows, key=lambda x: -x['spend']):
    share = p['spend']/total_spend*100 if total_spend>0 else 0
    report.append(f"- {p['platform']}/{p['position']}: £{p['spend']:.2f} ({share:.0f}%) · CPC £{p['cpc']:.2f} · LPV {p['lpv']} · ATC {p['atc']}")
report.append("")
report.append("## Country spread")
for c in sorted(ctry_rows, key=lambda x: -x['spend']):
    share = c['spend']/total_spend*100 if total_spend>0 else 0
    report.append(f"- {c['c']}: £{c['spend']:.2f} ({share:.0f}%) · CPC £{c['cpc']:.2f} · LPV {c['lpv']} · ATC {c['atc']} · Purch {c['purchase']}")
report.append("")
report.append("## Age spread")
for a in sorted(age_rows, key=lambda x: -x['spend']):
    share = a['spend']/total_spend*100 if total_spend>0 else 0
    report.append(f"- {a['age']}: £{a['spend']:.2f} ({share:.0f}%) · CPC £{a['cpc']:.2f} · LPV {a['lpv']} · ATC {a['atc']} · Purch {a['purchase']}")
report.append("")
if delta_note: report.append(f"## Deltas vs last check\n- {delta_note}\n")
report.append("## Flags")
if flags:
    for f in flags:
        bits = [f"rule {f['rule']}"] + [f"{k}={v}" for k,v in f.items() if k not in ('rule',)]
        report.append(f"- {' · '.join(bits)}")
else:
    report.append("- none")
report.append("")
report.append("## Recommended actions (do not execute)")
if C_today['spend']<5:
    report.append("- Wait for the next check at 12:01 UTC. ~£10/3h at this budget; need two more checks to see signal.")
elif any(f['rule']==3 for f in flags):
    report.append("- One placement is eating spend with no ATC. Consider excluding it manually in Meta.")
elif any(f['rule']==4 for f in flags):
    report.append("- One country has sunk >£80 with no purchases. Consider dropping from targeting.")
else:
    report.append("- Nothing to action. Let CBO continue picking winners.")
report.append("")
print('\n'.join(report))

# Save
snapshot = {
    'ts': ts_utc, 'ts_fn': ts_fn,
    'campaign_today': C_today, 'campaign_24h': C_24h,
    'ads': ad_rows, 'placements': plc_rows, 'countries': ctry_rows, 'ages': age_rows,
    'flags': flags, 'verdict': verdict,
}
out_ts = f'/home/user/Kengokuhebun/ads/launch/perfcheck-{ts_fn}.json'
open(out_ts, 'w').write(json.dumps(snapshot, indent=2))
open(prior_path, 'w').write(json.dumps(snapshot, indent=2))
report_path = f'/home/user/Kengokuhebun/ads/launch/perfcheck-{ts_fn}.md'
open(report_path, 'w').write('\n'.join(report))
print(f'\n(Saved to {report_path} and perfcheck-latest.json)')
print(f'(VERDICT: {verdict})')
