import json
B="/tmp/fin/bg/rc3/"
A="/home/user/financier-videos/assets/toon2d/"
SET={'P':A+'penny_kitchen.jpg','S':A+'slick_refunds.jpg','R':A+'rocco_study.jpg'}
lines=[
 ["S","[sly] [fast] Oops! I refunded you two THOUSAND instead of two hundred! Send back eighteen hundred in gift cards, please!"],
 ["P","[happy] Ooh! Let me check my bank app!"],
 ["P","[reading] It says... zero new dollars."],
 ["S","[nervous] It's... pending! Very, very pending!"],
 ["R","[whispering] Psst. She's onto him."],
 ["P","[innocent] Okay! I'll send it back the same way you sent it."],
 ["S","[confused] ...How?"],
 ["P","[cheerful] Refunds go back to the card they came from! So... what's YOUR card number?"],
 ["S","[panicked] What? No!"],
 ["P","[sweetly] But it's for your refund!"],
 ["S","[furious] I'm hanging up!"],
 ["P","[innocent] ...Was it something I said?"]]
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
shots[0].update(kind="call",bg=SET['P'],bg2=SET['S'],bright2=1.35,hook="POV: A SCAMMER TRIES THE REFUND TRICK",caller="CALLER: \"REFUND DEPT.\"",s="sly",p="happy")
shots.insert(1,S(line=0,**{"from":0.55},kind="slick",bg=SET['S'],bright=1.35,r_peek=True,s="sly",r="sideeye",msg="\"REFUND: $200!\"",msg_at=0.1))
spec={"id":"RC-24","title":"The Scammer Tried the Refund Trick on Penny","tail":2.2,"hot":["REFUND","THOUSAND","ZERO","PENDING","CARD"],
 "lines":lines,
 "sfx":[{"line":0,"word":"thousand","name":"impact","gain":0.3},{"line":2,"word":"zero","name":"crickets","gain":0.3},{"line":3,"word":"pending","name":"boing","gain":0.3},{"line":7,"word":"number","name":"bonk","gain":0.35},{"line":8,"frac":0.0,"name":"scratch","gain":0.3},{"line":10,"frac":0.6,"name":"wahwah","gain":0.35},{"line":11,"frac":0.2,"name":"ding","gain":0.25}],
 "sources":"FTC consumer advice on refund and overpayment scams",
 "shots":shots}
json.dump(spec,open("rc24.json","w"),indent=1)
