import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="/tmp/claude-0/fonts/"; OUT=sys.argv[1]; AV=sys.argv[2]
INTER="/usr/share/fonts/opentype/inter/Inter-Bold.otf"; INTERM="/usr/share/fonts/opentype/inter/Inter-Medium.otf"
RED=(255,59,59); CREAM=(243,239,231); PAPER=(232,200,120); INK=(30,32,40)
def bg(w,h):
    c0=(26,48,78); c1=(10,20,35)
    im=Image.new("RGB",(w,h)); px=im.load(); cx,cy=w/2,h*0.42; R=math.hypot(max(cx,w-cx),max(cy,h-cy))
    for y in range(h):
        for x in range(w):
            t=min(1,math.hypot(x-cx,y-cy)/R); px[x,y]=tuple(int(c0[i]*(1-t)+c1[i]*t) for i in range(3))
    return im
def font(n,s): return ImageFont.truetype(n,s)
def ctext(d,y,txt,f,fill,w):
    tw=d.textlength(txt,font=f); d.text(((w-tw)/2,y),txt,font=f,fill=fill)
def rocco(size):
    a=Image.open(AV).convert("RGB"); m=Image.new("L",a.size,0); ImageDraw.Draw(m).rounded_rectangle((60,60,740,740),radius=200,fill=255)
    m=m.filter(ImageFilter.GaussianBlur(50)); a=a.resize((size,size)); return a, m.resize((size,size))
# 1 avatar (circle-safe)
W=1080; src=Image.open(AV).convert("RGB"); im=src.resize((W,W)).filter(ImageFilter.GaussianBlur(90))
cl=Image.new("RGB",(W,W)); cl.paste(src.crop((0,0,40,40)).resize((W,W)).filter(ImageFilter.GaussianBlur(5)))
bgm=bg(W,W); im=bgm
a=src.resize((840,840)); m=Image.new("L",(840,840),0); ImageDraw.Draw(m).rounded_rectangle((60,60,780,780),radius=200,fill=255); m=m.filter(ImageFilter.GaussianBlur(55))
im.paste(a,(120,110),m); im.save(OUT+"/redfrocco_avatar_1080.jpg",quality=95)
prev=im.copy(); mk=Image.new("L",(W,W),0); ImageDraw.Draw(mk).ellipse((0,0,W,W),fill=255)
p=Image.new("RGB",(W,W),(255,255,255)); p.paste(prev,(0,0),mk); p.resize((400,400)).save(OUT+"/_avatar_circle_preview.jpg")
def tag(d,x,y,txt,f):
    tw=d.textlength(txt,font=f); d.rectangle((x-18,y-10,x+tw+18,y+f.size+22),fill=PAPER); d.text((x,y),txt,font=f,fill=INK)
def stamp(im,txt,cx,cy,size=110,ang=-8):
    f=font(F+"BlackOpsOne-Regular.ttf",size); tmp=Image.new("RGBA",(1400,400),(0,0,0,0)); d=ImageDraw.Draw(tmp)
    tw=d.textlength(txt,font=f); x=(1400-tw)/2; d.rectangle((x-30,60,x+tw+30,60+size+70),outline=RED+(255,),width=12)
    d.text((x,90),txt,font=f,fill=RED+(255,)); tmp=tmp.rotate(ang,resample=Image.BICUBIC); im.paste(tmp,(int(cx-700),int(cy-200)),tmp)
def brand(d,w):
    f=font(F+"BlackOpsOne-Regular.ttf",40); t="RED FLAG ROCCO"; d.text((w-d.textlength(t,font=f)-50,50),t,font=f,fill=RED)
    d.rectangle((0,0,w,10),fill=RED)
