"""Capa do TikTok dolar-6-reais-no-bolso, estilo caderno (modelo videos/ferias-mes-seguinte/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660.
    python render.py stills videos/dolar-6-reais-no-bolso/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "DÓLAR A R$ 6", 540, 390, 120, MARKER, NAVY)
    c.save(); c.translate(540, 560); hl(c, "O QUE FICA MAIS CARO", 0, 0, 70, (1, 0.8, 0.76), RED); c.restore()
    text(c, "NO SEU BOLSO", 540, 690, 92, MARKER, RED)
    c.save(); c.translate(280, 930); c.scale(1.3, 1.3); dollar_bill(c); c.restore()
    text(c, "viagem de US$ 1.000", 280, 1110, 46, HAND, DGRAY)
    text(c, "+ R$ 1.035", 280, 1190, 76, MARKER, RED)
    hero(c, 10, 770, 1300, 0.85, [(0, "head")], [(0, "shocked")], look=-0.4)
    c.save(); c.translate(540, 1420); hl(c, "FAZ A CONTA", 0, 0, 70, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
