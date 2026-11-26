import json
G="/tmp/fin/bg/b15/"
bk=lambda m:{"x":0.82,"y":0.99,"h":560,"mood":m}
host=lambda line,frm,mood,bg,st=1.0,prop=None:dict({"kind":"host","line":line,"from":frm,"buck":{"mood":mood,"h":1300,"y":1.04},"bg":G+bg,"bg_start":st,"dim":20},**({"prop":prop} if prop else {}))
lines=[
 ["B","[sly] [fast] One billion dollars. Spend a hundred grand a day."],
 ["B","[fast] A hundred thousand. Every single day. Cars, jets, whatever."],
 ["B","[confident] Spoiler: you never run out. Ever."],
 ["B","[deadpan] Park the billion somewhere boring. Four percent a year."],
 ["B","[shocked] That's forty million a year. A hundred and nine thousand a day."],
 ["B","[smug] You spend a hundred. The billion makes a hundred and nine."],
 ["B","[happy] Every year you end up richer than you started."],
 ["B","[whisper] So... one billion. A hundred grand a day."]]
Y=[255,205,60]; GR=[80,200,120]; R=[235,64,52]
shots=[
 {"kind":"kinetic","line":0,"from":0,"words":[{"t":"$1,000,000,000","size":120,"c":Y}],"bg":G+"vault.mp4","bg_start":1.0},
 {"kind":"kinetic","line":0,"from":0.5,"words":[{"t":"$100,000","size":150,"c":GR},{"t":"A DAY","size":110}],"bg":G+"gold.mp4","bg_start":1.0},
 {"kind":"kinetic","line":1,"from":0,"words":[{"t":"EVERY","size":110},{"t":"SINGLE DAY","size":120,"c":Y}],"bg":G+"bags.mp4","bg_start":1.0},
 {"kind":"kinetic","line":1,"from":0.55,"words":[{"t":"CARS · JETS","size":120}],"bg":G+"jet.mp4","bg_start":1.0},
 {"kind":"kinetic","line":2,"from":0,"words":[{"t":"YOU NEVER","size":120},{"t":"RUN OUT","size":160,"c":R}],"bg":G+"yacht.mp4","bg_start":1.0},
 host(2,0.6,"sly","mansion.mp4",1.0,"NEVER"),
 {"kind":"kinetic","line":3,"from":0,"words":[{"t":"4%","size":190,"c":GR},{"t":"A YEAR","size":110}],"bg":G+"hourglass.mp4","bg_start":1.0},
 host(3,0.6,"point","sunrise.mp4",1.0),
 {"kind":"kinetic","line":4,"from":0,"words":[{"t":"$40,000,000","size":130,"c":GR},{"t":"A YEAR","size":100}],"bg":G+"gold.mp4","bg_start":4.0},
 {"kind":"kinetic","line":4,"from":0.5,"words":[{"t":"$109,589","size":160,"c":Y},{"t":"A DAY","size":110}],"bg":G+"vault.mp4","bg_start":4.0},
 {"kind":"kinetic","line":5,"from":0,"words":[{"t":"SPEND $100K","size":120,"c":R},{"t":"EARN $109K","size":120,"c":GR}],"bg":G+"jet.mp4","bg_start":4.0},
 host(5,0.6,"smug","yacht.mp4",4.0,"+$9,589"),
 {"kind":"kinetic","line":6,"from":0,"words":[{"t":"RICHER","size":170,"c":Y},{"t":"EVERY YEAR","size":110}],"bg":G+"sunrise.mp4","bg_start":4.0},
 host(6,0.6,"laugh","mansion.mp4",4.0),
 {"kind":"kinetic","line":7,"from":0,"words":[{"t":"$100,000","size":150,"c":GR},{"t":"A DAY","size":110}],"bg":G+"vault.mp4","bg_start":1.0}]
spec={"topline":[{"t":"$1 BILLION · $100K A DAY","at":0}],"id":"BK-15","title":"Spend $100,000 a Day. You Never Run Out.","brand":["FINANCIER",Y],"tail":1.6,"speed":1.12,"amb":"room","grade":"cool",
 "lines":lines,"hot":["BILLION","NEVER","FOUR","FORTY","RICHER"],"cap_y":0.93,
 "pool":["b15_gold","b15_jet","b15_yacht","b15_sunrise","b15_hourglass"],
 "sfx":[{"line":0,"frac":0.0,"name":"coin","gain":0.3},{"line":2,"frac":0.3,"name":"subboom","gain":0.3},{"line":4,"frac":0.5,"name":"coin","gain":0.3}],
 "sources":"Assumption: 4% annual yield (illustrative; rates vary). $1B x 4% = $40M/yr; /365 = $109,589/day > $100,000/day spending -> principal grows by ~$3.5M/yr before taxes and inflation.",
 "shots":shots}
json.dump(spec,open("bk15.json","w"),indent=1)
