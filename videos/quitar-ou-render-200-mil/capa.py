"""Capa do TikTok: R$ 200 mil na mão, quitar o financiamento ou deixar rendendo?"""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "R$ 200 MIL NA MÃO", 540, 330, 86, GOLD)
    numero_i(c, "QUITA OU RENDE?", 540, 460, 100, CREME)
    linhas = (("CONTRATO ACIMA DE 11,5%", "QUITA", VERMELHO), ("CONTRATO ABAIXO DE 11,5%", "RENDE", VERDE))
    for i, (a, b, cor) in enumerate(linhas):
        y = 560 + i * 110
        rr(c, 90, y, 900, 92, 22); rgb(c, CREME); c.fill()
        text(c, a, 120, y + 62, 42, MARKER, NAVY, align="l")
        text(c, b, 960, y + 64, 52, MARKER, cor, align="r")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "think"),), look=0.0)
    rr(c, 110, 1570, 860, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "A CONTA COM OS JUROS DE 2026", 540, 1642, 46, MARKER, CREME)


SCENES = [(0, 999, capa)]
