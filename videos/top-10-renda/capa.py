"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/top-10-renda/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "QUANTO PRA", 540, 380, 110, MARKER, INK)
    text(c, "ESTAR NOS", 540, 510, 110, MARKER, INK)
    c.save(); c.translate(540, 680); hl(c, "TOP 10%?", 0, 0, 150, NAVY, WHITE); c.restore()
    c.save(); c.translate(540, 870); hl(c, "renda de quem trabalha", 0, 0, 58, LYELLOW); c.restore()
    for i, (h, col) in enumerate(((150, BLUE), (300, GREEN), (450, GOLD))):
        x = 180 + i * 190
        c.rectangle(x - 80, 1560 - h, 160, h); fs(c, col, 6)
    text(c, "?", 750, 1150, 260, MARKER, GOLD, outline=INK, ow=12)
    hero(c, 10, 840, 1560, 1.0, [(0, "think")], [(0, "think")], look=-0.6)
    line(c, 60, 1566, 1020, 1566, 5, LGRAY)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
