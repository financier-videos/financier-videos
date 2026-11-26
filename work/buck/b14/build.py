import json
G="/tmp/fin/bg/b14/"
bk=lambda m:{"x":0.82,"y":0.99,"h":560,"mood":m}
host=lambda line,frm,mood,bg,st=1.0,prop=None:dict({"kind":"host","line":line,"from":frm,"buck":{"mood":mood,"h":1300,"y":1.04},"bg":G+bg,"bg_start":st,"dim":20},**({"prop":prop} if prop else {}))
lines=[
 ["B","[sly] [fast] Ten bucks a bet. Coin flips. You pick first."],
 ["B","[fast] You pick heads, heads, tails. I pick tails, heads, heads."],
 ["B","[confident] First one to show up wins. And I win three games out of four."],
 ["B","[deadpan] Here's the trick. Your heads-heads only wins if it lands first."],
 ["B","[fast] Any later, a tails came right before it. That's my combo. I finish first."],
 ["B","[happy] A hundred games. You win twenty-five. I win seventy-five."],
 ["B","[smug] You're down five hundred dollars. On a perfectly fair coin."],
 ["B","[whisper] So... ten bucks a bet. You pick first."]]
H=[255,205,60]; T=[80,200,220]; R=[235,64,52]
shots=[
 {"kind":"kinetic","line":0,"from":0,"words":[{"t":"$10","size":170,"c":[80,200,120]},{"t":"A FLIP","size":110}],"bg":G+"coin.mp4","bg_start":1.0},
 {"kind":"kinetic","line":0,"from":0.55,"words":[{"t":"YOU","size":130,"c":H},{"t":"PICK FIRST","size":100}],"bg":G+"dice_cube.mp4","bg_start":0.5},
 {"kind":"kinetic","line":1,"from":0,"words":[{"t":"YOU: H H T","size":130,"c":H}],"bg":G+"ludo.mp4","bg_start":1.0},
 {"kind":"kinetic","line":1,"from":0.5,"words":[{"t":"ME: T H H","size":130,"c":T}],"bg":G+"roulette.mp4","bg_start":1.0},
 {"kind":"kinetic","line":2,"from":0,"words":[{"t":"FIRST TO SHOW","size":110},{"t":"WINS","size":150,"c":H}],"bg":G+"chess.mp4","bg_start":1.0},
 host(2,0.45,"sly","carnival.mp4",1.0,"3 OUT OF 4"),
 {"kind":"kinetic","line":3,"from":0,"words":[{"t":"H H","size":160,"c":H},{"t":"ONLY ON FLIPS 1-2","size":90}],"bg":G+"piggy.mp4","bg_start":1.0},
 host(3,0.6,"point","bench.mp4",1.0),
 {"kind":"kinetic","line":4,"from":0,"words":[{"t":"T  H H","size":160,"c":T},{"t":"ALWAYS FIRST","size":100}],"bg":G+"coin.mp4","bg_start":5.0},
 host(4,0.6,"smug","roulette.mp4",4.0,"T + HH"),
 {"kind":"kinetic","line":5,"from":0,"words":[{"t":"100 GAMES","size":110}],"bg":G+"carousel.mp4","bg_start":1.0},
 {"kind":"kinetic","line":5,"from":0.35,"words":[{"t":"YOU 25","size":140,"c":H},{"t":"ME 75","size":140,"c":T}],"bg":G+"carousel.mp4","bg_start":3.0},
 host(5,0.65,"laugh","dice_cube.mp4",3.0),
 {"kind":"kinetic","line":6,"from":0,"words":[{"t":"YOUR WALLET","size":100},{"t":"-$500","size":170,"c":[235,64,52]}],"bg":G+"wallet.mp4","bg_start":1.0},
 host(6,0.6,"sideeye","carnival.mp4",6.0,"FAIR COIN"),
 {"kind":"kinetic","line":7,"from":0,"words":[{"t":"$10","size":170,"c":[80,200,120]},{"t":"YOU PICK FIRST","size":100}],"bg":G+"coin.mp4","bg_start":1.0}]
spec={"topline":[{"t":"THE RIGGED COIN BET","at":0}],"id":"BK-14","title":"I Win 3 Out of 4 Coin Flips. Here's the Trick.","brand":["FINANCIER",H],"tail":1.6,"speed":1.12,"amb":"room","grade":"teal",
 "lines":lines,"hot":["TAILS","HEADS","THREE","FOUR","SEVENTY-FIVE","TWENTY-FIVE","TRICK"],"cap_y":0.93,
 "pool":["b14_coin","b14_carnival","b14_piggy","b14_dice_cube","b14_carousel"],
 "sfx":[{"line":0,"frac":0.0,"name":"coin","gain":0.3},{"line":2,"frac":0.6,"name":"subboom","gain":0.3},{"line":5,"frac":0.5,"name":"coin","gain":0.3},{"line":6,"frac":0.0,"name":"boing","gain":0.3}],
 "sources":"Penney's game: W. Penney, Journal of Recreational Mathematics (1969); M. Gardner, Scientific American (Oct 1974). THH vs HHT: HHT wins only if flips 1-2 are HH (1/4); otherwise a T precedes the first HH, so THH completes first (3/4). 100 x $10: 25 wins (+$250) - 75 losses (-$750) = -$500 expected.",
 "shots":shots}
json.dump(spec,open("bk14.json","w"),indent=1)
