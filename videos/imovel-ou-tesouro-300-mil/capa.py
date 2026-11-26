"""Capa do TikTok imovel-ou-tesouro-300-mil, estilo caderno (modelo videos/carro-novo-usado-mesmo-salario/capa.py).
    python render.py stills videos/imovel-ou-tesouro-300-mil/capa.py out/capas 10"""
from engine import *  # noqa

VERTICAL = True
PINKD = (0.85, 0.30, 0.52)


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "IMÓVEL É O MELHOR", 540, 340, 86, MARKER, NAVY)
    text(c, "INVESTIMENTO?", 540, 450, 100, MARKER, RED)
    c.save(); c.translate(540, 570); hl(c, "R$ 300 MIL CADA", 0, 0, 60, LYELLOW); c.restore()
    line(c, 540, 650, 540, 1330, 4, LGRAY)
    c.save(); c.translate(290, 960); c.scale(0.7, 0.7); apartment(c, LYELLOW, "ALUGA-SE", 4); c.restore()
    text(c, "APÊ", 290, 1020, 70, MARKER, PINKD)
    c.save(); c.translate(790, 830); bank(c); c.restore()
    text(c, "TESOURO", 790, 1020, 70, MARKER, GREEN)
    other(c, 10, 290, 1330, 0.5, [(0, "shrug")], [(0, "worried")], shirt=PINK, fid=4, hair="long", look=0.3)
    other(c, 10, 790, 1330, 0.5, [(0, "thumb")], [(0, "grin")], shirt=GREEN, fid=3, hair="tuft", look=-0.3)
    c.save(); c.translate(540, 1480); hl(c, "QUEM GANHA MAIS?", 0, 0, 66, (1, 0.8, 0.76), RED); c.restore()


SCENES = [(0, 999, capa)]
