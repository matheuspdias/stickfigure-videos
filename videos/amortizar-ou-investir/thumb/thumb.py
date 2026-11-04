"""Thumbnails do vídeo Amortizar o financiamento ou investir? (Faz a Conta). Rodar da raiz: python videos/amortizar-ou-investir/thumb/thumb.py"""
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


def at_(c, x, y, fn, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); fn(c); c.restore()


# A: Carla (amortizou) x Diego (investiu): quem ganhou?
s, c = surf()
rgb(c, PAPER); c.paint()
figure(c, 1.0, 300, 820, 0.85, poses=[(0, "arms_up")], exprs=[(0, "grin")], shirt=PURPLE, hair="long", fid=3, look=0.5)
other(c, 1.0, 1620, 820, 0.85, [(0, "thumb")], [(0, "happy")], look=-0.5)
at_(c, 300, 200, brick, 1.1)
at_(c, 1620, 210, piggy, 0.9)
big(c, "AMORTIZAR", 960, 200, 130, PURPLE)
big(c, "OU", 960, 350, 90, NAVY)
big(c, "INVESTIR?", 960, 500, 140, BLUE)
c.save(); c.translate(960, 680); hl(c, "R$ 300 por mês, 30 anos", 0, 0, 70, LYELLOW); c.restore()
band(c, "a conta completa do financiamento")
save(s, "amortizar_thumb_A")

# B: R$ 300 a mais = 13 anos a menos
s, c = surf()
rgb(c, PAPER); c.paint()
at_(c, 330, 420, lambda c: house(c, True), 1.6)
at_(c, 330, 700, lambda c: house_key(c, GOLD), 1.1)
big(c, "+ R$ 300", 1020, 190, 150, GREEN)
big(c, "= 13 ANOS", 1020, 380, 150, RED)
big(c, "A MENOS?", 1020, 560, 130, RED)
c.save(); c.translate(1020, 720); hl(c, "ou é melhor investir?", 0, 0, 70, LYELLOW); c.restore()
hero(c, 1.0, 1710, 845, 0.62, [(0, "head")], [(0, "shocked")], look=-1)
band(c, "Amortizar ou investir?")
save(s, "amortizar_thumb_B")
print("ok")
