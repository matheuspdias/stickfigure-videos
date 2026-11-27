"""Capa do TikTok pedir-demissao-acordo-demitido, estilo caderno.
    python render.py stills videos/pedir-demissao-acordo-demitido/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True
PINKD = (0.85, 0.30, 0.52)
ORANGED = (0.85, 0.45, 0.10)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "PEDIR DEMISSÃO,", 540, 340, 88, MARKER, NAVY)
    text(c, "ACORDO OU", 540, 440, 88, MARKER, NAVY)
    text(c, "SER DEMITIDO?", 540, 545, 96, MARKER, RED)
    for x, v, col, nm, kw in ((200, "R$ 10 mil", PINKD, "PEDIU", dict(shirt=PINK, fid=4, hair="long")),
                              (540, "R$ 19 mil", ORANGED, "ACORDO", dict(shirt=ORANGE, fid=5, hair="long")),
                              (880, "R$ 34 mil", GREEN, "DEMITIDO", dict(shirt=GREEN, fid=3, hair="tuft"))):
        text(c, v, x, 760, 54, MARKER, col)
        text(c, nm, x, 830, 44, MARKER, DGRAY)
        other(c, 10, x, 1300, 0.5, [(0, "arms_up" if nm == "DEMITIDO" else ("head" if nm == "PEDIU" else "stand"))],
              [(0, "grin" if nm == "DEMITIDO" else ("worried" if nm == "PEDIU" else "neutral"))], look=0, **kw)
    c.save(); c.translate(540, 1480); hl(c, "SALÁRIO DE R$ 3 MIL", 0, 0, 62, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
