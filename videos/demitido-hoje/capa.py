"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/demitido-hoje/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "DEMITIDO", 540, 400, 150, MARKER, RED)
    text(c, "HOJE?", 540, 560, 150, MARKER, INK)
    c.save(); c.translate(540, 740); hl(c, "quanto cai na conta?", 0, 0, 66, LYELLOW); c.restore()
    c.save(); c.translate(540, 960); hl(c, "R$ 21.164", 0, 0, 140, LGREEN); c.restore()
    text(c, "salário de R$ 3 mil, 2 anos", 540, 1090, 52, HAND, DGRAY)
    hero(c, 10, 540, 1640, 0.9, [(0, "arms_up")], [(0, "shocked")], look=0)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
