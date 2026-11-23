"""Capa do TikTok: Dólar a R$ 6, o que fica mais caro no seu bolso."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "DÓLAR A", 540, 290, 120, CREME)
    numero_i(c, "R$ 6", 540, 470, 200, VERMELHO)
    numero_i(c, "O QUE FICA MAIS CARO", 540, 635, 70, GOLD)
    for i, s in enumerate(("VIAGEM: +R$ 1.035", "COMPRINHA: +R$ 40", "GASOLINA, PÃO, CELULAR")):
        rr(c, 140, 695 + i * 100, 800, 84, 22); rgb(c, CREME); c.fill()
        text(c, s, 540, 753 + i * 100, 46, MARKER, TINTA)
    consultor_i(c, t, 540, 2350, 2.2, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "FAZ A CONTA COMIGO", 540, 1632, 50, MARKER, CREME)


SCENES = [(0, 999, capa)]
