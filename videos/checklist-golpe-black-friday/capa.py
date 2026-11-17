"""Capa do TikTok: Checklist do Consultor · 3 sinais de golpe na Black Friday."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "3 GOLPES DA", 540, 340, 100, CREME)
    numero_i(c, "BLACK FRIDAY", 540, 480, 130, GOLD)
    for i, s in enumerate(("1. O DESCONTO DE MENTIRA", "2. A LOJA SÓ NO PIX", "3. SEM JUROS COM JUROS")):
        rr(c, 110, 580 + i * 105, 860, 88, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 642 + i * 105, 48, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "shocked"),), look=0.0)
    rr(c, 200, 1570, 680, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA ANTES DO DIA 27", 540, 1642, 50, MARKER, CREME)


SCENES = [(0, 999, capa)]
