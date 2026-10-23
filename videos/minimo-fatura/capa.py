"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/minimo-fatura/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "PAGOU SÓ O", 540, 380, 110, MARKER, INK)
    text(c, "MÍNIMO?", 540, 520, 150, MARKER, RED)
    c.save(); c.translate(330, 820); c.scale(1.7, 1.7); card(c, NAVY); c.restore()
    text(c, "R$ 1.000", 760, 760, 84, MARKER, INK)
    arrow(c, 760, 810, 760, 920, RED, 9)
    c.save(); c.translate(540, 1050); hl(c, "R$ 1.819", 0, 0, 140, (1, 0.8, 0.76), RED); c.restore()
    hero(c, 10, 780, 1640, 0.95, [(0, "head")], [(0, "shocked")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
