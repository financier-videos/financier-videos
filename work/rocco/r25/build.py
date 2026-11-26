import json
A="/home/user/financier-videos/assets/toon2d/"
SET={'P':A+'penny_attic.jpg','S':A+'slick_techdesk.jpg','R':A+'rocco_rooftop.jpg'}
lines=[
 ["S","[fast] [fake serious] Tech support! Your computer has a virus. Turn it on!"],
 ["P","[cheerful] Okay! ...It says two plus two is four."],
 ["S","[confused] That's a CALCULATOR!"],
 ["P","[proud] It's my computer! It's very fast at math."],
 ["S","[frustrated] The REAL computer! Download the app I'm sending you!"],
 ["P","[reading slowly] It says... 'Please insert floppy disk.'"],
 ["S","[panicked] What year is that computer?!"],
 ["P","[innocent] It's older than you, sweetie."],
 ["S","[furious] Forget it! Just tell me your bank password!"],
 ["P","[cheerful] Sure! It's... 'NiceTryFox.' All one word."],
 ["S","[defeated] ...That's actually a really good password."]]
S=lambda **k:k
shots=[]
for i,(w,t) in enumerate(lines):
    if w=="S": shots.append(S(line=i,**{"from":0},kind="slick",bg=SET['S'],bright=1.2,r_peek=True,s=["sly","panic","angry"][i%3],r="smug"))
    elif w=="P": shots.append(S(line=i,**{"from":0},kind="cu_p",bg=SET['P'],blur=1,p=["happy","shock","happy"][i%3],r="sideeye"))
    else: shots.append(S(line=i,**{"from":0},kind="cu_r",bg=SET['R'],blur=1,r="sideeye"))
shots[0].update(kind="call",bg=SET['P'],bg2=SET['S'],bright2=1.2,hook=None,caller='CALLER: "TECH SUPPORT"',s="sly",p="happy")
shots.insert(1,S(line=0,**{"from":0.55},kind="slick",bg=SET['S'],bright=1.2,r_peek=True,s="sly",r="sideeye",msg='"VIRUS DETECTED!"',msg_at=0.1))
spec={"topline":[{"t":"PENNY PLAYS DUMB: PART 3","at":0}],"speed":1.05,"id":"RC-25","title":"Penny Plays Dumb With a Tech Support Scammer","tail":1.8,
 "hot":["VIRUS","CALCULATOR","FLOPPY","PASSWORD"],"lines":lines,
 "sfx":[{"line":0,"word":"virus","name":"impact","gain":0.3},{"line":2,"frac":0.0,"name":"scratch","gain":0.25},{"line":5,"word":"floppy","name":"boing","gain":0.3},{"line":7,"word":"sweetie","name":"bonk","gain":0.35},{"line":10,"frac":0.6,"name":"wahwah","gain":0.35}],
 "sources":"FTC consumer advice on tech support scams: real tech companies don't call you about viruses or ask for remote access or passwords",
 "shots":shots}
json.dump(spec,open("rc25.json","w"),indent=1)
