"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/financiar-carro/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    c.save(); c.translate(540, 380); hl(c, "VAI FINANCIAR?", 0, 0, 100, LYELLOW); c.restore()
    text(c, "O QUE", 540, 570, 120, MARKER, INK)
    text(c, "NINGUÉM", 540, 710, 120, MARKER, RED)
    text(c, "TE CONTA", 540, 850, 120, MARKER, RED)
    c.save(); c.translate(540, 1000); hl(c, "R$ 26.700 só de juros", 0, 0, 60, (1, 0.8, 0.76)); c.restore()
    c.save(); c.translate(290, 1500); c.scale(1.4, 1.4); car(c, BLUE); c.restore()
    hero(c, 10, 820, 1560, 1.0, [(0, "head")], [(0, "shocked")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
