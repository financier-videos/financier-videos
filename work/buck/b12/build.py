import json
G="/tmp/fin/bg/"
bk=lambda m:{"x":0.82,"y":0.99,"h":560,"mood":m}
host=lambda line,frm,mood,bg,st=1.0,prop=None:dict({"kind":"host","line":line,"from":frm,"buck":{"mood":mood,"h":1300,"y":1.04},"bg":G+bg,"bg_start":st,"dim":20},**({"prop":prop} if prop else {}))
lines=[
 ["B","[announcer] [fast] Black Friday: a hundred forty-nine thousand dollars. Every second."],
 ["B","[fast] In the time it takes me to say this sentence, about a million dollars. Gone."],
 ["B","[excited] One minute? Almost nine million."],
 ["B","[shocked] One hour? Five hundred and thirty-seven million dollars."],
 ["B","[deadpan] By midnight: twelve point nine billion. Online. In one day."],
 ["B","[sneaky] And that's not even the biggest day. Cyber Monday is expected to hit fifteen billion."],
 ["B","[deadpan] That's more every second than a typical full-time worker earns in two years."],
 ["B","[whisper] Since this video started, about six million dollars. Every. Single. Second."]]
shots=[
 {"kind":"counter","line":0,"from":0,"start":0,"to":149306,"dur":1.6,"label":"SPENT ONLINE · EVERY SECOND","size":120,"buck":bk("shocked"),"bg":G+"r/mall.mp4","bg_start":1.0,"hook":None},
 host(0,0.45,"proud","r/crowd.mp4",2.0),
 {"kind":"counter","line":0,"from":0.75,"start":0,"to":149306,"dur":0.8,"label":"EVERY SECOND","size":120,"buck":bk("happy"),"bg":G+"rc2/phonehand.mp4","bg_start":1.0},
 {"kind":"counter","line":1,"from":0,"start":0,"to":1000000,"dur":3.0,"label":"WHILE BUCK TALKS","ticker":"+$149,306","rate":3,"buck":bk("confused"),"bg":G+"r/online.mp4","bg_start":1.0},
 host(1,0.55,"shocked","r01/conveyor.mp4",1.0),
 {"kind":"counter","line":2,"from":0,"start":0,"to":8958000,"dur":1.4,"label":"ONE MINUTE","size":120,"buck":bk("happy"),"bg":G+"r/cart.mp4","bg_start":1.0},
 host(2,0.6,"happy","r01/boxline.mp4",2.0),
 {"kind":"counter","line":3,"from":0,"start":8958000,"to":537500000,"dur":1.6,"label":"ONE HOUR","size":110,"buck":bk("shocked"),"bg":G+"r01/courier.mp4","bg_start":1.0},
 host(3,0.55,"shocked","t03/nightcity.mp4",2.0,"$537,500,000"),
 {"kind":"kinetic","line":4,"from":0,"words":[{"t":"$12.9","size":180,"c":[255,205,60]},{"t":"BILLION","size":120}],"bg":G+"bank/city_fireworks.mp4","bg_start":1.0},
 host(4,0.5,"sideeye","r01/openbox.mp4",1.0),
 {"kind":"bars","line":5,"from":0,"title":"ADOBE 2026 FORECAST","items":[["THANKSGIVING",6.9,[120,120,140]],["BLACK FRIDAY",12.9,[235,64,52]],["CYBER MONDAY",15.1,[80,160,240]]],"new":2,"fmt":"${:,.1f}","suffix":"B","bg":G+"rc/loadbar.mp4","bg_start":1.0},
 host(5,0.6,"sly","rc2/card.mp4",1.0),
 {"kind":"kinetic","line":6,"from":0,"words":[{"t":"$149,306","size":150,"c":[255,205,60]},{"t":"> 2 YEARS OF PAY","size":100}],"bg":G+"rc2/scroll.mp4","bg_start":1.0},
 host(6,0.5,"sideeye","r/store.mp4",1.0),
 {"kind":"counter","line":7,"from":0,"start":0,"to":6000000,"dur":2.0,"label":"SINCE THIS VIDEO STARTED","size":110,"buck":bk("sly"),"bg":G+"rc/confetti.mp4","bg_start":0.5},
 {"kind":"counter","line":7,"from":0.65,"start":0,"to":149306,"dur":0.8,"label":"EVERY SECOND","size":120,"buck":bk("happy"),"bg":G+"r/mall.mp4","bg_start":4.0}]
spec={"topline":[{"t":"BLACK FRIDAY · ONLINE · USA","at":0}],"id":"BK-12","title":"Black Friday Spends $149,306 Every Second","brand":["FINANCIER",[255,205,60]],"tail":0.6,"speed":1.12,"amb":"room","grade":"warm",
 "lines":lines,"hot":["SECOND","MILLION","BILLION","CYBER"],"cap_y":0.93,
 "sfx":[{"line":0,"word":"second","name":"coin","gain":0.3},{"line":1,"word":"gone","name":"whip","gain":0.3},{"line":3,"frac":0.0,"name":"subboom","gain":0.35},{"line":4,"word":"billion","name":"impact","gain":0.3},{"line":6,"frac":0.3,"name":"impact","gain":0.3}],
 "sources":"Adobe Digital Insights 2026 holiday forecast (Sept 28, 2026): Black Friday $12.9B, Cyber Monday $15.1B, Thanksgiving $6.9B; $12.9B/86,400 s = $149,306/s; BLS Q3 2026 median usual weekly earnings, full-time: $1,232 (Oct 21, 2026) x 104 weeks = $128,128 < $149,306",
 "shots":shots}
json.dump(spec,open("bk12.json","w"),indent=1)
