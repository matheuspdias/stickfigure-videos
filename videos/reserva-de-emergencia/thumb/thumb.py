"""Thumbnails do vídeo Reserva de emergência (Faz a Conta). Rodar da raiz: python videos/reserva-de-emergencia/thumb/thumb.py"""
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


# A: demitido hoje: quantos meses você aguenta?
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "DEMITIDO", 1200, 160, 150, RED)
big(c, "HOJE?", 1200, 330, 150, RED)
c.save(); c.translate(820, 610); c.scale(1.2, 1.2); moving_box(c); c.restore()
big(c, "? MESES", 1420, 600, 150, NAVY)
hero(c, 1.0, 260, 1010, 1.15, [(0, "head")], [(0, "shocked")], look=1)
band(c, "quanto tempo você aguentaria?")
save(s, "reserva_thumb_A")

# B: Camila x Bruno: +R$ 7 mil x -R$ 15 mil
s, c = surf()
rgb(c, PAPER); c.paint()
big(c, "MESMA DEMISSÃO", 960, 110, 100, NAVY)
figure(c, 1.0, 420, 850, 0.85, poses=[(0, "arms_up")], exprs=[(0, "grin")], shirt=PURPLE, hair="long", fid=3, look=0.5)
other(c, 1.0, 1500, 850, 0.85, [(0, "head")], [(0, "desperate")], shirt=ORANGE, fid=4, look=-0.5)
big(c, "+R$ 7 MIL", 420, 260, 110, GREEN)
big(c, "-R$ 15 MIL", 1500, 260, 110, RED)
c.save(); c.translate(760, 520); c.scale(1.1, 1.1); piggy(c); c.restore()
c.save(); c.translate(1160, 520); c.scale(1.2, 1.2); card(c, RED); c.restore()
hero(c, 1.0, 960, 850, 0.5, [(0, "shrug")], [(0, "think")])
band(c, "a diferença é a reserva de emergência")
save(s, "reserva_thumb_B")
print("ok")
