"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/black-friday-metade-dobro/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "50% OFF", 540, 400, 150, MARKER, RED)
    text(c, "FALSO?", 540, 560, 150, MARKER, INK)
    c.save(); c.translate(540, 740); hl(c, 'o truque da "metade do dobro"', 0, 0, 56, LYELLOW); c.restore()
    c.save(); c.translate(330, 1010); c.scale(1.15, 1.15); tv(c); c.restore()
    text(c, "R$ 2 .000", 330, 1220, 64, MARKER, DGRAY)
    line(c, 200, 1230, 460, 1205, 9, RED)
    text(c, "R$ 1.000", 330, 1310, 76, MARKER, GREEN)
    hero(c, 10, 790, 1560, 1.1, [(0, "point_lu")], [(0, "angry")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
