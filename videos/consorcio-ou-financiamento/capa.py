"""Capa do TikTok consorcio-ou-financiamento, estilo caderno.
    python render.py stills videos/consorcio-ou-financiamento/capa.py out/capas_cons 10"""
from engine import *  # noqa

VERTICAL = True
PINKD = (0.85, 0.30, 0.52)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "CONSÓRCIO É", 540, 340, 92, MARKER, NAVY)
    text(c, "JOGADO FORA?", 540, 450, 96, MARKER, RED)
    c.save(); c.translate(540, 650); c.scale(0.9, 0.9); car(c, LBLUE); c.restore()
    text(c, "consórcio", 290, 830, 52, HAND, PINKD)
    text(c, "R$ ???", 290, 910, 80, MARKER, PINKD)
    text(c, "financiar", 790, 830, 52, HAND, GREEN)
    text(c, "R$ ???", 790, 910, 80, MARKER, GREEN)
    other(c, 10, 290, 1330, 0.6, [(0, "think")], [(0, "think")], shirt=PINK, fid=4, hair="long", look=0.4)
    other(c, 10, 790, 1330, 0.6, [(0, "shrug")], [(0, "worried")], shirt=GREEN, fid=3, hair="tuft", look=-0.4)
    c.save(); c.translate(540, 1480); hl(c, "FAZ A CONTA", 0, 0, 70, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
