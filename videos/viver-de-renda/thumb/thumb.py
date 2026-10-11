"""Thumbnails do vídeo viver de renda (Faz a Conta). Rodar da raiz: python videos/viver-de-renda/thumb/thumb.py"""
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


# A: a conta rápida x a conta honesta
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "R$ 5 MIL/MÊS", 840, 150, 120, NAVY)
text(c, "sem trabalhar", 840, 260, 70, MARKER, DGRAY)
big(c, "R$ 540 MIL?", 840, 420, 120, GRAY)
line(c, 480, 440, 1200, 400, 18, RED)
big(c, "R$ 1,5 MILHÃO", 880, 640, 130, GREEN)
c.save(); c.translate(1640, 560); c.scale(1.3, 1.3); beach_chair(c); c.restore()
hero(c, 1.0, 170, 1010, 1.15, [(0, "head")], [(0, "shocked")], look=1)
band(c, "a PEGADINHA da inflação")
save(s, "renda_thumb_A")

# B: Diego x Júlia
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "MESMO SALÁRIO", 960, 130, 110, NAVY)
c.save(); c.translate(0, 0)
figure(c, 1.0, 420, 800, 1.25, poses=[(0, "head")], exprs=[(0, "desperate")], shirt=ORANGE, hair="spiky", fid=4)
figure(c, 1.0, 1500, 800, 1.25, poses=[(0, "arms_up")], exprs=[(0, "grin")], shirt=PURPLE, hair="long", fid=3)
c.restore()
big(c, "66", 700, 470, 200, RED)
big(c, "42", 1220, 470, 200, GREEN)
text(c, "livre aos", 700, 330, 64, MARKER, RED)
text(c, "livre aos", 1220, 330, 64, MARKER, GREEN)
c.save(); c.translate(1760, 520); c.scale(0.8, 0.8); beach_chair(c, False); c.restore()
band(c, "24 ANOS de diferença: por quê?")
save(s, "renda_thumb_B")
print("ok")
