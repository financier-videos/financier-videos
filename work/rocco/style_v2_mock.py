from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
W,H=1080,1920; L='/tmp/fin_rocco_lib800/'
F=lambda s:ImageFont.truetype('/tmp/fonts/LilitaOne-Regular.ttf',s)
INK=(35,39,45)
def bg(c1,c2,dots=None,rays=None):
    im=Image.new('RGB',(W,H),c1); d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H; d.line([(0,y),(W,y)],fill=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)))
    if rays:
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov); cx,cy=W/2,H*0.42
        for k in range(0,360,20):
            a1,a2=math.radians(k),math.radians(k+10); R=2400
            od.polygon([(cx,cy),(cx+R*math.cos(a1),cy+R*math.sin(a1)),(cx+R*math.cos(a2),cy+R*math.sin(a2))],fill=rays+(70,))
        im.paste(ov,(0,0),ov)
    if dots:
        d=ImageDraw.Draw(im,'RGBA')
        for yy in range(0,H,54):
            for xx in range((yy//54%2)*27,W,54):
                r=5+7*(yy/H); d.ellipse([xx-r,yy-r,xx+r,yy+r],fill=dots+(60,))
    return im
def rocco(im,clip,size,x,y,flip=False):
    p=Image.open(L+clip).convert('RGBA').resize((size,size),Image.LANCZOS)
    if flip: p=p.transpose(Image.FLIP_LEFT_RIGHT)
    sh=Image.new('RGBA',im.size,(0,0,0,0)); ImageDraw.Draw(sh).ellipse([x+size*0.22,y+size*0.76,x+size*0.78,y+size*0.83],fill=(0,0,0,70)); im.paste(sh,(0,0),sh)
    im.paste(p,(x,y),p)
def piggy(im,cx,cy,s,mood='happy'):
    d=ImageDraw.Draw(im,'RGBA'); P=(255,143,171); PD=(232,104,140); u=s/400
    d.ellipse([cx-150*u,cy+150*u,cx+150*u,cy+178*u],fill=(0,0,0,60))
    for sx in(-1,1):
        d.rounded_rectangle([cx+sx*80*u-34*u,cy+90*u,cx+sx*80*u+34*u,cy+165*u],18*u,fill=PD,outline=INK,width=int(7*u))
    d.ellipse([cx-185*u,cy-140*u,cx+185*u,cy+130*u],fill=P,outline=INK,width=int(8*u))
    for sx in(-1,1):
        d.polygon([(cx+sx*120*u,cy-110*u),(cx+sx*170*u,cy-190*u),(cx+sx*60*u,cy-135*u)],fill=PD,outline=INK)
    d.rounded_rectangle([cx-45*u,cy-150*u,cx+45*u,cy-136*u],6*u,fill=INK)          # coin slot
    d.ellipse([cx-62*u,cy-10*u,cx+62*u,cy+70*u],fill=PD,outline=INK,width=int(7*u))   # snout
    for sx in(-1,1): d.ellipse([cx+sx*24*u-11*u,cy+18*u,cx+sx*24*u+11*u,cy+44*u],fill=INK)
    ey=cy-62*u
    for sx in(-1,1):
        ex=cx+sx*78*u; r=34*u if mood=='shock' else 28*u
        d.ellipse([ex-r,ey-r,ex+r,ey+r],fill=(255,255,255),outline=INK,width=int(6*u))
        pr=13*u; d.ellipse([ex-pr+sx*-6*u,ey-pr,ex+pr+sx*-6*u,ey+pr],fill=INK); d.ellipse([ex-2*u,ey-9*u,ex+5*u,ey-2*u],fill=(255,255,255))
    if mood=='happy': d.arc([cx-40*u,cy+60*u,cx+40*u,cy+110*u],10,170,fill=INK,width=int(8*u))
    elif mood=='shock': d.ellipse([cx-18*u,cy+78*u,cx+18*u,cy+116*u],fill=INK)
    else: d.arc([cx-36*u,cy+86*u,cx+36*u,cy+126*u],190,350,fill=INK,width=int(8*u))
    for sx in(-1,1): d.ellipse([cx+sx*140*u-24*u,cy-6*u,cx+sx*140*u+24*u,cy+26*u],fill=(255,180,200,200))
def txt(im,xy,s,size,fill,stroke=INK,sw=10,anchor='mm',ang=0):
    f=F(size)
    if ang:
        tmp=Image.new('RGBA',(W,400),(0,0,0,0)); ImageDraw.Draw(tmp).text((W/2,200),s,font=f,fill=fill,stroke_width=sw,stroke_fill=stroke,anchor='mm'); tmp=tmp.rotate(ang,expand=True,resample=Image.BICUBIC); im.paste(tmp,(int(xy[0]-tmp.width/2),int(xy[1]-tmp.height/2)),tmp)
    else: ImageDraw.Draw(im).text(xy,s,font=f,fill=fill,stroke_width=sw,stroke_fill=stroke,anchor=anchor)
def bubble(im,box,s,size=64,tail=(0,0),fill=(255,255,255)):
    d=ImageDraw.Draw(im); x0,y0,x1,y1=box; d.rounded_rectangle(box,48,fill=fill,outline=INK,width=9)
    tx,ty=tail; d.polygon([(tx-40,y1-6),(tx+40,y1-6),(tx+(60 if tx>W/2 else -60),ty)],fill=fill,outline=INK); d.line([(tx-34,y1-5),(tx+34,y1-5)],fill=fill,width=12)
    f=F(size); lines=s.split('\n'); th=len(lines)*size*1.1; y=(y0+y1)/2-th/2+size*0.55
    for l in lines: d.text(((x0+x1)/2,y),l,font=f,fill=INK,anchor='mm'); y+=size*1.1
def cap(im,s,hi=None,y=1500):
    f=F(104); d=ImageDraw.Draw(im); words=s.split(); tw=sum(d.textlength(w+' ',font=f) for w in words); x=W/2-tw/2
    for w in words:
        col=(255,222,60) if w.strip('.,!?').upper()==(hi or '').upper() else (255,255,255)
        d.text((x,y),w,font=f,fill=col,stroke_width=12,stroke_fill=INK,anchor='ls'); x+=d.textlength(w+' ',font=f)
def brand(im): txt(im,(W-50,70),'RED FLAG ROCCO',44,(255,59,59),sw=6,anchor='rm')
def phone(im,x,y,w,h,lines):
    d=ImageDraw.Draw(im); d.rounded_rectangle([x,y,x+w,y+h],60,fill=INK); d.rounded_rectangle([x+18,y+18,x+w-18,y+h-18],46,fill=(245,247,250))
    yy=y+90
    for s,col,fc in lines:
        f=F(46); tw=d.textlength(s,font=f); d.rounded_rectangle([x+46,yy,x+46+tw+56,yy+92],34,fill=col); d.text((x+74,yy+46),s,font=f,fill=fc,anchor='lm'); yy+=118
# FRAME A - hook: bright yellow, client excited, Rocco deadpan
a=bg((255,214,64),(255,170,40),dots=(255,255,255),rays=(255,236,140)); brand(a)
phone(a,90,330,470,620,[('FREE GTA 6',(52,199,89),(255,255,255)),('for PC!!!',(52,199,89),(255,255,255)),('Tonight only',(255,59,59),(255,255,255))])
piggy(a,330,1180,420,'happy'); bubble(a,(60,120,640,300),'FREE GTA 6\nFOR PC?!',70,tail=(300,360))
rocco(a,'sideeye_05.webp',760,400,760); txt(a,(820,640),'RED FLAG.',120,(255,59,59),sw=14,ang=-8)
cap(a,'FREE DOWNLOAD?','FREE',1700); a.save('/tmp/mock/A.jpg',quality=92)
# FRAME B - fact: teal, big Rocco pointing, stamp
b=bg((64,201,198),(30,150,170),dots=(255,255,255)); brand(b)
d=ImageDraw.Draw(b)
for i,(nm,col) in enumerate([('PS5',(40,90,220)),('XBOX',(30,160,70)),('PC',(150,150,150))]):
    x=80+i*320; d.rounded_rectangle([x,300,x+280,620],40,fill=(255,255,255),outline=INK,width=9); txt(b,(x+140,420),nm,96,col,sw=0); 
    if nm=='PC': txt(b,(x+140,540),'NOPE',84,(255,59,59),sw=8,ang=-12); d.line([(x+20,320),(x+260,600)],fill=(255,59,59),width=16)
    else: txt(b,(x+140,540),'YES',84,(52,199,89),sw=8)
rocco(b,'point_04.webp',900,-60,700,flip=False); piggy(b,860,1330,300,'shock')
bubble(b,(560,760,1040,960),"There's NO\nPC version.",64,tail=(520,1040))
cap(b,'NO PC VERSION.','NO',1700); b.save('/tmp/mock/B.jpg',quality=92)
# FRAME C - safety step: fresh green, thumbs up
c=bg((178,236,120),(96,200,110),rays=(220,255,170)); brand(c)
d=ImageDraw.Draw(c); d.rounded_rectangle([90,260,990,700],60,fill=(255,255,255),outline=INK,width=10)
txt(c,(540,340),'YOUR MOVE',80,(255,59,59),sw=0); txt(c,(540,470),'Buy it ONLY in the',68,INK,sw=0); txt(c,(540,570),'console store',96,(30,140,70),sw=0)
d.ellipse([820,180,1000,360],fill=(52,199,89),outline=INK,width=10); d.line([(860,270),(900,312),(962,232)],fill=(255,255,255),width=22)
rocco(c,'thumbsup_04.webp',880,-40,720); piggy(c,850,1320,320,'happy')
cap(c,'STORE ONLY.','STORE',1700); c.save('/tmp/mock/C.jpg',quality=92)
# sheet: old vs new
old=Image.open('/tmp/cmp/t04_big.jpg').crop((0,0,270*3,480))
sh=Image.new('RGB',(3*360+40,640*2+120),(24,24,28)); dd=ImageDraw.Draw(sh)
dd.text((20,14),'HOZIRGI (qorong\'i, Rocco deyarli yo\'q)',font=F(40),fill=(255,120,120))
sh.paste(old.resize((1080,640)),(20,70))
dd.text((20,730),'TAKLIF (yorug\', Rocco + mijoz Penny, suhbat, hazil)',font=F(40),fill=(140,255,160))
for i,k in enumerate('ABC'): sh.paste(Image.open(f'/tmp/mock/{k}.jpg').resize((360,640)),(20+i*360,790))
sh.save('/tmp/mock/rocco_v2_mock.jpg',quality=90); print('ok')
