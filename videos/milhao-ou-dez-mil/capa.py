"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/milhao-ou-dez-mil/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "R$ 1 MILHÃO", 540, 400, 130, MARKER, NAVY)
    c.save(); c.translate(540, 560); hl(c, "OU", 0, 0, 90, LYELLOW); c.restore()
    text(c, "R$ 10 MIL", 540, 720, 130, MARKER, GREEN)
    text(c, "por mês pra sempre?", 540, 840, 64, HAND, INK)
    c.save(); c.translate(300, 1180); c.scale(1.3, 1.3); c.rotate(-0.08)
    rrect(c, -170, -60, 340, 120, 14); rgb(c, RED); c.set_line_width(10); c.stroke()
    text(c, "ESCOLHE", 0, 0, 64, MARKER, RED)
    c.restore()
    hero(c, 10, 790, 1540, 1.15, [(0, "think")], [(0, "think")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
