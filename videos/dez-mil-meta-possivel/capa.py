"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/dez-mil-meta-possivel/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    # comentário genérico (sem nome nem foto)
    rrect(c, 90, 300, 900, 190, 26); fs(c, WHITE, 6)
    circle(c, 160, 370, 40, LGRAY, 4); circle(c, 160, 360, 14, DGRAY, 0)
    rrect(c, 225, 345, 200, 22, 11); rgb(c, LGRAY); c.fill()
    text(c, "100 mil é impossível", 225, 398, 56, HAND, INK, align="l")
    text(c, "pra quem ganha pouco", 225, 448, 56, HAND, INK, align="l")
    text(c, "VOCÊ TEM RAZÃO.", 540, 600, 78, MARKER, NAVY)
    text(c, "E R$ 10 MIL?", 540, 780, 128, MARKER, GREEN)
    c.save(); c.translate(540, 940); hl(c, "a partir de R$ 100 por mês", 0, 0, 58, LYELLOW); c.restore()
    hero(c, 10, 540, 1560, 1.1, [(0, "point_ru")], [(0, "grin")], look=0)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
