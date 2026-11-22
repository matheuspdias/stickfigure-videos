"""Capa do TikTok: Quanto rende R$ 10 mil em 1 ano (Parte 3 de 3)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANTO RENDE", 540, 330, 110, CREME)
    numero_i(c, "R$ 10 MIL?", 540, 480, 140, GOLD)
    linhas = (("POUPANÇA", "R$ 10.826"), ("TESOURO SELIC", "R$ 11.126"), ("CDB 100% CDI", "R$ 11.126"), ("CDB 110% CDI", "R$ 11.239"))
    for i, (a, b) in enumerate(linhas):
        y = 570 + i * 100
        rr(c, 110, y, 860, 84, 22); rgb(c, CREME); c.fill()
        text(c, a, 150, y + 58, 46, MARKER, NAVY, align="l")
        text(c, b, 930, y + 58, 46, MARKER, VERDE, align="r")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 120, 1570, 840, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "1 ANO, JÁ SEM IMPOSTO · PARTE 3", 540, 1642, 44, MARKER, CREME)


SCENES = [(0, 999, capa)]
