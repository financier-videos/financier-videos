import json
BK="/tmp/fin/bg/bank/"
bk=lambda m:{"x":0.82,"y":0.99,"h":560,"mood":m}
lines=[
 ["B","[game announcer] New game! Earn one billion dollars... at minimum wage."],
 ["B","[excited] Seven dollars and twenty-five cents an hour. Let's go!"],
 ["B","[fast] One day: fifty-eight bucks. One year: fifteen thousand."],
 ["B","[confident] Work your whole life. Forty-five years. Six hundred seventy-eight thousand!"],
 ["B","[nervous] That's... not even a tenth of one percent of a billion."],
 ["B","[shocked] You'd need sixty-six thousand years. Full time. No vacations."],
 ["B","[deadpan] Stonehenge is only about five thousand years old. You'd have to clock in before humans invented farming."],
 ["B","[sneaky] So how does anyone get a billion? Not by trading hours for dollars..."],
 ["B","[whisper] ...so, new game. Earn one billion dollars... at minimum wage."]]
shots=[
 {"kind":"pixel","line":0,"from":0,"hud_l":"GOAL","hud_r":"LV 1","start":1e9,"to":1e9,"msg":"EARN $1,000,000,000","buck":bk("happy"),"hook":"$1 BILLION AT MINIMUM WAGE?"},
 {"kind":"host","line":0,"from":0.55,"buck":{"mood":"proud","h":1300,"y":1.04},"bg":"/tmp/fin/bg/gta/clock.mp4","bg_start":0.5,"dim":20,"prop":"$7.25/HR"},
 {"kind":"counter","line":1,"from":0,"start":0,"to":7.25,"dur":1.2,"label":"PER HOUR","ticker":"+$7.25","rate":1.5,"buck":bk("happy"),"bg":BK+"coins_fall.mp4","bg_start":1.0},
 {"kind":"host","line":1,"from":0.6,"buck":{"mood":"happy","h":1300,"y":1.04},"bg":BK+"coffee_pour.mp4","bg_start":2.0,"dim":20},
 {"kind":"pixel","line":2,"from":0,"hud_l":"EARNED","hud_r":"DAY 1","start":0,"to":58,"dur":1.2,"msg":"ONE DAY","buck":bk("proud")},
 {"kind":"pixel","line":2,"from":0.5,"hud_l":"EARNED","hud_r":"YEAR 1","start":58,"to":15080,"dur":1.4,"msg":"ONE YEAR","buck":bk("proud")},
 {"kind":"pixel","line":3,"from":0,"hud_l":"EARNED","hud_r":"YEAR 45","start":15080,"to":678600,"dur":2.0,"msg":"A WHOLE CAREER","buck":bk("happy")},
 {"kind":"host","line":3,"from":0.55,"buck":{"mood":"proud","h":1300,"y":1.04},"bg":BK+"city_night.mp4","bg_start":1.0,"dim":20,"prop":"45 YEARS"},
 {"kind":"counter","line":4,"from":0,"start":0,"to":0.068,"dur":1.4,"label":"% OF A BILLION","sub":"0.068%","size":92,"buck":bk("confused"),"bg":BK+"earth_night.mp4","bg_start":3.0},
 {"kind":"host","line":4,"from":0.55,"buck":{"mood":"confused","h":1300,"y":1.04},"bg":BK+"typing_keys.mp4","bg_start":3.0,"dim":20},
 {"kind":"kinetic","line":5,"from":0,"words":[{"t":"66,313","size":220,"c":[255,205,60],"font":"Pixel"},{"t":"YEARS","size":120,"font":"Pixel"}],"bg":"/tmp/fin/bg/gta/earth.mp4","bg_start":2.0},
 {"kind":"host","line":5,"from":0.5,"buck":{"mood":"shocked","h":1300,"y":1.04},"bg":BK+"moon_big.mp4","bg_start":3.0,"dim":20,"prop":"66,313 YRS"},
 {"kind":"bars","line":6,"from":0,"title":"YEARS AGO","items":[["STONEHENGE",5000,[120,120,140]],["FARMING",12000,[80,160,90]],["YOUR FIRST SHIFT",66313,[235,64,52]]],"new":2,"bg":"/tmp/fin/bg/gta/clock.mp4","bg_start":3.0},
 {"kind":"host","line":6,"from":0.6,"buck":{"mood":"sideeye","h":1300,"y":1.04},"bg":BK+"cabin_empty.mp4","bg_start":1.0,"dim":20},
 {"kind":"host","line":7,"from":0,"buck":{"mood":"sly","h":1300,"y":1.04},"bg":BK+"cash_stacks.mp4","bg_start":7.0,"dim":20},
 {"kind":"pixel","line":8,"from":0,"hud_l":"GOAL","hud_r":"LV 1","start":1e9,"to":1e9,"msg":"EARN $1,000,000,000","buck":bk("happy")}]
spec={"id":"BK-11","title":"How Long to Earn $1 Billion at Minimum Wage?","brand":["FINANCIER",[255,205,60]],"tail":0.6,"speed":1.06,"amb":"room","grade":"gold",
 "lines":lines,"hot":["BILLION","MINIMUM","YEARS","FARMING"],"cap_y":0.93,"pool":["coins_fall","earth_night","city_night","typing_keys","coffee_pour","moon_big","cabin_empty","earth_globe"],
 "sfx":[{"line":0,"frac":0.0,"name":"coin","gain":0.3},{"line":2,"frac":0.3,"name":"coin","gain":0.3},{"line":3,"frac":0.6,"name":"coin","gain":0.3},{"line":5,"frac":0.0,"name":"subboom","gain":0.35},{"line":6,"word":"farming","name":"boing","gain":0.3}],
 "sources":"Federal minimum wage $7.25/h (US DOL); 2,080 h/year full time; $1B/$7.25 = 137.9M h = 66,313 years; Stonehenge ~5,000 years (English Heritage); farming ~12,000 years ago",
 "shots":shots}
json.dump(spec,open("bk11.json","w"),indent=1)
