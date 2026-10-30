import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
stats = json.loads((ROOT / 'stats.json').read_text(encoding='utf-8'))
W,H = 1200, 620
im = Image.new('RGB',(W,H),'#0c110d')
d = ImageDraw.Draw(im)
GOLD='#d6b77d'; WHITE='#e7e9de'; MUTED='#a9b5a1'; GREEN='#243324'; EDGE='#4a6044'
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
boldpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def font(n,bold=False):
    p=boldpath if bold else fontpath
    return ImageFont.truetype(p,n)
def label(x,y,t,size=22,color=WHITE,bold=False): d.text((x,y),str(t),font=font(size,bold),fill=color)
def num(v): return f'{int(v):,}'
d.rounded_rectangle((8,8,W-8,H-8),radius=26,outline=EDGE,width=3)
label(55,39,'TA1CCM  /  FIELD OPERATIONS',24,GOLD,True)
label(55,84,'POTA STATISTICS',43,WHITE,True)
d.line((55,148,1145,148),fill=EDGE,width=2)
items=[('ACTIVATOR QSOs',stats['activator']['qsos']),('PARKS ACTIVATED',stats['activator']['parks']),('ACTIVATIONS',stats['activator']['activations'])]
for i,(name,value) in enumerate(items):
    x=55+i*370
    d.rounded_rectangle((x,177,x+350,353),radius=17,fill=GREEN,outline=EDGE,width=2)
    label(x+25,205,name,18,MUTED,True)
    label(x+25,248,num(value),53,GOLD,True)
label(55,397,'HUNTER',22,GOLD,True)
label(55,441,f"{num(stats['hunter']['parks'])} parks",28,WHITE,True)
label(330,441,f"{num(stats['hunter']['qsos'])} QSOs",28,WHITE,True)
label(690,397,'AWARDS',22,GOLD,True)
label(690,441,num(stats.get('awards',0)),28,WHITE,True)
label(880,397,'ENDORSEMENTS',22,GOLD,True)
label(880,441,num(stats.get('endorsements',0)),28,WHITE,True)
d.line((55,520,1145,520),fill=EDGE,width=2)
updated=stats.get('updated_utc','')[:19].replace('T',' ') + ' UTC'
label(55,545,'DATA: PARKS ON THE AIR',19,MUTED)
label(760,545,'UPDATED: '+updated,17,MUTED)
im.save(ROOT / 'pota-stats.png',optimize=True)
print('Generated pota-stats.png')
