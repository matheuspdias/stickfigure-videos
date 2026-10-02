"""Thumbnails do vídeo do carro (Faz a Conta). Rodar da raiz: python videos/carro-5000-v2/thumb/thumb.py"""
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


# A: 41% do salário
s, c = surf()
rgb(c, PAPER); c.paint()
c.rectangle(0, 860, W, 220); rgb(c, NAVY); c.fill()
line(c, 0, 860, W, 860, 8, GOLD)
c.save(); c.translate(1580, 620); c.scale(1.55, 1.55); car(c, RED); c.restore()
c.save(); c.translate(1580, 400); c.rotate(-0.05); c.scale(1.4, 1.4); price_tag(c, "R$ 60 MIL", size=46); c.restore()
hero(c, 1.0, 220, 1010, 1.3, [(0, "head")], [(0, "shocked")], look=1)
big(c, "41%", 820, 320, 300, RED)
big(c, "DO SALÁRIO", 820, 560, 105, NAVY)
text(c, "ganhando R$ 5 mil", 960, 965, 78, MARKER, GOLD)
save(s, "carro_thumb_A")

# B: dá pra comprar?
s, c = surf()
rgb(c, PAPER); c.paint()
c.rectangle(0, 860, W, 220); rgb(c, NAVY); c.fill()
line(c, 0, 860, W, 860, 8, GOLD)
c.save(); c.translate(1600, 620); c.scale(1.55, 1.55); car(c, BLUE); c.restore()
c.save(); c.translate(1600, 400); c.rotate(-0.05); c.scale(1.4, 1.4); price_tag(c, "R$ 60 MIL", size=46); c.restore()
hero(c, 1.0, 220, 1010, 1.3, [(0, "think")], [(0, "think")], prop=("l", prop_calculator), look=1)
big(c, "GANHO", 800, 250, 120, NAVY)
big(c, "R$ 5 MIL", 800, 450, 165, GREEN)
text(c, "DÁ PRA COMPRAR?", 960, 965, 96, MARKER, PAPER, outline=INK, ow=10)
save(s, "carro_thumb_B")
print("ok")
