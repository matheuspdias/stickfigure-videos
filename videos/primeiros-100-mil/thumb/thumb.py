"""Thumbnails do vídeo dos primeiros R$ 100 mil (Faz a Conta). Rodar da raiz: python videos/primeiros-100-mil/thumb/thumb.py"""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *
OUT = os.path.dirname(os.path.abspath(__file__))


def surf():
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    return s, c


def big(c, s, x, y, size, col, ow=None):
    text(c, s, x, y, size, MARKER, col, outline=INK, ow=ow or size * 0.12)


def save(s, name):
    p = f"{OUT}/{name}_1080.png"; s.write_to_png(p)
    os.system(f'ffmpeg -loglevel error -y -i "{p}" -vf scale=1280:720:flags=lanczos "{OUT}/{name}.png" && rm "{p}"')


def band(c, label):
    c.rectangle(0, 860, W, 220); rgb(c, NAVY); c.fill()
    line(c, 0, 860, W, 860, 8, GOLD)
    text(c, label, 960, 965, 84, MARKER, GOLD)


# A: escada 6 anos -> 3 anos
s, c = surf()
rgb(c, PAPER); c.paint()
for x, h, col, lab in ((1120, 170, NAVY, "6 anos"), (1400, 340, BLUE, "+4 anos"), (1680, 520, GREEN, "+3 anos")):
    c.save(); c.translate(x, 840); bar(c, h, 230, col); c.restore()
    text(c, lab, x, 840 - h - 50, 72, MARKER, col)
hero(c, 1.0, 210, 1010, 1.2, [(0, "head")], [(0, "shocked")], look=1)
big(c, "R$ 100 MIL", 700, 190, 160, GREEN)
big(c, "CADA VEZ", 690, 430, 92, NAVY)
big(c, "MAIS RÁPIDO", 690, 560, 92, NAVY)
band(c, "guardando o MESMO valor")
save(s, "100mil_thumb_A")

# B: 72% foi juros
s, c = surf()
rgb(c, PAPER); c.paint()
c.save(); c.translate(1480, 450)
donut(c, 1.0, 270, 110, GREEN)
c.new_sub_path(); c.arc(0, 0, 270, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.276)
rgb(c, NAVY); c.set_line_width(104); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()
c.restore()
big(c, "72%", 1480, 450, 150, GREEN)
hero(c, 1.0, 230, 1010, 1.3, [(0, "thumb")], [(0, "grin")], prop=("l", prop_tablet), look=1)
big(c, "VOCÊ NÃO", 680, 280, 115, NAVY)
big(c, "FEZ ISSO", 680, 430, 115, NAVY)
text(c, "(foi o dinheiro)", 680, 570, 70, MARKER, GREEN)
band(c, "R$ 1.000 por mês = R$ 1 MILHÃO")
save(s, "100mil_thumb_B")
print("ok")
