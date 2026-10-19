"""Thumbnails do vídeo do 13º (Faz a Conta). Rodar da raiz: python videos/decimo-terceiro/thumb/thumb.py"""
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


# A: o 13º que vira R$ 183 mil
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "SEU 13º", 760, 170, 150, NAVY)
c.save(); c.translate(760, 400); c.scale(1.5, 1.5); bills(c, 3); c.restore()
arrow(c, 1040, 420, 1260, 420, INK, 14, 0.1, 40)
big(c, "R$ 183 MIL", 1500, 330, 120, GREEN)
text(c, "sem mexer no salário", 1500, 470, 60, MARKER, DGRAY)
c.save(); c.translate(1500, 790); c.scale(0.5, 0.5); tree(c, 1.0); c.restore()
hero(c, 1.0, 190, 1010, 1.15, [(0, "arms_up")], [(0, "grin")], look=1)
band(c, "o MELHOR destino pro seu 13º")
save(s, "decimo_thumb_A")

# B: não gaste o 13º antes de ver essa conta (cartão 14x)
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "NÃO GASTE", 960, 150, 140, RED)
big(c, "o seu 13º", 960, 300, 110, NAVY)
text(c, "antes de ver essa conta", 960, 420, 66, MARKER, DGRAY)
c.save(); c.translate(560, 640); c.scale(1.5, 1.5); card(c, RED); c.restore()
big(c, "14x", 1140, 650, 200, RED)
hero(c, 1.0, 1700, 1010, 1.1, [(0, "head")], [(0, "shocked")], look=-1)
band(c, "o erro de quase todo mundo")
save(s, "decimo_thumb_B")
print("ok")
