"""Thumbnails do vídeo alugar ou comprar (Faz a Conta). Rodar da raiz: python videos/alugar-ou-comprar/thumb/thumb.py"""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080


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


# A: quem fica mais rico em 30 anos?
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "ALUGAR", 470, 130, 130, PURPLE)
big(c, "COMPRAR", 1450, 130, 130, ORANGE)
text(c, "x", 960, 130, 110, MARKER, DGRAY)
other(c, 1.0, 330, 830, 1.15, [(0, "arms_up")], [(0, "grin")], shirt=PURPLE, fid=3)
figure(c, 1.0, 1640, 830, 1.15, poses=[(0, "head")], exprs=[(0, "shocked")], shirt=ORANGE, hair="tuft", fid=2)
c.save(); c.translate(720, 780); bar(c, 470, 220, PURPLE); c.restore()
c.save(); c.translate(1200, 780); bar(c, 390, 220, ORANGE); c.restore()
big(c, "R$ 2,49 MI", 720, 250, 76, PURPLE, 9)
big(c, "R$ 2,06 MI", 1200, 330, 76, ORANGE, 9)
band(c, "30 anos depois: quem tem MAIS?")
save(s, "alugar_thumb_A")

# B: aluguel é dinheiro jogado fora?
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "ALUGUEL É", 760, 150, 120, NAVY)
big(c, "DINHEIRO", 760, 300, 140, RED)
big(c, "JOGADO FORA?", 760, 460, 130, RED)
c.save(); c.translate(1560, 560); c.scale(0.95, 0.95)
balance(c, -0.5, lambda c: (c.scale(0.55, 0.55), house_key(c)), lambda c: (c.scale(0.5, 0.5), bills(c, 2)))
c.restore()
hero(c, 1.0, 170, 1000, 1.1, [(0, "think")], [(0, "think")], look=1)
band(c, "a conta que quase ninguém faz")
save(s, "alugar_thumb_B")
print("ok")
