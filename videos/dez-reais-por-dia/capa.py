"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/dez-reais-por-dia/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    c.save(); c.translate(540, 400); hl(c, "R$ 10 por dia", 0, 0, 100, LYELLOW); c.restore()
    text(c, "=", 540, 560, 110, MARKER, INK)
    text(c, "R$ 1 MILHÃO", 540, 720, 150, MARKER, GREEN)
    c.save(); c.translate(540, 880); hl(c, "será?", 0, 0, 72, (1, 0.8, 0.76)); c.restore()
    c.save(); c.translate(300, 1400); c.scale(1.2, 1.2); sandwich(c); c.restore()
    hero(c, 10, 770, 1560, 1.05, [(0, "head")], [(0, "shocked")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
