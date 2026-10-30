"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/mil-reais-poupanca/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "R$ 1.000", 540, 400, 150, MARKER, GREEN)
    text(c, "NA POUPANÇA", 540, 550, 104, MARKER, INK)
    c.save(); c.translate(540, 720); hl(c, "por 1 ano: quanto rendeu?", 0, 0, 62, LYELLOW); c.restore()
    c.save(); c.translate(320, 1080); c.scale(1.4, 1.4); piggy(c); c.restore()
    text(c, "?", 330, 1280, 220, MARKER, GOLD, outline=INK, ow=12)
    hero(c, 10, 770, 1520, 1.15, [(0, "think")], [(0, "think")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
