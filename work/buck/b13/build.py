import json
G="/tmp/fin/bg/"
bk=lambda m:{"x":0.82,"y":0.99,"h":560,"mood":m}
host=lambda line,frm,mood,bg,st=1.0,prop=None:dict({"kind":"host","line":line,"from":frm,"buck":{"mood":mood,"h":1300,"y":1.04},"bg":G+bg,"bg_start":st,"dim":20},**({"prop":prop} if prop else {}))
lines=[
 ["B","[announcer] [fast] Cyber Monday: fifteen billion dollars. Spend it at a hundred a day."],
 ["B","[fast] A hundred a day. One year? Thirty-six thousand five hundred."],
 ["B","[confident] A whole lifetime of shopping? About three million."],
 ["B","[nervous] That's... two hundredths of one percent of one Cyber Monday."],
 ["B","[shocked] You'd need four hundred thirteen thousand years."],
 ["B","[deadpan] Humans have only existed for about three hundred thousand. You'd start shopping before people were invented."],
 ["B","[deadpan] Online, America does it in one day. A hundred seventy-five thousand dollars a second."],
 ["B","[whisper] So... spend fifteen billion. At a hundred a day."]]
shots=[
 {"kind":"counter","line":0,"from":0,"start":15.1e9,"to":15.1e9,"dur":0.8,"label":"CYBER MONDAY 2026","size":110,"buck":bk("happy"),"bg":G+"rc2/mobank.mp4","bg_start":1.0},
 {"kind":"kinetic","line":0,"from":0.55,"words":[{"t":"$100","size":160,"c":[80,200,120]},{"t":"A DAY","size":110}],"bg":G+"t03/clouds.mp4","bg_start":1.0},
 {"kind":"counter","line":1,"from":0,"start":100,"to":36500,"dur":1.2,"label":"ONE YEAR","size":110,"buck":bk("proud"),"bg":G+"rc5/laptoptable.mp4","bg_start":1.0},
 host(1,0.6,"happy","rc/texting.mp4",1.0),
 {"kind":"counter","line":2,"from":0,"start":36500,"to":2920000,"dur":1.6,"label":"80 YEARS OF SHOPPING","size":110,"buck":bk("happy"),"bg":G+"rc5/workspace.mp4","bg_start":1.0},
 host(2,0.55,"proud","t03/stadium.mp4",1.0,"$2,920,000"),
 {"kind":"kinetic","line":3,"from":0,"words":[{"t":"0.02%","size":150,"c":[235,64,52]},{"t":"OF ONE DAY","size":100}],"bg":G+"r2/river.mp4","bg_start":1.0},
 host(3,0.55,"confused","rc5/vintage.mp4",1.0),
 {"kind":"kinetic","line":4,"from":0,"words":[{"t":"413,415","size":140,"c":[255,205,60]},{"t":"YEARS","size":110}],"bg":G+"gta/earth2.mp4","bg_start":1.0},
 host(4,0.5,"shocked","bank/earth_moons.mp4",1.0,"413,415 YRS"),
 {"kind":"bars","line":5,"from":0,"title":"YEARS AGO","items":[["HUMANS EXIST",300000,[80,160,90]],["YOUR SHOPPING STARTS",413415,[235,64,52]]],"new":1,"fmt":"{:,.0f}","suffix":" YRS","bg":G+"v01/oldforest.mp4","bg_start":1.0},
 host(5,0.6,"sideeye","v01/deer.mp4",1.0),
 {"kind":"counter","line":6,"from":0,"start":0,"to":174769,"dur":1.4,"label":"EVERY SECOND · ONLINE","size":110,"buck":bk("shocked"),"bg":G+"gta/moon.mp4","bg_start":1.0},
 host(6,0.55,"sly","rc4/sunset.mp4",1.0),
 {"kind":"counter","line":7,"from":0,"start":15.1e9,"to":15.1e9,"dur":0.8,"label":"CYBER MONDAY 2026","size":110,"buck":bk("happy"),"bg":G+"rc2/mobank.mp4","bg_start":3.0}]
spec={"topline":[{"t":"$15.1 BILLION · $100 A DAY","at":0}],"id":"BK-13","title":"Spend Cyber Monday's $15 Billion at $100 a Day","brand":["FINANCIER",[255,205,60]],"tail":1.6,"speed":1.15,"amb":"room","grade":"gold",
 "lines":lines,"hot":["BILLION","YEARS","HUMANS","SECOND"],"cap_y":0.93,
 "pool":["earth_globe","earth_night","city_night","typing_keys","moon_big","coins_fall"],
 "sfx":[{"line":0,"frac":0.0,"name":"coin","gain":0.3},{"line":1,"frac":0.5,"name":"coin","gain":0.3},{"line":2,"frac":0.6,"name":"coin","gain":0.3},{"line":4,"frac":0.0,"name":"subboom","gain":0.35},{"line":5,"word":"invented","name":"boing","gain":0.3}],
 "sources":"Adobe Digital Insights 2026 holiday forecast (Sept 28, 2026): Cyber Monday $15.1B; $15.1B/$100 = 151M days = 413,415 years; Homo sapiens ~300,000 years (Smithsonian Human Origins); $15.1B/86,400 = $174,769/s",
 "shots":shots}
json.dump(spec,open("bk13.json","w"),indent=1)
