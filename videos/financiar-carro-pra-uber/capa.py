"""Capa do TikTok financiar-carro-pra-uber, estilo caderno.
    python render.py stills videos/financiar-carro-pra-uber/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "FINANCIAR CARRO", 540, 340, 92, MARKER, NAVY)
    text(c, "PRA RODAR DE APP?", 540, 450, 84, MARKER, RED)
    c.save(); c.translate(330, 650); c.scale(0.8, 0.8); car(c, RED); c.restore()
    c.save(); c.translate(780, 640); c.scale(0.9, 0.9); phone(c, NAVY); c.restore()
    text(c, "faturou", 300, 830, 50, HAND, DGRAY)
    text(c, "R$ 7.000", 300, 910, 80, MARKER, GREEN)
    text(c, "sobrou", 780, 830, 50, HAND, DGRAY)
    text(c, "R$ 1.550", 780, 910, 80, MARKER, RED)
    other(c, 10, 540, 1330, 0.6, [(0, "head")], [(0, "shocked")], shirt=ORANGE, fid=2, look=0)
    c.save(); c.translate(540, 1480); hl(c, "FAZ A CONTA", 0, 0, 70, LYELLOW); c.restore()


SCENES = [(0, 999, capa)]
