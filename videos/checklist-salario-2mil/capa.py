"""Capa do TikTok: Checklist do Consultor · Parte 2 · salário de R$ 2 mil caiu, 4 passos."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1300))
    rr(c, 390, 225, 300, 70, 20); rgb(c, GOLD); c.fill()
    text(c, "PARTE 2", 540, 275, 44, MARKER, TINTA)
    numero_i(c, "SALÁRIO DE", 540, 390, 100, CREME)
    numero_i(c, "R$ 2 MIL CAIU", 540, 520, 120, GOLD)
    for i, s in enumerate(("1. O QUE JÁ TEM DONO", "2. A SUA PARTE", "3. O MERCADO DO MÊS", "4. SEU NÚMERO DO DIA")):
        rr(c, 110, 600 + i * 108, 860, 92, 22); rgb(c, CREME); c.fill()
        text(c, s, 150, 664 + i * 108, 48, MARKER, TINTA, align="l")
    consultor_i(c, t, 540, 2300, 2.2, poses=((0, "finger_up"),), exprs=((0, "confident"),), look=0.0)
    rr(c, 300, 1560, 480, 110, 26); rgb(c, VERMELHO); c.fill()
    text(c, "SALVA PRO DIA 5", 540, 1632, 54, MARKER, CREME)


SCENES = [(0, 999, capa)]
