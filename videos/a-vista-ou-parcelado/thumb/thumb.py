"""Thumbnails do vídeo À vista ou parcelado (Faz a Conta). Rodar da raiz: python videos/a-vista-ou-parcelado/thumb/thumb.py"""
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


# A: "sem juros" esconde 26% ao ano
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "\"SEM JUROS\"", 1180, 150, 130, NAVY)
c.save(); c.translate(720, 470); c.scale(1.25, 1.25); tv(c, LBLUE); c.restore()
c.save(); c.translate(940, 290); c.rotate(-0.12); price_tag(c, "10x R$ 300", YELLOW, 52); c.restore()
big(c, "26%", 1450, 440, 220, RED)
text(c, "de juros ao ano", 1450, 620, 66, MARKER, DGRAY)
hero(c, 1.0, 200, 1010, 1.1, [(0, "head")], [(0, "shocked")], look=1)
band(c, "à vista ou parcelado? faça a conta")
save(s, "parcelado_thumb_A")

# B: à vista x parcelado, regra ÷2
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "À VISTA", 480, 170, 130, GREEN)
big(c, "PARCELADO", 1440, 170, 120, ORANGE)
big(c, "x", 960, 175, 110, INK)
c.save(); c.translate(480, 420); c.scale(1.6, 1.6); pix_tag(c); c.restore()
c.save(); c.translate(1440, 420); c.scale(1.6, 1.6); card(c, NAVY); c.restore()
big(c, "÷ 2", 960, 620, 170, NAVY)
text(c, "a regra de 10 segundos", 960, 770, 60, MARKER, DGRAY)
hero(c, 1.0, 1760, 1010, 0.8, [(0, "finger_up")], [(0, "confident")], look=-1)
band(c, "qual sai mais barato na Black Friday?")
save(s, "parcelado_thumb_B")
print("ok")