W,H=1080,1350
# Post 1: meet rocco
im=bg(W,H); d=ImageDraw.Draw(im); brand(d,W)
a,m=rocco(620); im.paste(a,(230,190),m)
ctext(d,850,"MEET ROCCO",font(F+"BlackOpsOne-Regular.ttf",120),CREAM,W)
ctext(d,1000,"A raccoon detective who spots scams",font(INTER,46),CREAM,W)
ctext(d,1060,"so you don't fall for them.",font(INTER,46),CREAM,W)
ctext(d,1170,"1 scam · its red flags · 1 safety step",font(F+"CourierPrime-Bold.ttf",40),PAPER,W)
im.save(OUT+"/post1_meet_rocco.jpg",quality=93)
# Post 2: 4 signs (FTC)
im=bg(W,H); d=ImageDraw.Draw(im); brand(d,W)
tag(d,70,110,"CASE FILE",font(INTER,28))
d.text((70,190),"4 SIGNS",font=font(F+"BlackOpsOne-Regular.ttf",130),fill=CREAM)
d.text((70,340),"IT'S A SCAM",font=font(F+"BlackOpsOne-Regular.ttf",130),fill=RED)
items=[("1","They PRETEND to be someone","you trust (a bank, the IRS, a store)."),
       ("2","There's a PROBLEM or a PRIZE","that needs you right now."),
       ("3","They PRESSURE you","to act before you can think."),
       ("4","They tell you HOW to pay:","gift cards, crypto, wire, an app.")]
y=540; fb=font(INTER,44); fm=font(INTERM,38)
for n,l1,l2 in items:
    d.ellipse((70,y,150,y+80),fill=RED); ctext_n=d.textlength(n,font=fb); d.text((110-ctext_n/2,y+12),n,font=fb,fill=(255,255,255))
    d.text((185,y+2),l1,font=fb,fill=CREAM); d.text((185,y+58),l2,font=fm,fill=(200,205,215)); y+=165
d.text((70,1245),"Source: FTC, \"How To Avoid a Scam\" (consumer.ftc.gov)",font=font(INTERM,30),fill=(170,178,190))
im.save(OUT+"/post2_4_signs.jpg",quality=93)
# Post 3: where to report
im=bg(W,H); d=ImageDraw.Draw(im); brand(d,W)
tag(d,70,110,"CASE FILE",font(INTER,28))
d.text((70,190),"GOT SCAMMED?",font=font(F+"BlackOpsOne-Regular.ttf",110),fill=CREAM)
d.text((70,320),"REPORT IT (U.S.)",font=font(F+"BlackOpsOne-Regular.ttf",86),fill=RED)
rows=[("ReportFraud.ftc.gov","Federal Trade Commission — any scam"),
      ("ic3.gov","FBI Internet Crime Complaint Center"),
      ("877-908-3360","AARP Fraud Watch Network Helpline (free)")]
y=520
for big,small in rows:
    d.rounded_rectangle((70,y,1010,y+170),radius=24,fill=(20,30,50),outline=PAPER,width=4)
    d.text((110,y+28),big,font=font(F+"CourierPrime-Bold.ttf",58),fill=PAPER); d.text((110,y+108),small,font=font(INTERM,34),fill=CREAM); y+=210
ctext(d,1180,"Lost money? Call your bank first.",font(INTER,44),CREAM,W)
im.save(OUT+"/post3_report.jpg",quality=93)
# Highlight covers 1080x1920 (centre-safe circle)
for name,txt,sub in [("hl_scams","SCAMS","case files"),("hl_flags","RED FLAGS","how to spot"),("hl_report","REPORT","where to go"),("hl_about","ROCCO","who's this?")]:
    im=bg(1080,1920); d=ImageDraw.Draw(im); d.ellipse((240,660,840,1260),fill=(20,30,50),outline=RED,width=14)
    f=font(F+"BlackOpsOne-Regular.ttf",120 if len(txt)<7 else 86); ctext(d,890 if len(txt)<7 else 905,txt,f,CREAM,1080)
    ctext(d,1050,sub,font(F+"CourierPrime-Bold.ttf",50),PAPER,1080); im.save(OUT+"/%s.jpg"%name,quality=92)
