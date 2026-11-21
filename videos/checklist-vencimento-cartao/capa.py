"""Capa do TikTok: Checklist do Consultor · A melhor data de vencimento do cartão (3 passos)."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "A MELHOR DATA", 540, 300, 104, CREME)
    numero_i(c, "DO SEU CARTÃO", 540, 440, 104, GOLD)
    for i, s in enumerate(("1. VENCE DEPOIS DO SALÁRIO", "2. ACHA O FECHAMENTO", "3. COMPRA NO MELHOR DIA")):
        rr(c, 90, 520 + i * 108, 900, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 130, 584 + i * 108, 48, MARKER, TINTA, align="l")
    rr(c, 150, 860, 780, 100, 26); rgb(c, VERDE); c.fill()
    text(c, "ATÉ 40 DIAS PRA PAGAR", 540, 928, 50, MARKER, CREME)
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 100, 1560, 880, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA E TROCA NO APP HOJE", 540, 1632, 48, MARKER, CREME)


SCENES = [(0, 999, capa)]
