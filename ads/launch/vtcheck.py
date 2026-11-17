#!/usr/bin/env python3
"""Report-only readout for Glowling_R1_BF26_VIDEO_TEST. Never changes anything."""
import urllib.request, urllib.parse, json
API='https://graph.facebook.com/v22.0'; CAMP='120252690625940104'
def g(p,q):
    try: return json.loads(urllib.request.urlopen(urllib.request.Request(f'{API}/{p}?'+urllib.parse.urlencode(q),headers={'Authorization':'Bearer x'}),timeout=60).read())
    except Exception as e: return {'error':str(e)}
r=g(f'{CAMP}/insights',{'level':'ad','date_preset':'maximum','fields':'ad_name,spend,impressions,inline_link_clicks,inline_link_click_ctr,actions,video_thruplay_watched_actions','limit':20})
print(f"{'ad':32} {'spend':>7} {'imp':>6} {'hook3s':>7} {'thru%':>6} {'ctr':>5} {'clk':>4} {'lpv':>4} {'£/lpv':>6}  flags")
for x in sorted(r.get('data',[]),key=lambda x:x['ad_name']):
    a={i['action_type']:float(i['value']) for i in x.get('actions',[])}
    imp=int(x['impressions']); sp=float(x['spend']); clk=int(x.get('inline_link_clicks',0)); lpv=a.get('landing_page_view',0)
    v3=a.get('video_view',0); th=sum(float(i['value']) for i in x.get('video_thruplay_watched_actions',[]))
    hook=100*v3/imp if imp else 0; ctr=float(x.get('inline_link_click_ctr',0) or 0)
    fl=[]
    if imp>=1000 and hook<15: fl.append('hook<15% after 1000 imp')
    if imp>=1500 and ctr<0.7: fl.append('CTR<0.7% after 1500 imp')
    if imp<1000: fl.append('small sample, no verdict')
    print(f"{x['ad_name'][-22:]:32} £{sp:6.2f} {imp:6d} {hook:6.1f}% {100*th/imp if imp else 0:5.1f}% {ctr:4.2f}% {clk:4d} {lpv:4.0f} {(sp/lpv if lpv else 0):6.2f}  {'; '.join(fl)}")
