"""Иллюстрации мастерской для раздела «О нас» / «О студии».

    python tools/studio_illustrations.py a   — seed/a/media/studio-*.svg
    python tools/studio_illustrations.py d   — seed/d/media/studio-*.svg

Рисует четыре сцены (у окна, рабочий стол, стена с работами, стеллаж с материалами)
в палитре сайта. На мольберт и стены подставляются обложки из seed/<site>/media.
SVG переводится в JPG браузером (см. tools/render_svg.js) — результат кладется рядом.
Это иллюстрации, а не фотографии: в админке у них включен флаг «Иллюстрация».
"""
import base64
import random
import sys
from pathlib import Path

W, H = 1600, 1200
ROOT = Path(__file__).resolve().parent.parent

PALETTES = {
    "a": {
        "wall": "#eef4fa", "wall2": "#dcebf6", "floor1": "#e2d3bd", "floor2": "#cdb897", "plank": "#bda27c",
        "wood": "#b08a5e", "wood2": "#8c6a43", "ink": "#1c497e", "ink2": "#073662", "accent": "#e3bf58",
        "sky1": "#bcd8f0", "sky2": "#f7fbff", "light": "#fff8e6", "cloth": "#f7f3ea", "plant": "#5f8f76",
        "plant2": "#3f6f5a", "pot": "#d9d3c7", "rug": "#c9dcee", "rug2": "#1c497e", "shadow": "7,54,98",
        "paints": ["#1c497e", "#3f7cc0", "#e3bf58", "#e8e2d4", "#b84a3a", "#5f8f76", "#073662", "#f2c9a0"],
    },
    "d": {
        "wall": "#f1eee4", "wall2": "#e3dfd1", "floor1": "#c9bda8", "floor2": "#a89a82", "plank": "#978870",
        "wood": "#8a6a4a", "wood2": "#5e4631", "ink": "#171a17", "ink2": "#000000", "accent": "#e7f36a",
        "sky1": "#dcdad0", "sky2": "#f7f5ee", "light": "#fffbe8", "cloth": "#ebe8dd", "plant": "#6b7d52",
        "plant2": "#465533", "pot": "#79352f", "rug": "#d6d2c3", "rug2": "#79352f", "shadow": "23,26,23",
        "paints": ["#171a17", "#79352f", "#e7f36a", "#f1eee4", "#c2703d", "#6b7d52", "#3b4a6b", "#d9a441"],
    },
}


def embed(path):
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


def defs(p):
    s = p["shadow"]
    return f"""
<defs>
  <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['wall']}"/><stop offset="1" stop-color="{p['wall2']}"/></linearGradient>
  <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['floor2']}"/><stop offset="1" stop-color="{p['floor1']}"/></linearGradient>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{p['sky1']}"/><stop offset="1" stop-color="{p['sky2']}"/></linearGradient>
  <linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['light']}" stop-opacity=".75"/><stop offset="1" stop-color="{p['light']}" stop-opacity="0"/></linearGradient>
  <linearGradient id="woodg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{p['wood2']}"/><stop offset=".5" stop-color="{p['wood']}"/><stop offset="1" stop-color="{p['wood2']}"/></linearGradient>
  <linearGradient id="table" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{p['wood']}"/><stop offset="1" stop-color="{p['wood2']}"/></linearGradient>
  <radialGradient id="spot" cx=".5" cy="0" r="1"><stop offset="0" stop-color="{p['light']}" stop-opacity=".9"/><stop offset="1" stop-color="{p['light']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="vign" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="rgb({s})" stop-opacity="0"/><stop offset="1" stop-color="rgb({s})" stop-opacity=".22"/></radialGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="14"/></filter>
  <filter id="soft2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
  <filter id="wc" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".018" numOctaves="3" seed="4" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="7"/>
  </filter>
  <filter id="paper" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="7"/>
    <feColorMatrix values="0 0 0 0 .5  0 0 0 0 .45  0 0 0 0 .4  0 0 0 .09 0"/>
  </filter>
  <filter id="blotch" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".004" numOctaves="3" seed="11"/>
    <feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .18 -.04"/>
  </filter>
</defs>"""


def finish():
    return f'<rect width="{W}" height="{H}" filter="url(#blotch)"/><rect width="{W}" height="{H}" fill="url(#vign)"/><rect width="{W}" height="{H}" filter="url(#paper)"/>'


