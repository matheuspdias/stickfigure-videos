"""Capa do TikTok: Checklist do Consultor · 4 passos quando o 13º cair."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANDO O", 540, 340, 100, CREME)
    numero_i(c, "13º CAIR", 540, 480, 150, GOLD)
    for i, s in enumerate(("1. DÍVIDA CARA PRIMEIRO", "2. SEPARA JANEIRO", "3. A SUA PARTE", "4. O TETO DO NATAL")):
        rr(c, 110, 580 + i * 105, 860, 88, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 642 + i * 105, 48, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.3, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 230, 1570, 620, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRO DIA QUE CAIR", 540, 1642, 50, MARKER, CREME)


SCENES = [(0, 999, capa)]
