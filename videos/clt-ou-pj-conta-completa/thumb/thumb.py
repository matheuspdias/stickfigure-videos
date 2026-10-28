"""Thumbnails do vídeo CLT ou PJ? A conta completa (Faz a Conta). Rodar da raiz: python videos/clt-ou-pj-conta-completa/thumb/thumb.py"""
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


def tagbox(c, s, x, y, col, size=90):
    wd = text_w(c, s, size) + 60
    rrect(c, x - wd / 2, y - size * 0.72, wd, size * 1.44, 22); fs(c, col, 8)
    text(c, s, x, y + 4, size, MARKER, WHITE)


# A: CLT R$ 5 mil x PJ R$ 7 mil: só R$ 130 de diferença
s, c = surf()
rgb(c, PAPER); c.paint()
tagbox(c, "CLT", 470, 130, BLUE); big(c, "R$ 5 MIL", 470, 290, 130, BLUE)
tagbox(c, "PJ", 1450, 130, ORANGE); big(c, "R$ 7 MIL", 1450, 290, 130, ORANGE)
big(c, "x", 960, 230, 110, INK)
c.save(); c.translate(960, 470); hl(c, "SÓ R$ 130 A MAIS?", 0, 0, 110, LYELLOW); c.restore()
figure(c, 1.0, 230, 840, 0.75, poses=[(0, "hips")], exprs=[(0, "confident")], shirt=BLUE, hair="long", fid=3, look=0.6)
figure(c, 1.0, 1700, 840, 0.75, poses=[(0, "shrug")], exprs=[(0, "worried")], shirt=ORANGE, hair="long", fid=3, look=-0.6)
hero(c, 1.0, 960, 845, 0.55, [(0, "head")], [(0, "shocked")])
band(c, "a conta completa de 2026")
save(s, "cltpj_thumb_A")

# B: Consultor chocado + "PJ GANHA MENOS?"
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "PJ DE R$ 7 MIL", 1200, 150, 120, ORANGE)
big(c, "GANHA MENOS", 1200, 330, 130, RED)
big(c, "QUE CLT DE R$ 5 MIL?", 1200, 500, 96, BLUE)
c.save(); c.translate(1200, 700); calculator(c, "-5.290"); c.restore()
hero(c, 1.0, 330, 1000, 1.25, [(0, "head")], [(0, "shocked")], look=1)
band(c, "o detalhe que muda tudo")
save(s, "cltpj_thumb_B")
print("ok")
