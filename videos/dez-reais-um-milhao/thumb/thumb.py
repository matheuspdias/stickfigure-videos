"""Thumbnails do vídeo R$ 10 por dia vira R$ 1 milhão? (Faz a Conta). Rodar da raiz: python videos/dez-reais-um-milhao/thumb/thumb.py"""
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


# A: R$ 10 por dia = R$ 1 milhão? + o milhão que vale R$ 260 mil
s, c = surf()
rgb(c, PAPER); c.paint()
c.save(); c.translate(300, 330); sandwich(c); c.restore()
c.save(); c.translate(300, 560); price_tag(c, "R$ 10/DIA", LYELLOW, 52); c.restore()
big(c, "R$ 1 MILHÃO", 1060, 190, 150, GREEN)
c.save(); c.translate(1060, 190); line(c, -440, 20, 440, -20, 18, RED); c.restore()
big(c, "VALE R$ 260 MIL?", 1060, 410, 118, RED)
c.save(); c.translate(1060, 610); hl(c, "a conta que ninguém mostra", 0, 0, 70, LYELLOW); c.restore()
hero(c, 1.0, 1700, 845, 0.62, [(0, "head")], [(0, "shocked")], look=-1)
band(c, "R$ 10 por dia vira R$ 1 milhão?")
save(s, "milhao_thumb_A")

# B: Ana 10 anos x Bruno 25 anos: quem ficou mais rico?
s, c = surf()
rgb(c, PAPER); c.paint()
figure(c, 1.0, 300, 820, 0.85, poses=[(0, "arms_up")], exprs=[(0, "grin")], shirt=PURPLE, hair="long", fid=3, look=0.5)
other(c, 1.0, 1620, 820, 0.85, [(0, "shrug")], [(0, "worried")], look=-0.5)
big(c, "10 ANOS", 300, 150, 100, PURPLE)
big(c, "25 ANOS", 1620, 150, 100, BLUE)
big(c, "R$ 10", 960, 200, 120, GOLD)
big(c, "POR DIA", 960, 330, 90, GOLD)
big(c, "QUEM FICOU", 960, 520, 110, NAVY)
big(c, "MAIS RICO?", 960, 670, 120, GREEN)
band(c, "o detalhe que muda tudo")
save(s, "milhao_thumb_B")
print("ok")
