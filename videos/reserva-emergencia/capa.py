"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/reserva-emergencia/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "DEMITIDO", 540, 400, 150, MARKER, RED)
    text(c, "HOJE?", 540, 560, 150, MARKER, INK)
    c.save(); c.translate(540, 760); hl(c, "quantos dias você aguenta?", 0, 0, 62, LYELLOW); c.restore()
    c.save(); c.translate(330, 1080); c.scale(1.9, 1.9); calendar(c, "20", RED, 80); c.restore()
    c.save(); c.translate(330, 1290); text(c, "dias", 0, 0, 56, HAND); c.restore()
    hero(c, 10, 760, 1520, 1.15, [(0, "head")], [(0, "shocked")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
