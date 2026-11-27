"""Capa do TikTok saque-aniversario-preso, estilo caderno.
    python render.py stills videos/saque-aniversario-preso/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True
PINKD = (0.85, 0.30, 0.52)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "DEMITIDOS NO", 540, 340, 96, MARKER, NAVY)
    text(c, "MESMO DIA", 540, 450, 110, MARKER, RED)
    line(c, 540, 560, 540, 1330, 4, LGRAY)
    text(c, "R$ 7 mil", 290, 680, 90, MARKER, RED)
    c.save(); c.translate(290, 850); padlock(c, GOLD); c.restore()
    text(c, "R$ 24 mil", 790, 680, 90, MARKER, GREEN)
    c.save(); c.translate(790, 850); bills(c, 3); c.restore()
    other(c, 10, 290, 1320, 0.55, [(0, "head")], [(0, "desperate")], shirt=PINK, fid=4, hair="long", look=0.3)
    other(c, 10, 790, 1320, 0.55, [(0, "arms_up")], [(0, "grin")], shirt=GREEN, fid=3, hair="tuft", look=-0.3)
    c.save(); c.translate(540, 1480); hl(c, "SAQUE-ANIVERSÁRIO?", 0, 0, 66, (1, 0.8, 0.76), RED); c.restore()


SCENES = [(0, 999, capa)]
