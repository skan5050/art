"""Фавиконки брендов: python tools/make_favicons.py — SVG не трогает, PNG/ICO строит по тем же размерам.

МираМе — монограмма «М» на синем скругленном квадрате; ХолСтори — «Х» акцентного цвета на тёмном квадрате.
Файлы лежат в static/themes/<тема>/img/ и отдаются сайту своей темы (общего файла нет).
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent / "static" / "themes"
SCALE = 8


def draw(theme, size):
    s = size * SCALE
    k = s / 64
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if theme == "a":
        d.rounded_rectangle((0, 0, s - 1, s - 1), radius=12 * k, fill="#1c497e")
        pts = [(16, 46), (16, 18), (32, 38), (48, 18), (48, 46)]
        d.line([(x * k, y * k) for x, y in pts], fill="#ffffff", width=round(5 * k), joint="curve")
        for x, y in (pts[0], pts[-1]):
            d.ellipse((x * k - 2.5 * k, y * k - 2.5 * k, x * k + 2.5 * k, y * k + 2.5 * k), fill="#ffffff")
    else:
        d.rectangle((0, 0, s - 1, s - 1), fill="#171a17")
        for a, b in (((19, 19), (45, 45)), ((45, 19), (19, 45))):
            d.line([(a[0] * k, a[1] * k), (b[0] * k, b[1] * k)], fill="#e7f36a", width=round(6.5 * k))
    return im.resize((size, size), Image.LANCZOS)


for theme in ("a", "d"):
    out = ROOT / theme / "img"
    out.mkdir(parents=True, exist_ok=True)
    draw(theme, 180).save(out / "apple-touch-icon.png", optimize=True)
    draw(theme, 32).save(out / "favicon-32.png", optimize=True)
    draw(theme, 64).save(out / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("ok", theme)
