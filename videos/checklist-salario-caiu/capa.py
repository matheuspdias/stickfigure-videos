"""Capa do TikTok: Checklist do Consultor · 3 passos quando o salário cair."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    numero_i(c, "QUANDO O", 540, 360, 110, CREME)
    numero_i(c, "SALÁRIO CAIR", 540, 500, 130, GOLD)
    for i, s in enumerate(("1. O QUE JÁ TEM DONO", "2. A SUA PARTE", "3. SEU NÚMERO DO DIA")):
        rr(c, 110, 610 + i * 120, 860, 100, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 680 + i * 120, 52, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2250, 2.3, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 300, 1560, 480, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRO DIA 5", 540, 1632, 54, MARKER, CREME)


SCENES = [(0, 999, capa)]
