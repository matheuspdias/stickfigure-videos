"""Capa do TikTok ir-duas-rendas-2027, estilo caderno (modelo videos/dolar-6-reais-no-bolso/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "GANHA MENOS DE 5 MIL", 540, 380, 70, MARKER, NAVY)
    c.save(); c.translate(540, 520); hl(c, "E VAI PAGAR IR?", 0, 0, 96, (1, 0.8, 0.76), RED); c.restore()
    text(c, "2 empregos de R$ 3 mil", 540, 680, 60, HAND, DGRAY)
    text(c, "em 2027 o Leão cobra", 360, 860, 52, HAND, DGRAY)
    text(c, "~R$ 3.400", 360, 990, 100, MARKER, RED)
    hero(c, 10, 840, 1300, 0.9, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1420); hl(c, "FAZ A CONTA", 0, 0, 70, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