def planks(p, y0, rnd, count=14):
    out = [f'<rect x="0" y="{y0}" width="{W}" height="{H - y0}" fill="url(#floor)"/>']
    vx = W * 0.55
    for i in range(-count, count * 2):
        x = vx + i * 140
        out.append(f'<line x1="{vx + (x - vx) * 0.25:.0f}" y1="{y0}" x2="{x:.0f}" y2="{H}" stroke="{p["plank"]}" stroke-width="2" opacity=".55"/>')
    for j in range(6):
        y = y0 + (H - y0) * (j / 6) ** 1.6
        out.append(f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{p["plank"]}" stroke-width="1.2" opacity=".25"/>')
    return "".join(out)


def framed(x, y, w, h, img, p, frame="#ffffff", depth=18, mat=0):
    s = p["shadow"]
    inner = f'<image href="{img}" x="{x + mat}" y="{y + mat}" width="{w - 2 * mat}" height="{h - 2 * mat}" preserveAspectRatio="xMidYMid slice"/>'
    return (f'<rect x="{x + 10}" y="{y + 16}" width="{w}" height="{h}" fill="rgba({s},.28)" filter="url(#soft2)"/>'
            f'<rect x="{x - depth / 2}" y="{y - depth / 2}" width="{w + depth}" height="{h + depth}" fill="{frame}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>{inner}'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="rgba(0,0,0,.18)" stroke-width="2"/>')


def brush(x, y, length, angle, p, color, rnd):
    handle = rnd.choice([p["wood"], p["ink"], p["wood2"], "#d9cbb3"])
    return (f'<g transform="translate({x} {y}) rotate({angle})">'
            f'<rect x="0" y="-5" width="{length}" height="10" rx="5" fill="{handle}"/>'
            f'<rect x="{length}" y="-6" width="34" height="12" fill="#c9c9c9"/><rect x="{length}" y="-6" width="34" height="4" fill="#e8e8e8"/>'
            f'<path d="M{length + 34} -7 q30 7 44 7 q-14 0 -44 7z" fill="#3a2d20"/>'
            f'<path d="M{length + 60} -3 q16 3 20 3 q-4 0 -20 3z" fill="{color}"/></g>')


def plant(x, y, p, scale=1.0):
    leaves = []
    rnd = random.Random(3)
    for i in range(16):
        a = -160 + i * 9 + rnd.uniform(-6, 6)
        l = rnd.uniform(90, 170) * scale
        c = p["plant"] if i % 2 else p["plant2"]
        leaves.append(f'<path d="M0 0 q{l * 0.3:.0f} -{l * 0.5:.0f} 0 -{l:.0f} q-{l * 0.3:.0f} {l * 0.5:.0f} 0 {l:.0f}z" fill="{c}" transform="rotate({a + 90:.0f})"/>')
    return (f'<g transform="translate({x} {y})">{"".join(leaves)}'
            f'<path d="M-{60 * scale} 0 h{120 * scale} l-{14 * scale} {110 * scale} h-{92 * scale}z" fill="{p["pot"]}"/>'
            f'<rect x="-{66 * scale}" y="-8" width="{132 * scale}" height="18" fill="{p["pot"]}" opacity=".85"/></g>')


# --- сцены ---------------------------------------------------------------------

def scene_window(p, covers, rnd):
    y0 = 830
    s = p["shadow"]
    parts = [f'<rect width="{W}" height="{y0}" fill="url(#wall)"/>', planks(p, y0, rnd)]
    # окно
    wx, wy, ww, wh = 150, 120, 470, 620
    parts.append(f'<rect x="{wx - 26}" y="{wy - 26}" width="{ww + 52}" height="{wh + 52}" fill="#ffffff" opacity=".9"/>')
    parts.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" fill="url(#sky)"/>')
    for cx, cy, r in ((260, 250, 60), (330, 230, 80), (420, 260, 55), (500, 420, 40), (560, 400, 60)):
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#ffffff" opacity=".7" filter="url(#soft2)"/>')
    parts.append(f'<path d="M{wx} {wy + wh * .78} q120 -60 230 -20 t240 -40 v{wh * .22 + 40} h-{ww}z" fill="{p["plant2"]}" opacity=".35"/>')
    parts.append(f'<rect x="{wx + ww / 2 - 7}" y="{wy}" width="14" height="{wh}" fill="#ffffff"/><rect x="{wx}" y="{wy + wh * .42}" width="{ww}" height="14" fill="#ffffff"/>')
    parts.append(f'<rect x="{wx - 44}" y="{wy + wh + 20}" width="{ww + 88}" height="26" fill="#ffffff"/><rect x="{wx - 44}" y="{wy + wh + 46}" width="{ww + 88}" height="10" fill="rgba({s},.12)"/>')
    # луч света на пол
    parts.append(f'<polygon points="{wx},{wy + wh} {wx + ww},{wy + wh} {wx + ww + 520},{H} {wx + 120},{H}" fill="url(#beam)" opacity=".8"/>')
    # ковер
    parts.append(f'<ellipse cx="1000" cy="1040" rx="470" ry="95" fill="{p["rug"]}"/><ellipse cx="1000" cy="1040" rx="420" ry="75" fill="none" stroke="{p["rug2"]}" stroke-width="5" opacity=".45"/>')
    # мольберт
    ex = 1010
    parts.append(f'<ellipse cx="{ex}" cy="1045" rx="260" ry="30" fill="rgba({s},.25)" filter="url(#soft2)"/>')
    parts.append(f'<path d="M{ex - 150} 1050 L{ex - 10} 180 L{ex + 10} 180 L{ex - 125} 1050z" fill="url(#woodg)"/>')
    parts.append(f'<path d="M{ex + 150} 1050 L{ex + 10} 180 L{ex - 10} 180 L{ex + 125} 1050z" fill="url(#woodg)"/>')
    parts.append(f'<path d="M{ex - 8} 200 L{ex + 55} 1010 L{ex + 72} 1010 L{ex + 8} 200z" fill="{p["wood2"]}" opacity=".8"/>')
    parts.append(f'<rect x="{ex - 190}" y="800" width="380" height="24" fill="{p["wood"]}"/><rect x="{ex - 190}" y="824" width="380" height="8" fill="{p["wood2"]}"/>')
    parts.append(framed(ex - 230, 300, 460, 490, covers[0], p, frame=p["cloth"], depth=22))
    parts.append(f'<rect x="{ex - 40}" y="270" width="80" height="26" fill="{p["wood"]}"/>')
    # холсты у стены
    for i in range(3):
        parts.append(f'<rect x="{1280 + i * 40}" y="{540 + i * 20}" width="230" height="{290 - i * 20}" fill="{p["cloth"]}" stroke="{p["wood2"]}" stroke-width="10" transform="rotate({-4 + i * 2} {1380} 830)"/>')
    # табурет с банкой кистей
    tx, ty = 1400, 930
    parts.append(f'<ellipse cx="{tx}" cy="{ty}" rx="95" ry="26" fill="{p["wood"]}"/><rect x="{tx - 80}" y="{ty}" width="12" height="190" fill="{p["wood2"]}"/><rect x="{tx + 68}" y="{ty}" width="12" height="190" fill="{p["wood2"]}"/><rect x="{tx - 8}" y="{ty + 10}" width="12" height="185" fill="{p["wood2"]}"/>')
    for i, c in enumerate(p["paints"][:5]):
        parts.append(brush(tx - 28 + i * 13, ty - 40, 150, -104 + i * 7, p, c, rnd))
    parts.append(f'<path d="M{tx - 48} {ty - 70} h96 l-8 74 h-80z" fill="#ffffff" opacity=".55" stroke="rgba(0,0,0,.15)"/>')
    # растение и холсты у стены
    parts.append(plant(720, 760, p, 1.0))
    parts.append(finish())
    return parts


def scene_table(p, covers, rnd):
    s = p["shadow"]
    parts = [f'<rect width="{W}" height="{H}" fill="url(#table)"/>']
    for i in range(9):
        y = i * 150 + rnd.randint(-10, 10)
        parts.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y + rnd.randint(-8, 8)}" stroke="{p["wood2"]}" stroke-width="3" opacity=".45"/>')
        for _ in range(4):
            x = rnd.randint(0, W)
            parts.append(f'<path d="M{x} {y + 30} q60 {rnd.randint(-20, 20)} 180 0" stroke="{p["wood2"]}" stroke-width="1.5" fill="none" opacity=".3"/>')
    # листы эскизов
    for i, (x, y, a) in enumerate(((120, 140, -8), (260, 190, 5))):
        parts.append(f'<g transform="rotate({a} {x + 250} {y + 330})"><rect x="{x + 12}" y="{y + 16}" width="500" height="660" fill="rgba({s},.3)" filter="url(#soft2)"/><rect x="{x}" y="{y}" width="500" height="660" fill="#fbfaf6"/>'
                     + "".join(f'<path d="M{x + 60} {y + 120 + k * 70} q{rnd.randint(80, 160)} -{rnd.randint(20, 60)} {rnd.randint(260, 380)} {rnd.randint(-20, 20)}" stroke="#6d6a64" stroke-width="2" fill="none" opacity=".45"/>' for k in range(7))
                     + "</g>")
    parts.append(f'<circle cx="480" cy="520" r="120" fill="none" stroke="#6d6a64" stroke-width="2" opacity=".4" transform="rotate(5 480 520)"/>')
    # палитра
    px, py = 1080, 560
    parts.append(f'<ellipse cx="{px + 20}" cy="{py + 30}" rx="360" ry="250" fill="rgba({s},.35)" filter="url(#soft)"/>')
    parts.append(f'<path d="M{px - 330} {py} c0 -170 200 -250 380 -230 c190 20 300 130 290 270 c-10 150 -170 230 -330 220 c-80 -5 -60 -80 -130 -90 c-70 -10 -80 60 -140 40 c-50 -15 -70 -110 -70 -210z" fill="#d8b98f"/>')
    parts.append(f'<ellipse cx="{px - 170}" cy="{py + 110}" rx="44" ry="34" fill="url(#table)"/>')
    rnd2 = random.Random(5)
    for i, c in enumerate(p["paints"]):
        a = -2.7 + i * 0.42
        import math
        cx, cy = px + math.cos(a) * 230, py + 10 + math.sin(a) * 150
        r = rnd2.randint(30, 44)
        parts.append(f'<g filter="url(#wc)"><circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r}" fill="{c}"/><circle cx="{cx - r * .3:.0f}" cy="{cy - r * .3:.0f}" r="{r * .3:.0f}" fill="#ffffff" opacity=".35"/></g>')
    for i in range(3):
        parts.append(f'<path d="M{px - 60 + i * 70} {py + 40} q40 -30 90 10 q30 30 -20 60 q-60 20 -70 -70z" fill="{p["paints"][i * 2 + 1]}" opacity=".75" filter="url(#wc)"/>')
    # кисти
    for i, c in enumerate(p["paints"][:6]):
        parts.append(brush(620 + i * 40, 900 + i * 22, 380, -18 + i * 3, p, c, rnd))
    # банка с водой
    parts.append(f'<circle cx="1420" cy="230" r="120" fill="rgba({s},.3)" filter="url(#soft2)"/><circle cx="1400" cy="210" r="115" fill="#ffffff" opacity=".45" stroke="#ffffff" stroke-width="10"/><circle cx="1400" cy="210" r="90" fill="{p["sky1"]}" opacity=".6"/>')
    # тюбики
    for i, c in enumerate(p["paints"][:4]):
        x, y = 150 + i * 110, 930 + (i % 2) * 40
        parts.append(f'<g transform="rotate({-20 + i * 12} {x} {y})"><rect x="{x}" y="{y}" width="70" height="200" rx="10" fill="#eceae4"/><rect x="{x}" y="{y + 40}" width="70" height="90" fill="{c}"/><rect x="{x + 20}" y="{y - 30}" width="30" height="34" fill="#3a3a3a"/></g>')
    # маленький холст
    parts.append(f'<g transform="rotate(7 1330 960)">{framed(1180, 820, 300, 300, covers[1], p, frame=p["cloth"], depth=16)}</g>')
    parts.append(finish())
    return parts


def scene_wall(p, covers, rnd):
    y0 = 900
    s = p["shadow"]
    parts = [f'<rect width="{W}" height="{y0}" fill="url(#wall)"/>', planks(p, y0, rnd)]
    # трек со светильниками
    parts.append(f'<rect x="80" y="70" width="{W - 160}" height="12" fill="{p["ink"]}"/>')
    for x in (330, 800, 1270):
        parts.append(f'<polygon points="{x - 20},96 {x + 20},96 {x + 260},760 {x - 260},760" fill="url(#spot)" opacity=".55"/>')
        parts.append(f'<rect x="{x - 8}" y="82" width="16" height="22" fill="{p["ink"]}"/><path d="M{x - 26} 100 h52 l-10 44 h-32z" fill="{p["ink"]}"/>')
    parts.append(framed(170, 250, 320, 400, covers[0], p, frame=p["ink"], depth=20, mat=26))
    parts.append(framed(610, 200, 380, 480, covers[1], p, frame="#ffffff", depth=24))
    parts.append(framed(1110, 260, 320, 390, covers[2], p, frame=p["wood"], depth=20, mat=22))
    # подписи-таблички
    for x in (330, 800, 1270):
        parts.append(f'<rect x="{x - 40}" y="{700 if x != 800 else 720}" width="80" height="26" fill="#ffffff" opacity=".85"/>')
    # холсты у стены (обратной стороной)
    for i, (x, w, h, a) in enumerate(((140, 300, 380, -3), (390, 260, 330, 2))):
        parts.append(f'<g transform="rotate({a} {x + w / 2} {y0 + 140})"><rect x="{x + 14}" y="{y0 + 150 - h + 16}" width="{w}" height="{h}" fill="rgba({s},.3)" filter="url(#soft2)"/>'
                     f'<rect x="{x}" y="{y0 + 150 - h}" width="{w}" height="{h}" fill="#e8dfcd" stroke="{p["wood"]}" stroke-width="16"/>'
                     f'<line x1="{x + w / 2}" y1="{y0 + 150 - h}" x2="{x + w / 2}" y2="{y0 + 150}" stroke="{p["wood"]}" stroke-width="12"/></g>')
    # скамья
    parts.append(f'<ellipse cx="1180" cy="1110" rx="330" ry="26" fill="rgba({s},.25)" filter="url(#soft2)"/><rect x="900" y="980" width="560" height="36" fill="{p["wood"]}"/><rect x="900" y="1016" width="560" height="10" fill="{p["wood2"]}"/><rect x="930" y="1026" width="22" height="84" fill="{p["wood2"]}"/><rect x="1408" y="1026" width="22" height="84" fill="{p["wood2"]}"/>')
    parts.append(f'<rect x="1000" y="930" width="150" height="50" fill="{p["cloth"]}"/><rect x="1010" y="905" width="130" height="26" fill="{p["accent"]}"/>')
    parts.append(plant(1530, 960, p, 0.8))
    parts.append(finish())
    return parts


def scene_shelf(p, covers, rnd):
    s = p["shadow"]
    parts = [f'<rect width="{W}" height="{H}" fill="url(#wall)"/>']
    # стеллаж
    sx, sw = 140, 820
    shelves = (260, 520, 780, 1040)
    parts.append(f'<rect x="{sx + 20}" y="120" width="{sw}" height="{H}" fill="rgba({s},.18)" filter="url(#soft)"/>')
    parts.append(f'<rect x="{sx}" y="110" width="24" height="{H}" fill="{p["wood2"]}"/><rect x="{sx + sw - 24}" y="110" width="24" height="{H}" fill="{p["wood2"]}"/>')
    for y in shelves:
        parts.append(f'<rect x="{sx}" y="{y}" width="{sw}" height="22" fill="{p["wood"]}"/><rect x="{sx}" y="{y + 22}" width="{sw}" height="8" fill="{p["wood2"]}"/>')
    # полка 1: банки с кистями
    for i in range(4):
        x = sx + 70 + i * 180
        for k, c in enumerate(p["paints"][i:i + 4]):
            parts.append(brush(x + 30 + k * 10, shelves[0] - 70, 140, -100 + k * 7, p, c, rnd))
        parts.append(f'<path d="M{x} {shelves[0] - 110} h110 l-8 110 h-94z" fill="#ffffff" opacity=".5" stroke="rgba(0,0,0,.12)"/>')
    # полка 2: книги/альбомы
    x = sx + 50
    for i in range(14):
        w = rnd.randint(30, 52)
        h = rnd.randint(150, 215)
        c = [p["ink"], p["accent"], p["cloth"], p["wood2"], p["paints"][4], p["plant2"]][i % 6]
        parts.append(f'<rect x="{x}" y="{shelves[1] - h}" width="{w}" height="{h}" fill="{c}"/><rect x="{x + 6}" y="{shelves[1] - h + 20}" width="{w - 12}" height="8" fill="#ffffff" opacity=".35"/>')
        x += w + 4
    parts.append(f'<rect x="{x + 30}" y="{shelves[1] - 60}" width="190" height="60" fill="{p["cloth"]}"/><rect x="{x + 40}" y="{shelves[1] - 100}" width="170" height="40" fill="#ffffff" opacity=".8"/>')
    # полка 3: тюбики и рулоны холста
    for i, c in enumerate(p["paints"]):
        x = sx + 60 + i * 50
        parts.append(f'<rect x="{x}" y="{shelves[2] - 150}" width="38" height="150" rx="6" fill="#eceae4"/><rect x="{x}" y="{shelves[2] - 110}" width="38" height="60" fill="{c}"/><rect x="{x + 10}" y="{shelves[2] - 172}" width="18" height="24" fill="#3a3a3a"/>')
    for i in range(3):
        parts.append(f'<rect x="{sx + 520}" y="{shelves[2] - 60 - i * 55}" width="260" height="52" rx="26" fill="#efe6d4" stroke="{p["wood2"]}" stroke-width="3"/><ellipse cx="{sx + 780}" cy="{shelves[2] - 34 - i * 55}" rx="14" ry="26" fill="#d8ccb4"/>')
    # полка 4: подрамники
    for i in range(4):
        parts.append(f'<rect x="{sx + 60 + i * 60}" y="{shelves[3] - 220 + i * 10}" width="170" height="{220 - i * 10}" fill="none" stroke="{p["wood"]}" stroke-width="14"/>')
    parts.append(framed(sx + 480, shelves[3] - 200, 240, 180, covers[2], p, frame=p["cloth"], depth=14))
    # справа — картина и лампа
    parts.append(framed(1100, 230, 380, 470, covers[0], p, frame=p["ink"], depth=20, mat=24))
    parts.append(f'<path d="M1290 760 l-60 260 h120z" fill="{p["ink"]}"/><rect x="1180" y="1020" width="220" height="16" fill="{p["ink"]}"/>'
                 f'<path d="M1210 760 h160 l-30 -90 h-100z" fill="{p["accent"]}"/><polygon points="1215,760 1365,760 1480,1100 1100,1100" fill="url(#beam)" opacity=".5"/>')
    parts.append(f'<rect x="0" y="1100" width="{W}" height="{H - 1100}" fill="url(#floor)"/>')
    parts.append(finish())
    return parts


SCENES = [
    ("studio-window", scene_window, ("Мастерская у окна: мольберт с картиной", "Studio by the window: an easel with a painting"),
     ("Мастерская у окна", "The studio by the window")),
    ("studio-table", scene_table, ("Рабочий стол художника: палитра, кисти и эскизы", "The artist’s desk: palette, brushes and sketches"),
     ("Рабочий стол", "The work desk")),
    ("studio-wall", scene_wall, ("Стена с работами под светом софитов", "A wall of works under spotlights"),
     ("Работы на стене", "Works on the wall")),
    ("studio-shelf", scene_shelf, ("Стеллаж с материалами: кисти, краски и подрамники", "Shelves with materials: brushes, paints and stretchers"),
     ("Материалы", "Materials")),
]


def covers_for(site):
    media = ROOT / "seed" / site / "media"
    order = ["cover-sea.jpg", "cover-flowers.jpg", "cover-abstract.jpg", "cover-landscape.jpg", "cover-women.jpg"]
    files = [media / name for name in order if (media / name).exists()]
    return [embed(f) for f in files]


def main(site):
    p = PALETTES[site]
    covers = covers_for(site)
    out_dir = ROOT / "seed" / site / "media"
    for i, (name, fn, _alt, _caption) in enumerate(SCENES):
        rnd = random.Random(i + (0 if site == "a" else 100))
        rot = covers[i:] + covers[:i]
        body = "".join(fn(p, rot, rnd))
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{defs(p)}{body}</svg>'
        (out_dir / f"{name}.svg").write_text(svg, encoding="utf-8")
        print(out_dir / f"{name}.svg")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "a")
