from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
SP='/tmp/claude-0/-home-user-Kengokuhebun/8aadc6e6-93f1-5925-a984-2582c804173b/scratchpad'
OUT='/home/user/Kengokuhebun/ads/ritual-swipe/final'
ref=Image.open('/root/.claude/uploads/8aadc6e6-93f1-5925-a984-2582c804173b/c30a4e2f-image.jpg').convert('RGB'); W0,H0=ref.size
xs=[0.04,0.5,0.96]; ys=[0.03,0.2,0.5,0.8,0.97]; g=np.zeros((5,3,3))
for j,y in enumerate(ys):
    for i,x in enumerate(xs): g[j,i]=np.asarray(ref.crop((int(x*W0)-12,int(y*H0)-12,int(x*W0)+12,int(y*H0)+12))).reshape(-1,3).mean(0)
g[2,1]=(g[1,1]+g[3,1])/2
CW,CH=1170,1900
def font(size,weight='ExtraBold'):
    ft=ImageFont.truetype(f'{SP}/fonts/Nunito.ttf',size); ft.set_variation_by_name(weight); return ft
tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
def ink(text,ft): l,t,r,b=tmp.textbbox((0,0),text,font=ft); return l,r
def balanced(text,ft,maxw):
    words=text.split(); n=len(words)
    wid=lambda i,j: tmp.textlength(' '.join(words[i:j]),font=ft)
    best=[1e18]*(n+1); nxt=[0]*(n+1); best[n]=0
    for i in range(n-1,-1,-1):
        for j in range(i+1,n+1):
            w=wid(i,j)
            if w>maxw and j>i+1: break
            c=(maxw-w)**2+best[j]
            if c<best[i]: best[i]=c; nxt[i]=j
    lines=[]; i=0
    while i<n: lines.append(' '.join(words[i:nxt[i]])); i=nxt[i]
    return lines
FS=100; MAXW=1000; LH=1.18
def post(hook,keep,name):
    bg=Image.fromarray(g.astype('uint8')).resize((CW,CH),Image.BICUBIC).convert('RGBA')
    ft=font(FS); lines=balanced(hook,ft,MAXW); fk=font(int(FS*0.70),'Bold'); lh=int(FS*LH)
    gap=int(FS*0.75); karrow=int(FS*0.95)
    block=len(lines)*lh+gap+int(FS*0.70*1.2)+karrow
    cy=int(CH*0.47); y0=cy-block//2
    sh=Image.new('RGBA',(CW,CH),(0,0,0,0)); sd=ImageDraw.Draw(sh); layer=Image.new('RGBA',(CW,CH),(0,0,0,0)); ld=ImageDraw.Draw(layer)
    def line(text,ftx,y,fill,shadow):
        l,r=ink(text,ftx); x=(CW-(r-l))/2-l
        sd.text((x,y+4),text,font=ftx,fill=shadow); ld.text((x,y),text,font=ftx,fill=fill)
    y=y0
    for ln in lines: line(ln,ft,y,(255,255,255,255),(30,0,80,95)); y+=lh
    y+=gap; k=keep.replace('↓','').strip(); line(k,fk,y,(255,255,255,238),(30,0,80,95))
    ay=y+int(FS*0.70*1.3); cx=CW//2; s=int(FS*0.30)
    for dd,col,o in ((sd,(30,0,80,95),3),(ld,(255,255,255,238),0)):
        dd.line([(cx,ay+o),(cx,ay+2*s+o)],fill=col,width=11); dd.line([(cx-s,ay+s+o),(cx,ay+2*s+o),(cx+s,ay+s+o)],fill=col,width=11,joint='curve')
    sh=sh.filter(ImageFilter.GaussianBlur(6))
    Image.alpha_composite(Image.alpha_composite(bg,sh),layer).convert('RGB').save(f'{OUT}/{name}.jpg',quality=95)
    wmax=max(ink(l_,ft)[1]-ink(l_,ft)[0] for l_ in lines)
    print(f"{name}: {len(lines)} lines, widest {wmax}px ({100*wmax/CW:.0f}% of width), block y {y0}-{y0+block} (safe 250-1560)")
    for l_ in lines: print('   ',l_)
HOOKS={'G-A_control':("i added up what i spent trying to keep my boys off the ipad before dinner. $847 since january.","keep reading ↓"),
 'G-H1_number':("$847 since january. that's what i added up trying to keep my boys off the ipad before dinner.","the list is in the caption ↓"),
 'G-H2_item':("a $142 easel. used three times. in the garage. it was one line on a list that came to $847.","read the rest ↓"),
 'G-H3_result':("i cooked for twenty-two minutes last tuesday and the ipad never came out. before that, $847 since january and nothing lasted.","here's what changed ↓")}
for n,(h,k) in HOOKS.items(): post(h,k,n)
