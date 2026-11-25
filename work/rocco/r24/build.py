import json
B="/tmp/fin/bg/rc3/"
lines=[
 ["S","[sly] [fake friendly] Hi! You were overcharged. I'm refunding you two hundred dollars!"],
 ["P","[happy] Ooh, yay!"],
 ["S","[fast] Oops! My finger slipped! I sent you two THOUSAND! Send back eighteen hundred in gift cards, please!"],
 ["R","[whispering] Psst. Open your real bank app."],
 ["P","[reading] My bank app says... zero new dollars."],
 ["S","[nervous] It's... pending! Very, very pending!"],
 ["P","[innocent] Okay! I'll send it back the same way you sent it."],
 ["S","[confused] ...How?"],
 ["P","[cheerful] Refunds go back to the card they came from! So... what's YOUR card number?"],
 ["S","[panicked] What? No!"],
 ["P","[sweetly] But it's for your refund!"],
 ["S","[furious] I'm hanging up!"],
 ["R","[warmly] A real refund never comes with 'send the extra back.' Check your bank app yourself. Never the screen they show you."]]
S=lambda **k:k
shots=[]
mood={"S":["sly","panic","angry","sly"],"P":["happy","shock","happy","happy"],"R":["sideeye","smug"]}
for i,(w,t) in enumerate(lines):
    if w=="S":
        shots.append(S(line=i,**{"from":0},kind="slick",bg=B+"animeoffice.mp4",bright=1.35,r_peek=True,s=["sly","panic","angry"][i%3],r="smug"))
    elif w=="P":
        shots.append(S(line=i,**{"from":0},kind="cu_p",bg=B+"rainroom.mp4",blur=1,p=["happy","shock","happy"][i%3],r="sideeye"))
    else:
        shots.append(S(line=i,**{"from":0},kind="cu_r",bg=B+"fireplace.mp4",blur=1,r="sideeye"))
shots[0].update(kind="call",bg=B+"rainroom.mp4",bg2=B+"animeoffice.mp4",bright2=1.35,hook="POV: A SCAMMER TRIES THE REFUND TRICK",caller="CALLER: \"REFUND DEPT.\"",s="sly",p="happy")
shots.insert(1,S(line=0,**{"from":0.55},kind="slick",bg=B+"animeoffice.mp4",bright=1.35,r_peek=True,s="sly",r="sideeye",msg="\"REFUND: $200!\"",msg_at=0.1))
spec={"id":"RC-24","title":"The Scammer Tried the Refund Trick on Penny","tail":2.2,"hot":["REFUND","THOUSAND","ZERO","PENDING","CARD"],
 "lines":lines,
 "sfx":[{"line":0,"frac":0.0,"name":"ding","gain":0.3},{"line":2,"word":"thousand","name":"impact","gain":0.3},{"line":4,"word":"zero","name":"crickets","gain":0.3},{"line":5,"word":"pending","name":"boing","gain":0.3},{"line":8,"word":"number","name":"bonk","gain":0.35},{"line":9,"frac":0.0,"name":"scratch","gain":0.3},{"line":11,"frac":0.6,"name":"wahwah","gain":0.35},{"line":12,"frac":0.1,"name":"ding","gain":0.25}],
 "sources":"FTC consumer advice on refund and overpayment scams",
 "shots":shots}
json.dump(spec,open("rc24.json","w"),indent=1)
