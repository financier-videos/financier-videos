import json
B="/tmp/fin/bg/rc3/"
A="/home/user/financier-videos/assets/toon2d/"
SET={'P':A+'porch_boxes.jpg','S':A+'slick_van.jpg','R':A+'hallway_package.jpg'}
lines=[
 ["S","[fast] [fake friendly] Hi! Delivery company! Your Black Friday package is STUCK!"],
 ["P","[gasps] Oh no! Which package?"],
 ["S","[pause] [nervous] ...The... box one!"],
 ["R","[whispering] Psst. Play dumb again."],
 ["S","[sly] Just pay a tiny fee. Read me the long number on your card."],
 ["P","[proud] Okay! Three. Point. One. Four. One. Five. Nine..."],
 ["S","[angry] That's PI!"],
 ["P","[excited] Ooh, I love pie! Is it pumpkin?"],
 ["S","[frustrated] The CARD! Read the CARD!"],
 ["P","[reading slowly] It says... 'Penny's piggy bank card. Do not give to foxes.'"],
 ["S","[stammering] I'm not a fox! I'm a... delivery guy!"],
 ["P","[innocent] Then why is your tail sticking out of the phone?"],
 ["R","[whispering] [impressed] ...She's getting scary good at this."],
 ["S","[furious] Fine! Your package is CANCELLED!"],
 ["P","[cheerful] Good! I didn't order one!"],
 ["S","[pause] [defeated] ...Wait. What?"],
 ["R","[warmly] Real delivery companies don't call asking for your card. Didn't order it? Nothing to pay. Hang up."]]
S=lambda **k:k
shots=[]
mood={"S":["sly","panic","angry","sly"],"P":["happy","shock","happy","happy"],"R":["sideeye","smug"]}
for i,(w,t) in enumerate(lines):
    if w=="S":
        shots.append(S(line=i,**{"from":0},kind="slick",bg=SET['S'],bright=1.35,r_peek=True,s=["sly","panic","angry"][i%3],r="smug"))
    elif w=="P":
        shots.append(S(line=i,**{"from":0},kind="cu_p",bg=SET['P'],blur=1,p=["happy","shock","happy"][i%3],r="sideeye"))
    else:
        shots.append(S(line=i,**{"from":0},kind="cu_r",bg=SET['R'],blur=1,r="sideeye"))
shots[0].update(kind="call",bg=SET['P'],bg2=SET['S'],bright2=1.35,hook="PENNY PLAYS DUMB: PART 2",caller="CALLER: \"DELIVERY CO.\"",s="sly",p="happy")
shots.insert(1,S(line=0,**{"from":0.55},kind="slick",bg=SET['S'],bright=1.35,r_peek=True,s="sly",r="sideeye",msg="\"YOUR PACKAGE IS STUCK!\"",msg_at=0.1))
spec={"id":"RC-23","title":"Penny Plays Dumb With a Scammer: Part 2","tail":2.2,"hot":["PIE","CARD","FOXES","TAIL","CANCELLED"],
 "lines":lines,
 "sfx":[{"line":0,"frac":0.0,"name":"ding","gain":0.3},{"line":2,"frac":0.0,"name":"crickets","gain":0.25},{"line":6,"frac":0.0,"name":"scratch","gain":0.25},
        {"line":7,"word":"pumpkin","name":"boing","gain":0.3},{"line":9,"word":"foxes","name":"bonk","gain":0.35},{"line":11,"word":"tail","name":"boing","gain":0.3},
        {"line":13,"word":"cancelled","name":"buzzer","gain":0.2},{"line":15,"frac":0.0,"name":"crickets","gain":0.3},{"line":15,"frac":0.7,"name":"wahwah","gain":0.35},{"line":16,"frac":0.1,"name":"ding","gain":0.25}],
 "sources":"FTC consumer advice on fake delivery texts and calls; never give card numbers to unsolicited callers",
 "shots":shots}
json.dump(spec,open("rc23.json","w"),indent=1)
