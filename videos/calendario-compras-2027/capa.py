"""Capa do TikTok: Você compra no mês errado · calendário de compras 2027."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "VOCÊ COMPRA NO", 540, 330, 100, CREME)
    numero_i(c, "MÊS ERRADO", 540, 470, 140, GOLD)
    for i, (m, s) in enumerate((("FEV / SET", "CELULAR"), ("JAN a MAR", "TV"), ("40 DIAS ANTES", "PASSAGEM"), ("FIM DO ANO", "CARRO"))):
        y = 570 + i * 100
        rr(c, 110, y, 860, 84, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, y + 58, 46, MARKER, NAVY, align="l")
        text(c, m, 930, y + 58, 44, MARKER, VERDE, align="r")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 120, 1570, 840, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA O CALENDÁRIO 2027", 540, 1642, 50, MARKER, CREME)


SCENES = [(0, 999, capa)]
