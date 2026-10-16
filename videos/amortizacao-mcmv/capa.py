"""Capa do TikTok (1080x1920). A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/amortizacao-mcmv/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    c.save(); c.translate(540, 390); hl(c, "+ R$ 200/mês", 0, 0, 96, LGREEN); c.restore()
    text(c, "R$ 62 MIL", 540, 590, 170, MARKER, GREEN)
    text(c, "A MENOS", 540, 750, 120, MARKER, INK)
    c.save(); c.translate(540, 900); hl(c, "prazo ou parcela?", 0, 0, 62, LYELLOW); c.restore()
    c.save(); c.translate(300, 1530); c.scale(1.25, 1.25); apartment(c, LYELLOW, None, 5); c.restore()
    hero(c, 10, 760, 1530, 1.1, [(0, "arms_up")], [(0, "grin")], look=-0.6)
    text(c, "FAZ A CONTA", 540, 1800, 54, MARKER, GOLD)


SCENES = [(0.0, 999.0, capa)]
