"""Capa do TikTok janeiro-2027-contas, estilo caderno (modelo videos/dolar-6-reais-no-bolso/capa.py).
A grade do perfil corta para 3:4: o essencial fica entre y 260 e 1660."""
from engine import *  # noqa

VERTICAL = True


def capa(c, t):
    rgb(c, NAVY); c.paint()
    rrect(c, 40, 230, 1000, 1460, 40); fs(c, PAPER, 0)
    text(c, "JANEIRO DE 2027", 540, 380, 96, MARKER, NAVY)
    c.save(); c.translate(540, 510); hl(c, "VOCÊ JÁ DEVE", 0, 0, 80, (1, 0.8, 0.76), RED); c.restore()
    text(c, "~R$ 4.100", 540, 690, 150, MARKER, RED)
    for i, (tit, col) in enumerate((("IPVA", RED), ("IPTU", ORANGE), ("ESCOLA", BLUE), ("FATURA", PURPLE))):
        c.save(); c.translate(170 + i * 150, 950 - i * 15); c.scale(0.6, 0.6); boleto(c, tit, col); c.restore()
    hero(c, 10, 860, 1380, 0.8, [(0, "head")], [(0, "shocked")], look=-0.6)
    c.save(); c.translate(400, 1250); hl(c, "CUIDADO!", 0, 0, 80, LYELLOW); c.restore()
    text(c, "faz a conta antes de dezembro", 470, 1520, 52, HAND, DGRAY)


SCENES = [(0, 999, capa)]
