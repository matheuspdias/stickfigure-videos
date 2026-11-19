"""Capa do TikTok: Quanto rende R$ 1.000 em 1 ano (Parte 1)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANTO RENDE", 540, 330, 110, CREME)
    numero_i(c, "R$ 1.000?", 540, 480, 150, GOLD)
    linhas = (("POUPANÇA", "R$ 1.083"), ("TESOURO SELIC", "R$ 1.113"), ("CDB 100% CDI", "R$ 1.113"), ("CDB 110% CDI", "R$ 1.124"))
    for i, (a, b) in enumerate(linhas):
        y = 570 + i * 100
        rr(c, 110, y, 860, 84, 22); rgb(c, CREME); c.fill()
        text(c, a, 150, y + 58, 46, MARKER, NAVY, align="l")
        text(c, b, 930, y + 58, 46, MARKER, VERDE, align="r")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 120, 1570, 840, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "1 ANO, JÁ SEM IMPOSTO · PARTE 1", 540, 1642, 44, MARKER, CREME)


SCENES = [(0, 999, capa)]
